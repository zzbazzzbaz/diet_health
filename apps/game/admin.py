from django.contrib import admin
from django.utils.html import format_html
from .models import Food, GameRecord


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'image_preview', 'is_active', 'sort_order']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'sort_order']
    list_per_page = 20

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;"/>', obj.image.url)
        return '-'
    image_preview.short_description = '图片预览'


@admin.register(GameRecord)
class GameRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'crowd_type', 'meal_type', 'health_score', 'foods_count', 'created_at']
    list_filter = ['crowd_type', 'meal_type', 'created_at']
    readonly_fields = ['crowd_type', 'meal_type', 'selected_foods', 'health_score', 'ai_evaluation', 'created_at']
    list_per_page = 20

    def foods_count(self, obj):
        return len(obj.selected_foods) if obj.selected_foods else 0
    foods_count.short_description = '食物数量'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
