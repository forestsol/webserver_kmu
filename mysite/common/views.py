from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from common.forms import UserForm


# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')  # form.cleaned_data.get(데이터 명)메서드 : 폼에 들어있는 입력값 하나를 개별적으로 가져오는 메서드
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 위에서 가져온 개별 입력값들로 해당하는 유저를 인증하고 객체 생성
            login(request, user)  # 위에서 만든 객체로 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form':form})