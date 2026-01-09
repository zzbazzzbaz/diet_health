from django.db import models


class Food(models.Model):
    """食物模型"""
    CATEGORY_CHOICES = [
        ('staple', '主食类'),
        ('meat', '肉蛋类'),
        ('vegetable', '蔬菜类'),
        ('fruit', '水果类'),
        ('dairy', '奶制品'),
        ('bean', '豆制品'),
        ('drink', '饮品类'),
        ('snack', '零食甜点'),
    ]

    name = models.CharField('食物名称', max_length=50)
    category = models.CharField('食物分类', max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField('食物图片', upload_to='foods/', blank=True)
    description = models.TextField('食物描述', blank=True)
    is_active = models.BooleanField('是否启用', default=True)
    sort_order = models.IntegerField('排序权重', default=0)

    class Meta:
        verbose_name = '食物'
        verbose_name_plural = '食物管理'
        ordering = ['category', '-sort_order', 'name']

    def __str__(self):
        return f'{self.get_category_display()} - {self.name}'


class GameRecord(models.Model):
    """游戏记录模型"""
    CROWD_CHOICES = [('child', '小孩'), ('adult', '成人'), ('elder', '老人')]
    MEAL_CHOICES = [('breakfast', '早餐'), ('lunch', '午餐'), ('dinner', '晚餐')]

    crowd_type = models.CharField('人群类型', max_length=10, choices=CROWD_CHOICES)
    meal_type = models.CharField('用餐时段', max_length=10, choices=MEAL_CHOICES)
    selected_foods = models.JSONField('选择的食物', default=list)
    health_score = models.IntegerField('健康评分', default=0)
    ai_evaluation = models.TextField('AI评价内容', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '游戏记录'
        verbose_name_plural = '游戏记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_crowd_type_display()}-{self.get_meal_type_display()} ({self.health_score}分)'
