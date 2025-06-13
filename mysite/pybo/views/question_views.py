from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False) # 임시 저장
            question.author = request.user
            question.create_date = timezone.now() # 사용자에게 입력받지 않은 현재 시간 데이터를 설정
            question.save() # 데이터 실제 저장
            return redirect('pybo:index')
    else:
        form = QuestionForm()  # 빈 폼 생성
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)  # 빈 폼을 템플릿에 전달

@login_required(login_url='common:login')
def question_modify(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)

    if request.method =="POST":
        form = QuestionForm(request.POST, instance=question)  # instance 기준으로 QuestionForm을 생성 -> 그 뒤에 request.POST의 값으로 덮어쓰라는 뜻.
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)  # get 했을 때, 이전에 적어뒀던 값을 instance 에 담아서 보여줌
    context = {'form' : form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

