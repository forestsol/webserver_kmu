from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from .models import Question, Answer, Comment
from django.utils import timezone
from .forms import QuestionForm, AnswerForm, CommentForm
from django.contrib import messages


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


@login_required(login_url='common:login')
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST) # request 안에는, HTML에서 보낸, submit 버튼 누른 뒤 포장된 POST데이터가 들어있음.
        # 그 안에 데이터 전체가 딕셔너리 형태처럼 저장되어 있음.
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question' : question, 'form' : form}
    return render(request, 'pybo/question_detail.html', context)
    # 특히 content라는 변수에 들어있는 정보를 가져오기.


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


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form' : form}
    return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, "댓글수정권한이 없습니다")
        return redirect('pybo:detail', question_id=comment.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request, comment_id):
    answer = get_object_or_404(Answer, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=answer.question.id)
    else:
        form = CommentForm()
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_modify_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form' : form}
    return render(request, 'pybo/comment_form.html', context)

@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)

