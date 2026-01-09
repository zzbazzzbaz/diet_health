from django.contrib import admin
from .models import Question


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_short', 'category', 'difficulty', 'correct_answer', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty', 'is_active']
    search_fields = ['content', 'explanation']
    list_editable = ['is_active']
    list_per_page = 20
    
    fieldsets = [
        ('题目内容', {'fields': ['content', 'category', 'difficulty']}),
        ('选项设置', {'fields': ['option_a', 'option_b', 'option_c', 'option_d']}),
        ('答案解析', {'fields': ['correct_answer', 'explanation']}),
        ('状态', {'fields': ['is_active']}),
    ]

    def content_short(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_short.short_description = '题干'
