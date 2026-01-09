import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Question
from apps.core.models import SystemConfig


def index(request):
    """问答首页"""
    return render(request, 'quiz/index.html')


def start(request):
    """开始答题 - 随机抽题存入session"""
    quiz_count = int(SystemConfig.get_value('QUIZ_COUNT', '5'))
    
    # 随机抽取题目
    questions = list(Question.objects.filter(is_active=True).values_list('id', flat=True))
    if len(questions) < quiz_count:
        quiz_count = len(questions)
    
    if quiz_count == 0:
        return render(request, 'quiz/index.html', {'error': '暂无题目，请联系管理员添加'})
    
    selected_ids = random.sample(questions, quiz_count)
    
    # 存入session
    request.session['quiz_questions'] = selected_ids
    request.session['quiz_answers'] = {}
    request.session['quiz_current'] = 0
    
    return redirect('quiz:question', index=0)


def question(request, index):
    """显示第N题"""
    question_ids = request.session.get('quiz_questions', [])
    answers = request.session.get('quiz_answers', {})
    
    if not question_ids:
        return redirect('quiz:index')
    
    if index < 0 or index >= len(question_ids):
        return redirect('quiz:result')
    
    question_id = question_ids[index]
    q = Question.objects.get(id=question_id)
    
    # 检查是否已答过此题
    answered = str(question_id) in answers
    user_answer = answers.get(str(question_id), {}).get('answer', '')
    is_correct = answers.get(str(question_id), {}).get('correct', False)
    
    context = {
        'question': q,
        'index': index,
        'total': len(question_ids),
        'answered': answered,
        'user_answer': user_answer,
        'is_correct': is_correct,
        'is_last': index == len(question_ids) - 1,
    }
    return render(request, 'quiz/question.html', context)


@require_POST
def submit(request):
    """提交答案 - AJAX接口"""
    import json
    data = json.loads(request.body)
    question_id = data.get('question_id')
    answer = data.get('answer')
    
    question_ids = request.session.get('quiz_questions', [])
    answers = request.session.get('quiz_answers', {})
    
    if int(question_id) not in question_ids:
        return JsonResponse({'error': '无效的题目'}, status=400)
    
    # 检查是否已答过
    if str(question_id) in answers:
        return JsonResponse({'error': '已经回答过此题'}, status=400)
    
    q = Question.objects.get(id=question_id)
    is_correct = answer == q.correct_answer
    
    # 记录答案
    answers[str(question_id)] = {
        'answer': answer,
        'correct': is_correct
    }
    request.session['quiz_answers'] = answers
    request.session.modified = True
    
    return JsonResponse({
        'correct': is_correct,
        'correct_answer': q.correct_answer,
        'explanation': q.explanation
    })


def result(request):
    """显示答题结果"""
    question_ids = request.session.get('quiz_questions', [])
    answers = request.session.get('quiz_answers', {})
    
    if not question_ids:
        return redirect('quiz:index')
    
    total = len(question_ids)
    correct_count = sum(1 for a in answers.values() if a.get('correct'))
    score = int(correct_count / total * 100) if total > 0 else 0
    
    # 评价
    if score >= 80:
        comment = '太棒了！你是饮食健康小达人！🌟'
    elif score >= 60:
        comment = '不错哦！继续学习会更棒！💪'
    else:
        comment = '加油！多了解健康饮食知识吧！📚'
    
    context = {
        'total': total,
        'correct_count': correct_count,
        'score': score,
        'comment': comment,
    }
    
    # 清除session
    request.session.pop('quiz_questions', None)
    request.session.pop('quiz_answers', None)
    request.session.pop('quiz_current', None)
    
    return render(request, 'quiz/result.html', context)
