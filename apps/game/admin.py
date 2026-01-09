from django.contrib import admin
from django.utils.html import format_html
from .models import Food, GameRecord


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'image_preview', 'description_short', 'is_active', 'sort_order']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'sort_order']
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = '图片'
    
    def description_short(self, obj):
        if obj.description:
            return obj.description[:30] + '...' if len(obj.description) > 30 else obj.description
        return '-'
    description_short.short_description = '描述'


@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'crowd_type', 'meal_type', 'health_score', 'foods_display', 'ai_model_display', 'ai_used_mock', 'created_at']
    list_filter = ['crowd_type', 'meal_type', 'ai_used_mock', 'ai_model', 'created_at']
    search_fields = ['ai_summary', 'ai_response']
    readonly_fields = [
        'crowd_type', 'meal_type', 'selected_foods', 'selected_foods_detail',
        'health_score', 'ai_summary', 'ai_suggestions', 'ai_good_points', 'ai_bad_points',
        'ai_model', 'ai_prompt', 'ai_response', 'ai_used_mock', 'ai_duration_ms', 'ai_error',
        'created_at', 'foods_detail_display', 'ai_result_display'
    ]
    list_per_page = 20
    
    fieldsets = [
        ('基本信息', {
            'fields': ['crowd_type', 'meal_type', 'created_at']
        }),
        ('食物选择', {
            'fields': ['foods_detail_display']
        }),
        ('AI评分结果', {
            'fields': ['health_score', 'ai_result_display']
        }),
        ('AI调用详情', {
            'fields': ['ai_model', 'ai_used_mock', 'ai_duration_ms', 'ai_error'],
            'classes': ['collapse']
        }),
        ('AI提示词', {
            'fields': ['ai_prompt'],
            'classes': ['collapse']
        }),
        ('AI原始响应', {
            'fields': ['ai_response'],
            'classes': ['collapse']
        }),
    ]

    def foods_display(self, obj):
        names = obj.food_names
        if names:
            return '、'.join(names[:3]) + ('...' if len(names) > 3 else '')
        return '-'
    foods_display.short_description = '选择食物'
    
    def ai_model_display(self, obj):
        return obj.ai_model or '-'
    ai_model_display.short_description = 'AI模型'
    
    def foods_detail_display(self, obj):
        if not obj.selected_foods_detail:
            return '-'
        
        html = '<table style="width:100%;border-collapse:collapse;">'
        html += '<tr style="background:#f5f5f5;"><th style="padding:8px;text-align:left;">食物</th><th style="padding:8px;text-align:left;">分类</th><th style="padding:8px;text-align:left;">描述</th></tr>'
        
        for food in obj.selected_foods_detail:
            html += f'<tr style="border-bottom:1px solid #eee;">'
            html += f'<td style="padding:8px;">{food.get("name", "")}</td>'
            html += f'<td style="padding:8px;">{food.get("category_display", "")}</td>'
            html += f'<td style="padding:8px;">{food.get("description", "") or "-"}</td>'
            html += '</tr>'
        
        html += '</table>'
        return format_html(html)
    foods_detail_display.short_description = '食物详情'
    
    def ai_result_display(self, obj):
        html = f'<div style="padding:10px;background:#f9f9f9;border-radius:8px;">'
        html += f'<p><strong>摘要：</strong>{obj.ai_summary or "-"}</p>'
        
        if obj.ai_good_points:
            html += '<p><strong>优点：</strong></p><ul>'
            for point in obj.ai_good_points:
                html += f'<li style="color:green;">{point}</li>'
            html += '</ul>'
        
        if obj.ai_bad_points:
            html += '<p><strong>不足：</strong></p><ul>'
            for point in obj.ai_bad_points:
                html += f'<li style="color:orange;">{point}</li>'
            html += '</ul>'
        
        if obj.ai_suggestions:
            html += '<p><strong>建议：</strong></p><ul>'
            for sug in obj.ai_suggestions:
                html += f'<li>{sug}</li>'
            html += '</ul>'
        
        html += '</div>'
        return format_html(html)
    ai_result_display.short_description = 'AI评价详情'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
