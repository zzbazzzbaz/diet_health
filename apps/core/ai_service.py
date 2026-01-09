"""
AI 服务封装 - 阿里百炼 DashScope
"""
import json
import logging
from dashscope import Generation
from .models import SystemConfig

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, use_mock=False):
        self.api_key = SystemConfig.get_value('AI_API_KEY', '')
        self.model = SystemConfig.get_value('AI_MODEL', 'deepseek-v3')
        self.timeout = 30
        self.max_retries = 3
        self.use_mock = use_mock or SystemConfig.get_value('AI_USE_MOCK', 'false').lower() == 'true'

    def evaluate_meal(self, crowd_type, meal_type, foods):
        """评价膳食搭配"""
        if self.use_mock or not self.api_key:
            logger.info('使用Mock数据评分')
            return self._fallback_evaluation(crowd_type, meal_type, foods)
        
        logger.info(f'调用AI服务: model={self.model}, foods={foods}')
        
        prompt = self._build_prompt(crowd_type, meal_type, foods)
        
        for attempt in range(self.max_retries):
            try:
                response = self._call_api(prompt)
                return self._parse_response(response)
            except Exception as e:
                logger.error(f'AI调用失败 (尝试 {attempt + 1}/{self.max_retries}): {e}')
                if attempt == self.max_retries - 1:
                    return self._fallback_evaluation(crowd_type, meal_type, foods)
        
        return self._fallback_evaluation(crowd_type, meal_type, foods)

    def _build_prompt(self, crowd_type, meal_type, foods):
        """构建提示词"""
        crowd_map = {'child': '6-12岁儿童', 'adult': '成年人', 'elder': '60岁以上老年人'}
        meal_map = {'breakfast': '早餐', 'lunch': '午餐', 'dinner': '晚餐'}
        
        crowd_name = crowd_map.get(crowd_type, '成年人')
        meal_name = meal_map.get(meal_type, '午餐')
        food_list = '、'.join(foods)
        
        prompt = f"""你是一位专业的营养师，请评价以下膳食搭配。

用餐人群：{crowd_name}
用餐时段：{meal_name}
选择的食物：{food_list}

请从以下几个方面进行评价：
1. 营养均衡性（是否包含主食、蛋白质、蔬菜等）
2. 针对该人群的适宜性
3. 针对该用餐时段的合理性

请以JSON格式返回，格式如下：
{{
    "score": 0-100的整数分数,
    "summary": "一句话总结评价",
    "suggestions": ["建议1", "建议2", "建议3"],
    "good_points": ["优点1", "优点2"],
    "bad_points": ["不足1", "不足2"]
}}

注意：
- 评分要客观合理，不要过于严格或宽松
- 建议要具体、有针对性、适合{crowd_name}理解
- 语言要友好、鼓励性的
- 只返回JSON，不要有其他内容"""
        
        return prompt

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
            # 尝试提取JSON
            content = response.strip()
            if content.startswith('```'):
                content = content.split('```')[1]
                if content.startswith('json'):
                    content = content[4:]
            
            data = json.loads(content)
            
            return {
                'score': max(0, min(100, int(data.get('score', 60)))),
                'summary': data.get('summary', ''),
                'suggestions': data.get('suggestions', []),
                'good_points': data.get('good_points', []),
                'bad_points': data.get('bad_points', [])
            }
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f'解析AI响应失败: {e}, 响应内容: {response}')
            raise Exception('解析AI响应失败')

    def _fallback_evaluation(self, crowd_type, meal_type, foods):
        """降级评分方案"""
        food_categories = self._categorize_foods(foods)
        score = 60
        suggestions = []
        good_points = []
        bad_points = []
        
        # 根据食物种类评分
        if len(food_categories) >= 4:
            score += 20
            good_points.append('食物种类丰富，营养较均衡')
        elif len(food_categories) >= 3:
            score += 10
            good_points.append('食物搭配不错')
            suggestions.append('可以再增加一些食物种类')
        else:
            bad_points.append('食物种类较少')
            suggestions.append('建议增加食物种类，保证营养均衡')
        
        # 检查主食
        if 'staple' in food_categories:
            score += 5
            good_points.append('有主食提供能量')
        else:
            suggestions.append('建议添加主食（米饭、面条等），提供能量')
        
        # 检查蔬菜
        if 'vegetable' in food_categories:
            score += 5
            good_points.append('有蔬菜补充维生素')
        else:
            suggestions.append('建议添加蔬菜，补充维生素和膳食纤维')
        
        # 检查蛋白质
        protein_sources = {'meat', 'bean', 'dairy'}
        if food_categories & protein_sources:
            score += 5
            good_points.append('有蛋白质来源')
        else:
            suggestions.append('建议添加肉蛋类或豆制品，补充蛋白质')
        
        # 检查零食
        if 'snack' in food_categories:
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

    def _categorize_foods(self, food_names):
        """根据食物名称推断分类"""
        from apps.game.models import Food
        
        categories = set()
        for name in food_names:
            try:
                food = Food.objects.get(name=name)
                categories.add(food.category)
            except Food.DoesNotExist:
                pass
        
        return categories
