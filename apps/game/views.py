from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import FoodCategory, Food, GameRecord
from apps.core.models import SystemConfig
from apps.core.ai_service import AIService


def index(request):
    """游戏首页"""
    request.session.pop('game_crowd', None)
    request.session.pop('game_meal', None)
    request.session.pop('game_foods', None)
    return render(request, 'game/index.html')


def select_crowd(request):
    """选择人群"""
    if request.method == 'POST':
        crowd = request.POST.get('crowd')
        if crowd in ['child', 'adult', 'elder']:
            request.session['game_crowd'] = crowd
            return redirect('game:meal')
    return render(request, 'game/select_crowd.html')


def select_meal(request):
    """选择用餐时段"""
    if not request.session.get('game_crowd'):
        return redirect('game:crowd')
    
    if request.method == 'POST':
        meal = request.POST.get('meal')
        if meal in ['breakfast', 'lunch', 'dinner']:
            request.session['game_meal'] = meal
            return redirect('game:food')
    
    return render(request, 'game/select_meal.html')


def select_food(request):
    """食物选择页面"""
    if not request.session.get('game_crowd') or not request.session.get('game_meal'):
        return redirect('game:crowd')
    
    max_foods = int(SystemConfig.get_value('MAX_FOODS', '8'))
    categories = FoodCategory.objects.filter(is_active=True)
    
    context = {
        'categories': categories,
        'max_foods': max_foods,
        'crowd': request.session.get('game_crowd'),
        'meal': request.session.get('game_meal'),
    }
    return render(request, 'game/select_food.html', context)


def get_foods(request):
    """获取食物列表 - JSON API"""
    category_id = request.GET.get('category', '')
    foods = Food.objects.filter(is_active=True).select_related('category')
    
    if category_id:
        foods = foods.filter(category_id=category_id)
    
    data = [{
        'id': f.id,
        'name': f.name,
        'category': f.category.code,
        'category_display': f.category.name,
        'description': f.description or '',
        'image': f.image.url if f.image else '',
    } for f in foods]
    
    return JsonResponse({'foods': data})


@require_POST
def evaluate(request):
    """提交评分"""
    import json
    
    crowd = request.session.get('game_crowd')
    meal = request.session.get('game_meal')
    
    if not crowd or not meal:
        return JsonResponse({'error': '请先选择人群和用餐时段'}, status=400)
    
    data = json.loads(request.body)
    food_ids = data.get('foods', [])
    
    if not food_ids:
        return JsonResponse({'error': '请至少选择一种食物'}, status=400)
    
    # 获取食物完整信息
    foods_qs = Food.objects.filter(id__in=food_ids).select_related('category')
    
    foods_data = [{
        'id': f.id,
        'name': f.name,
        'category': f.category.code,
        'category_display': f.category.name,
        'description': f.description,
    } for f in foods_qs]
    
    food_names = [f['name'] for f in foods_data]
    
    # 调用 AI 服务评分
    ai_service = AIService()
    result = ai_service.evaluate_meal(crowd, meal, foods_data)
    
    # 存储到session供结果页使用
    request.session['game_foods'] = food_ids
    request.session['game_food_names'] = food_names
    request.session['game_foods_data'] = foods_data
    request.session['game_result'] = result
    
    return JsonResponse({'success': True, 'redirect': '/game/result/'})


def result(request):
    """显示评分结果"""
    crowd = request.session.get('game_crowd')
    meal = request.session.get('game_meal')
    food_ids = request.session.get('game_foods', [])
    food_names = request.session.get('game_food_names', [])
    foods_data = request.session.get('game_foods_data', [])
    ai_result = request.session.get('game_result', {})
    
    if not crowd or not meal or not food_ids:
        return redirect('game:index')
    
    # 提取 AI 元信息
    meta = ai_result.pop('_meta', {})
    
    # 保存游戏记录
    GameRecord.objects.create(
        crowd_type=crowd,
        meal_type=meal,
        selected_foods=food_ids,
        selected_foods_detail=foods_data,
        health_score=ai_result.get('score', 0),
        ai_summary=ai_result.get('summary', ''),
        ai_suggestions=ai_result.get('suggestions', []),
        ai_good_points=ai_result.get('good_points', []),
        ai_bad_points=ai_result.get('bad_points', []),
        ai_model=meta.get('model', ''),
        ai_prompt=meta.get('prompt', ''),
        ai_response=meta.get('response', ''),
        ai_used_mock=meta.get('used_mock', False),
        ai_duration_ms=meta.get('duration_ms', 0),
        ai_error=meta.get('error', ''),
    )
    
    # 人群和餐次显示
    crowd_display = dict(GameRecord.CROWD_CHOICES).get(crowd, '')
    meal_display = dict(GameRecord.MEAL_CHOICES).get(meal, '')
    
    context = {
        'score': ai_result.get('score', 0),
        'summary': ai_result.get('summary', ''),
        'suggestions': ai_result.get('suggestions', []),
        'good_points': ai_result.get('good_points', []),
        'bad_points': ai_result.get('bad_points', []),
        'food_names': food_names,
        'crowd': crowd_display,
        'meal': meal_display,
    }
    
    # 清除session
    request.session.pop('game_crowd', None)
    request.session.pop('game_meal', None)
    request.session.pop('game_foods', None)
    request.session.pop('game_food_names', None)
    request.session.pop('game_foods_data', None)
    request.session.pop('game_result', None)
    
    return render(request, 'game/result.html', context)
