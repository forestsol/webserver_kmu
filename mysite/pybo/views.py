from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from django.utils import timezone
from .forms import QuestionForm, AnswerForm


def index(request):
    page = request.GET.get('page', '1')  # 페이지
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    # context = {'question_list' : question_list} # context라는 딕셔너리를 만들기. # context = {'question_list': [질문1, 질문2, 질문3, ...]}
    context = {'question_list': page_obj}

    return render(request, 'pybo/question_list.html', context) # render는 (request, 템플릿경로, 딕셔너리) 를 받아야함.

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question' : question}
    return render(request, 'pybo/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST) # request 안에는, HTML에서 보낸, submit 버튼 누른 뒤 포장된 POST데이터가 들어있음.
        # 그 안에 데이터 전체가 딕셔너리 형태처럼 저장되어 있음.
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only Post is possible.')
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)
    # 특히 content라는 변수에 들어있는 정보를 가져오기.


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # 임시 저장
            question.create_date = timezone.now() # 사용자에게 입력받지 않은 현재 시간 데이터를 설정
            question.save() # 데이터 실제 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm()  # 빈 폼 생성
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)  # 빈 폼을 템플릿에 전달
