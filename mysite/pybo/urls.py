from django.urls import path
from . import views

app_name = 'pybo'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:question_id>/', views.detail, name='detail'), # 뷰에 전달할 변수와 자료형 <int:question_id>
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('question/create/', views.question_create, name="question_create")
]
