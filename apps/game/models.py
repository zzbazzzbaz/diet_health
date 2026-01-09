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
    
    # 基本信息
    crowd_type = models.CharField('人群类型', max_length=10, choices=CROWD_CHOICES)
    meal_type = models.CharField('用餐时段', max_length=10, choices=MEAL_CHOICES)
    selected_foods = models.JSONField('选择的食物', default=list, help_text='食物ID列表')
    selected_foods_detail = models.JSONField('食物详情', default=list, blank=True, help_text='食物完整信息')
    
    # AI 评分结果
    health_score = models.IntegerField('健康评分', default=0)
    ai_summary = models.CharField('评价摘要', max_length=100, blank=True)
    ai_suggestions = models.JSONField('改进建议', default=list, blank=True)
    ai_good_points = models.JSONField('优点', default=list, blank=True)
    ai_bad_points = models.JSONField('不足', default=list, blank=True)
    
    # AI 调用信息
    ai_model = models.CharField('AI模型', max_length=50, blank=True)
    ai_prompt = models.TextField('AI提示词', blank=True)
    ai_response = models.TextField('AI原始响应', blank=True)
    ai_used_mock = models.BooleanField('使用Mock', default=False, help_text='是否使用降级方案')
    ai_duration_ms = models.IntegerField('AI耗时(ms)', default=0)
    ai_error = models.TextField('AI错误信息', blank=True)
    
    # 时间戳
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '游戏记录'
        verbose_name_plural = '游戏记录'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_crowd_type_display()}-{self.get_meal_type_display()} ({self.health_score}分)'
    
    @property
    def food_names(self):
        """获取食物名称列表"""
        if self.selected_foods_detail:
            return [f.get('name', '') for f in self.selected_foods_detail]
        return []
