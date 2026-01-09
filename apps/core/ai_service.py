"""
AI 服务封装 - 阿里百炼 DashScope
"""
import json
import logging
import re
from dashscope import Generation
from .models import SystemConfig

logger = logging.getLogger(__name__)


class AIService:
    """AI 评价服务"""
    
    # 人群映射
    CROWD_MAP = {
        'child': '6-12岁儿童',
        'adult': '成年人',
        'elder': '60岁以上老年人'
    }
    
    # 餐次映射
    MEAL_MAP = {
        'breakfast': '早餐',
        'lunch': '午餐',
        'dinner': '晚餐'
    }

    def __init__(self, use_mock=False):
        self.api_key = SystemConfig.get_value('AI_API_KEY', '')
        self.model = SystemConfig.get_value('AI_MODEL', 'deepseek-v3')
        self.timeout = 30
        self.max_retries = 3
        self.use_mock = use_mock or SystemConfig.get_value('AI_USE_MOCK', 'false').lower() == 'true'

    def evaluate_meal(self, crowd_type, meal_type, foods):
        """
        评价膳食搭配
        
        Args:
            crowd_type: 人群类型 (child/adult/elder)
            meal_type: 餐次类型 (breakfast/lunch/dinner)
            foods: 食物列表，每项包含 {name, category, category_display, description}
        
        Returns:
            dict: {
                score, summary, suggestions, good_points, bad_points,
                _meta: {model, prompt, response, used_mock, duration_ms, error}
            }
        """
        import time
        
        meta = {
            'model': self.model,
            'prompt': '',
            'response': '',
            'used_mock': False,
            'duration_ms': 0,
            'error': ''
        }
        
        if self.use_mock or not self.api_key:
            logger.info('使用Mock数据评分')
            meta['used_mock'] = True
            result = self._fallback_evaluation(crowd_type, meal_type, foods)
            result['_meta'] = meta
            return result
        
        logger.info(f'调用AI服务: model={self.model}, foods={[f["name"] for f in foods]}')
        
        prompt = self._build_prompt(crowd_type, meal_type, foods)
        meta['prompt'] = prompt
        
        start_time = time.time()
        
        for attempt in range(self.max_retries):
            try:
                response = self._call_api(prompt)
                meta['response'] = response
                meta['duration_ms'] = int((time.time() - start_time) * 1000)
                
                result = self._parse_response(response)
                result['_meta'] = meta
                return result
            except Exception as e:
                error_msg = str(e)
                logger.error(f'AI调用失败 (尝试 {attempt + 1}/{self.max_retries}): {error_msg}')
                meta['error'] = error_msg
                
                if attempt == self.max_retries - 1:
                    meta['used_mock'] = True
                    meta['duration_ms'] = int((time.time() - start_time) * 1000)
                    result = self._fallback_evaluation(crowd_type, meal_type, foods)
                    result['_meta'] = meta
                    return result
        
        meta['used_mock'] = True
        result = self._fallback_evaluation(crowd_type, meal_type, foods)
        result['_meta'] = meta
        return result

    def _build_prompt(self, crowd_type, meal_type, foods):
        """构建提示词"""
        crowd_name = self.CROWD_MAP.get(crowd_type, '成年人')
        meal_name = self.MEAL_MAP.get(meal_type, '午餐')
        food_details = self._format_foods(foods)
        
        prompt = f"""你是一位专业的营养师，请评价以下膳食搭配。

## 用餐信息
- 用餐人群：{crowd_name}
- 用餐时段：{meal_name}

## 选择的食物
{food_details}

## 评价要求
请从以下几个方面进行评价：
1. 营养均衡性（是否包含主食、蛋白质、蔬菜、水果等）
2. 食物种类搭配是否合理
3. 针对{crowd_name}的适宜性
4. 针对{meal_name}的合理性

## 输出格式
请以JSON格式返回，格式如下：
{{
    "score": 0-100的整数分数,
    "summary": "一句话总结评价（20字以内）",
    "suggestions": ["具体建议1", "具体建议2", "具体建议3"],
    "good_points": ["优点1", "优点2"],
    "bad_points": ["不足1", "不足2"]
}}

## 注意事项
- 评分标准：80分以上为优秀，60-79分为良好，60分以下需改进
- 建议要具体、可操作，适合{crowd_name}理解
- 语言要友好、鼓励性的
- 只返回JSON，不要有其他内容"""
        
        logger.debug(f'AI提示词: {prompt}')
        return prompt

    def _format_foods(self, foods):
        """格式化食物列表"""
        lines = []
        for food in foods:
            name = food.get('name', '')
            category = food.get('category_display', food.get('category', ''))
            desc = food.get('description', '')
            
            line = f"- {name}【{category}】"
            if desc:
                line += f"（{desc}）"
            lines.append(line)
        
        return '\n'.join(lines) if lines else '无'

    def _call_api(self, prompt):
        """调用 DashScope API"""
        response = Generation.call(
            api_key=self.api_key,
            model=self.model,
            messages=[
                {'role': 'system', 'content': '你是一位专业的营养师，擅长为不同人群提供膳食搭配建议。'},
                {'role': 'user', 'content': prompt}
            ],
            result_format='message',
            timeout=self.timeout
        )
        
        if response.status_code != 200:
            raise Exception(f'API返回错误: {response.code} - {response.message}')
        
        return response.output.choices[0].message.content

    def _parse_response(self, response):
        """解析AI响应"""
        try:
            content = response.strip()
            
            # 提取 markdown 代码块中的 JSON
            if '```' in content:
                match = re.search(r'```(?:json)?\s*([\s\S]*?)```', content)
                if match:
                    content = match.group(1).strip()
            
            # 提取 JSON 对象
            start = content.find('{')
            end = content.rfind('}')
            if start != -1 and end != -1:
                content = content[start:end + 1]
            
            data = json.loads(content)
            
            return {
                'score': max(0, min(100, int(data.get('score', 60)))),
                'summary': str(data.get('summary', '')),
                'suggestions': list(data.get('suggestions', []))[:5],
                'good_points': list(data.get('good_points', []))[:3],
                'bad_points': list(data.get('bad_points', []))[:3]
            }
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error(f'解析AI响应失败: {e}, 响应内容: {response[:500]}')
            raise Exception('解析AI响应失败')

    def _fallback_evaluation(self, crowd_type, meal_type, foods):
        """降级评分方案"""
        categories = set(f.get('category', '') for f in foods)
        score = 60
        suggestions = []
        good_points = []
        bad_points = []
        
        # 根据食物种类评分
        if len(categories) >= 4:
            score += 20
            good_points.append('食物种类丰富，营养较均衡')
        elif len(categories) >= 3:
            score += 10
            good_points.append('食物搭配不错')
            suggestions.append('可以再增加一些食物种类')
        else:
            bad_points.append('食物种类较少')
            suggestions.append('建议增加食物种类，保证营养均衡')
        
        # 检查主食
        if 'staple' in categories:
            score += 5
            good_points.append('有主食提供能量')
        else:
            suggestions.append('建议添加主食（米饭、面条等），提供能量')
        
        # 检查蔬菜
        if 'vegetable' in categories:
            score += 5
            good_points.append('有蔬菜补充维生素')
        else:
            suggestions.append('建议添加蔬菜，补充维生素和膳食纤维')
        
        # 检查蛋白质
        protein_sources = {'meat', 'bean', 'dairy'}
        if categories & protein_sources:
            score += 5
            good_points.append('有蛋白质来源')
        else:
            suggestions.append('建议添加肉蛋类或豆制品，补充蛋白质')
        
        # 检查零食
        if 'snack' in categories:
            score -= 5
            bad_points.append('含有零食甜点')
            suggestions.append('零食甜点不宜过多，建议减少')
        
        score = max(0, min(100, score))
        
        # 生成总结
        if score >= 80:
            summary = '搭配很棒！营养均衡，继续保持！'
        elif score >= 60:
            summary = '搭配不错，稍作调整会更好！'
        else:
            summary = '还需要改进，多选择不同种类的食物哦！'
        
        return {
            'score': score,
            'summary': summary,
            'suggestions': suggestions[:3],
            'good_points': good_points[:3],
            'bad_points': bad_points[:2]
        }
