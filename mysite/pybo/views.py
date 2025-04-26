from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer
from django.utils import timezone

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list} # context라는 딕셔너리를 만들기. # context = {'question_list': [질문1, 질문2, 질문3, ...]}
    return render(request, 'pybo/question_list.html', context) # render는 (request, 템플릿경로, 딕셔너리) 를 받아야함.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # request 안에는, Form에서 보낸 POST데이터가 들어있음.
    # 그 안에 데이터 전체가 딕셔너리 형태처럼 저장되어 있음.
    # 특히 content라는 변수에 들어있는 정보를 가져오기.
    return redirect('pybo:detail', question_id=question.id)

