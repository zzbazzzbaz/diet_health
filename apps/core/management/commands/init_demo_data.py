from django.core.management.base import BaseCommand
from apps.quiz.models import Question
from apps.game.models import Food


class Command(BaseCommand):
    help = '初始化示例数据'

    def handle(self, *args, **options):
        self.init_questions()
        self.init_foods()
        self.stdout.write(self.style.SUCCESS('示例数据初始化完成！'))

    def init_questions(self):
        questions = [
            {
                'content': '以下哪种食物富含维生素C？',
                'option_a': '米饭',
                'option_b': '猪肉',
                'option_c': '橙子',
                'option_d': '牛奶',
                'correct_answer': 'C',
                'explanation': '橙子等柑橘类水果富含维生素C，有助于增强免疫力。',
                'category': 'nutrition',
                'difficulty': 1,
            },
            {
                'content': '早餐最好在起床后多长时间内吃？',
                'option_a': '30分钟内',
                'option_b': '1小时内',
                'option_c': '2小时内',
                'option_d': '随时都可以',
                'correct_answer': 'B',
                'explanation': '建议起床后1小时内吃早餐，这样有助于启动新陈代谢。',
                'category': 'habit',
                'difficulty': 1,
            },
            {
                'content': '以下哪种搭配更有利于钙的吸收？',
                'option_a': '牛奶+菠菜',
                'option_b': '牛奶+鸡蛋',
                'option_c': '豆腐+海带',
                'option_d': '酸奶+水果',
                'correct_answer': 'D',
                'explanation': '酸奶中的乳酸和水果中的维生素C都有助于钙的吸收。菠菜中的草酸会影响钙吸收。',
                'category': 'matching',
                'difficulty': 2,
            },
            {
                'content': '每天应该喝多少水比较合适？',
                'option_a': '500毫升',
                'option_b': '1000毫升',
                'option_c': '1500-2000毫升',
                'option_d': '3000毫升以上',
                'correct_answer': 'C',
                'explanation': '成年人每天建议饮水1500-2000毫升，约7-8杯水。',
                'category': 'health',
                'difficulty': 1,
            },
            {
                'content': '以下哪种食物不适合空腹食用？',
                'option_a': '面包',
                'option_b': '香蕉',
                'option_c': '牛奶',
                'option_d': '柿子',
                'correct_answer': 'D',
                'explanation': '柿子含有大量鞣酸，空腹食用容易与胃酸结合形成结石。',
                'category': 'safety',
                'difficulty': 2,
            },
            {
                'content': '蛋白质的主要作用是什么？',
                'option_a': '提供能量',
                'option_b': '构建和修复身体组织',
                'option_c': '帮助消化',
                'option_d': '调节体温',
                'correct_answer': 'B',
                'explanation': '蛋白质是构建和修复身体组织的重要营养素，是生命的基础物质。',
                'category': 'nutrition',
                'difficulty': 1,
            },
            {
                'content': '以下哪种烹饪方式最健康？',
                'option_a': '油炸',
                'option_b': '烧烤',
                'option_c': '清蒸',
                'option_d': '烟熏',
                'correct_answer': 'C',
                'explanation': '清蒸能最大程度保留食物的营养成分，且不会产生有害物质。',
                'category': 'habit',
                'difficulty': 1,
            },
            {
                'content': '晚餐应该在睡前多长时间吃完？',
                'option_a': '30分钟',
                'option_b': '1小时',
                'option_c': '2-3小时',
                'option_d': '4小时以上',
                'correct_answer': 'C',
                'explanation': '晚餐建议在睡前2-3小时吃完，给胃足够的消化时间。',
                'category': 'habit',
                'difficulty': 1,
            },
            {
                'content': '以下哪种食物是优质蛋白质来源？',
                'option_a': '白菜',
                'option_b': '鸡蛋',
                'option_c': '苹果',
                'option_d': '米饭',
                'correct_answer': 'B',
                'explanation': '鸡蛋含有完整的氨基酸，是优质蛋白质的代表食物。',
                'category': 'nutrition',
                'difficulty': 1,
            },
            {
                'content': '食品保质期过了一天还能吃吗？',
                'option_a': '可以，没关系',
                'option_b': '看情况，闻一闻',
                'option_c': '不建议食用',
                'option_d': '加热后可以吃',
                'correct_answer': 'C',
                'explanation': '过期食品可能已经变质，即使外观正常也不建议食用，以免影响健康。',
                'category': 'safety',
                'difficulty': 1,
            },
        ]

        for q_data in questions:
            Question.objects.get_or_create(
                content=q_data['content'],
                defaults=q_data
            )
        self.stdout.write(f'创建了 {len(questions)} 道题目')

    def init_foods(self):
        foods = [
            # 主食类
            {'name': '米饭', 'category': 'staple', 'sort_order': 10, 'description': '富含碳水化合物，提供能量'},
            {'name': '馒头', 'category': 'staple', 'sort_order': 9, 'description': '面粉发酵制成，易消化'},
            {'name': '面条', 'category': 'staple', 'sort_order': 8, 'description': '碳水化合物来源，饱腹感强'},
            {'name': '面包', 'category': 'staple', 'sort_order': 7, 'description': '方便快捷的主食选择'},
            {'name': '玉米', 'category': 'staple', 'sort_order': 6, 'description': '粗粮，富含膳食纤维'},
            # 肉蛋类
            {'name': '鸡蛋', 'category': 'meat', 'sort_order': 10, 'description': '优质蛋白质，营养全面'},
            {'name': '鸡肉', 'category': 'meat', 'sort_order': 9, 'description': '低脂高蛋白，易消化'},
            {'name': '猪肉', 'category': 'meat', 'sort_order': 8, 'description': '富含蛋白质和B族维生素'},
            {'name': '牛肉', 'category': 'meat', 'sort_order': 7, 'description': '高蛋白，富含铁和锌'},
            {'name': '鱼肉', 'category': 'meat', 'sort_order': 6, 'description': '优质蛋白，富含DHA'},
            # 蔬菜类
            {'name': '西红柿', 'category': 'vegetable', 'sort_order': 10, 'description': '富含维生素C和番茄红素'},
            {'name': '黄瓜', 'category': 'vegetable', 'sort_order': 9, 'description': '低热量，补充水分'},
            {'name': '白菜', 'category': 'vegetable', 'sort_order': 8, 'description': '富含维生素和膳食纤维'},
            {'name': '胡萝卜', 'category': 'vegetable', 'sort_order': 7, 'description': '富含胡萝卜素，护眼'},
            {'name': '菠菜', 'category': 'vegetable', 'sort_order': 6, 'description': '富含铁和叶酸'},
            # 水果类
            {'name': '苹果', 'category': 'fruit', 'sort_order': 10, 'description': '富含果胶和维生素'},
            {'name': '香蕉', 'category': 'fruit', 'sort_order': 9, 'description': '富含钾，补充能量'},
            {'name': '橙子', 'category': 'fruit', 'sort_order': 8, 'description': '维生素C含量高'},
            {'name': '葡萄', 'category': 'fruit', 'sort_order': 7, 'description': '富含花青素，抗氧化'},
            {'name': '西瓜', 'category': 'fruit', 'sort_order': 6, 'description': '水分多，消暑解渴'},
            # 奶制品
            {'name': '牛奶', 'category': 'dairy', 'sort_order': 10, 'description': '富含钙和优质蛋白'},
            {'name': '酸奶', 'category': 'dairy', 'sort_order': 9, 'description': '含益生菌，助消化'},
            {'name': '奶酪', 'category': 'dairy', 'sort_order': 8, 'description': '钙含量高，营养浓缩'},
            # 豆制品
            {'name': '豆腐', 'category': 'bean', 'sort_order': 10, 'description': '植物蛋白，低脂健康'},
            {'name': '豆浆', 'category': 'bean', 'sort_order': 9, 'description': '植物蛋白饮品'},
            {'name': '豆干', 'category': 'bean', 'sort_order': 8, 'description': '蛋白质含量高'},
            # 饮品类
            {'name': '白开水', 'category': 'drink', 'sort_order': 10, 'description': '最健康的饮品'},
            {'name': '绿茶', 'category': 'drink', 'sort_order': 9, 'description': '含茶多酚，抗氧化'},
            {'name': '果汁', 'category': 'drink', 'sort_order': 8, 'description': '含维生素，但糖分较高'},
            # 零食甜点
            {'name': '饼干', 'category': 'snack', 'sort_order': 5, 'description': '高糖高油，少吃为宜'},
            {'name': '蛋糕', 'category': 'snack', 'sort_order': 4, 'description': '高糖高脂，偶尔食用'},
            {'name': '薯片', 'category': 'snack', 'sort_order': 3, 'description': '高盐高油，不宜多吃'},
            {'name': '糖果', 'category': 'snack', 'sort_order': 2, 'description': '高糖，影响牙齿健康'},
        ]

        for f_data in foods:
            obj, created = Food.objects.update_or_create(
                name=f_data['name'],
                defaults=f_data
            )
            status = '创建' if created else '更新'
        self.stdout.write(f'处理了 {len(foods)} 种食物')
