from django.db import models


class Question(models.Model):
    """题目模型"""
    DIFFICULTY_CHOICES = [(1, '简单'), (2, '中等'), (3, '困难')]
    CATEGORY_CHOICES = [
        ('nutrition', '营养素知识'),
        ('matching', '食物搭配'),
        ('habit', '饮食习惯'),
        ('safety', '食品安全'),
        ('health', '健康常识'),
    ]

    content = models.TextField('题干内容')
    option_a = models.CharField('选项A', max_length=200)
    option_b = models.CharField('选项B', max_length=200)
    option_c = models.CharField('选项C', max_length=200)
    option_d = models.CharField('选项D', max_length=200)
    correct_answer = models.CharField('正确答案', max_length=1, choices=[
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
    ])
    explanation = models.TextField('答案解析')
    difficulty = models.IntegerField('难度等级', choices=DIFFICULTY_CHOICES, default=1)
    category = models.CharField('题目分类', max_length=20, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '题目'
        verbose_name_plural = '题目管理'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.get_category_display()} - {self.content[:30]}'
