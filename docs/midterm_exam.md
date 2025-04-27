### 1. INSTALLED_APPS에 앱 명시하는 법
- '앱이름.apps.앱이름Config' 라고 적기
```python
INSTALLED_APPS = [
    'pybo.apps.PyboConfig',
    # ...
]
```

### 2. makemigration은 변경사항 반영한 작업파일 생성용
### 3. migrate는 DB에 실제 테이블 생성하는 작업
### 4. python manage.py shell 로 셸 킬 수 있음
- 셸에서 인터프리터로 한줄한줄 실행하는 것임.

```python
>>> from pybo.models import Question, Answer
>>> from django.utils import timezone
>>> q = Question(subject='pybo가 무엇인가요?', content='pybo에 대해서 알고 싶습니다.', create_date=timezone.now())
>>> q.save() # 이러면 쿼리 하나 저장

>>> Question.objects.all() # 저장된 모든 쿼리 조회

>>> Question.objects.filter(id=1) # 다건조회 # id가 1인 모든 쿼리 조회 (쿼리셋 반환)
# 없으면 빈 쿼리셋 반환

>>> Question.objects.get(id=1) # 단일조회 # id가 1인 쿼리 조회 (id가 유일한 값이라면 모델 객체 하나 리턴)
# 없으면 오류뜸

>>> Question.objects.filter(subject__contains='pybo') # 특정 필드에 어떤 값이 포함(contains)된 쿼리 필터링
# 없으면 빈 쿼리셋 반환

# 수정하려면?
>>> q = Question.objects.get(id=1) # q라는 변수에 id 1인 쿼리를 복사해서 넣어둠
# get 사용해야 함 쿼리셋 넣으면 안됨.
>>> q.subject = 'Django Model Question' # q안에 subject를 수정
>>> q.save() # 저장해줌

# 삭제하려면?
>>> q.delete() # 아까 변수 할당한거로 지우면 됨.

# 역방향 접근
# foreign key 로 연결되어있는 상태에서, (1 : 다수) 인 상황이 생길거아님? 그때 1인 쿼리쪽의 객체를 이용해서, 연결된 다수의 데이터를 조회하는 방법?
>>> q.answer_set.all()
# question에는 answer_set이라는 필드가 없지만 사용가능, 이러면 Question 쿼리에 연결된 모든 Answer 쿼리를 조회할 수 있다.
```

- ctrl+z 또는 quit()로 셸 종료

### 5. 템플릿(templates)과 폼(form)
- '템플릿'은 유저에게 보이는 화면
- '폼'은 사용자 입력을 받는 양식(이렇게 입력하기를 정해두는 거)

### 6. 템플릿 태그
1. 분기
```html
{% if 조건문1 %}
    <p> 실행문1 </p>
{% elif 조건문2 %}
    <p> 실행문2 </p>
{% else %}
    <p> 조건1, 2에 해당하지 않을 때 실행문 </p>
{% endif %}
```
2. 반복
```html
{% for item in list %}
    <p>순서 : {{ forloop.counter }} </p> <!--forloop라는 카운터 객체 사용 가능 1부터 자동으로 세어줌-->
    <p>{{item}}</p>
```
| forloop 속성       |설명|
|------------------|---|
| forloop.counter  |	루프 내의 순서로 1부터 표시
| forloop.counter0 |	루프 내의 순서로 0부터 표시
| forloop.first    |	루프의 첫 번째 순서인 경우 True
| forloop.last     |	루프의 마지막 순서인 경우 True

3. 객체 출력
```html
{{ 객체.속성 }} <!--예 : {{question.id}}-->
```
---
## View
### 1) 기본 뷰 구조
```python
def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list' : question_list} 
    # context라는 딕셔너리를 만들기. # context = {'question_list': [질문1, 질문2, 질문3, ...]}
    return render(request, 'pybo/question_list.html', context) 
    # render는 (request, 템플릿경로, 딕셔너리) 를 받아야함.
    # 템플릿에서는 이 딕셔너리를 사용해서 뭔가 함. 리스트 형태면 리스트 꺼내서 반복해서 뿌리겠지?
```
### 2) get_object_or_404
```python
question = Question.objects.get(id=question_id)
# 이걸 아래와 같이 수정하면
question = get_object_or_404(Question, pk=question_id)
# get할 때 뭔가 없으면 500 에러가 아닌 404 에러를 띄움
```
### 3) 제네릭 뷰는 복잡한 케이스에서 더 어려워질 수 있음. 상황에 따라 주의하여 사용할 것.
### 4) redirect()
```python
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)  # <-- 이거
```
- redirect(URL 패턴 이름, URL 만들 때 필요한 변수값(kargs))
- 위 예시
  - pybo앱의 detail별칭 달린 URL에
  - question_id 변수가 필요하므로 같이 넘겨주기

---
### URL 네임스페이스 (app별 네임스페이스)
서로 다른 app에서 같은 URL 별칭 사용 방지
```python
#urls.py
app_name = 'pybo'
```

### URL 하드코딩을 URL 별칭으로
```html
<li><a href="/pybo/{{question.id}}/">{{question.subject}}</a></li>

<!--path('<int:question_id>/', views.detail, name='detail')-->
<!--app_name:url_name-->

<li><a href="{% url 'pybo:detail' question.id %}">{{question.subject}}</a></li>
```

---
## Form
- 페이지 요청 시(POST) 뭔가 입력해서 주는 경우가 있음.
- 그 때 전달받는 파라미터들을 쉽게 관리하기 위해 쓰는 클래스
- 검증용으로도 씀(DRF에서는 시리얼라이저로 바뀜)
  - 필수로 줘야하는 파라미터가 누락되지 않았는지,
  - 적절한 형태로 줬는지 검증
- HTML을 자동으로 생성해주기도 함
- 폼에 연결된 모델을 이용해 데이터를 저장하기도 함
```html
<h1>{{question.subject}}</h1>

<div>
  {{question.content}}
</div>

<form action="{% url 'pybo:answer_create' question.id %}" method = "post">
  {% csrf_token %}  <!--POST 요청 시 csrf_token 안달면 오류-->
  <textarea name="content" id="content" rows="15"></textarea>  <!--텍스트를 입력하는 텍스트 창-->
  <input type="submit" value="답변등록">  <!--답변 등록 버튼-->
</form>
```
- 폼에서 content라는 변수에 내용을 담아줌
- name이 view에서 쓰는 변수, id가 html에서 사용할 때 쓰는 변수임
  - textarea 에서 정해주는 것

```python
def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())  
    # request 안에는, Form에서 보낸 POST데이터가 들어있음. 
    # 그 안에 데이터 전체가 딕셔너리 형태처럼 저장되어 있음. 
    # 특히 content라는 변수에 들어있는 정보를 가져오기.
```
---
## Django : Front
### 1) Template
- HTML 화면을 만드는 역할
- ex : 질문 목록, 글, 상세 페이지
### 2) static
- CSS/JS/이미지로 화면을 꾸미는 역할
- ex : 배경색, 버튼 애니메이션, 폰트
- 이때, css는 꾸미는 역할, js는 화면을 움직이고, 반응하게 만드는 역할임.

항목 | 템플릿(HTML) | JavaScript(JS)
---|---|---
본질 | 정적인 구조를 만듦 (페이지 뼈대) | 동적인 동작을 만듦 (페이지를 움직이게)
하는 일 | 페이지를 "보여주기" | 페이지를 "반응하게 하기"
서버와 관계 | 서버가 만들어서 보내줌 (Django가 render) | 브라우저에서 작동 (서버 필요 없음)
사용 타이밍 | 페이지 열 때 바로 표시 | 사용자가 액션할 때 실행 (클릭, 스크롤 등)
---
### 3) 표준 HTML 구조
- 표준 HTML 문서의 구조는 html, head, body 엘리먼트가 있어야 함.
- 엘리먼트란 "하나의 완성된 HTML 덩어리"를 뜻함.
- head 엘리먼트 안에는 meta, title 엘리먼트 등이 포함되어야 한다.
  - css 파일 링크는 head 엘리먼트 안에 위치해야 한다.

### 4) 템플릿 상속
- 보통 body 엘리먼트 내부만 바뀌고 나머지 엘리먼트는 모든 페이지가 비슷한 경우가 많은듯(위에 메뉴 바가 같은 느낌?)
- 그래서 매번 똑같이 반복되는 부분을 기본 템플릿으로 만듦
- 개별 페이지는 기본 템플릿을 상속 받은 뒤 필요한 부분(body)만 수정해서 씀

---
## POST동작과정
- 하나의 view를 GET동작과 POST 동작으로 나누어둠.
### 0) POST가 동작하기 전에 폼에 데이터를 입력해 둬야한다
- POST는 데이터가 들어있는 완성된 폼을 전달받아 Django 서버로 전달하는 행동임
- 그러니까 이미 데이터가 들어있는 폼이 완성되어야 한다는 뜻 
- 데이터가 들어있지 않은 폼은 get을 통해 클라이언트에게 이미 전달되어 있어야 함.
  - view의 GET작동부가 작동하는 것임.
- 클라이언트는 그 빈 폼에 데이터를 채워 넣음.
- 채워넣어야 할 데이터 유형은 forms.py 에서 정함
- 화면에 보면 어떤 부분에 넣어야 하는지는 form method="post" ~ /form 로 정해두는 것.

### 1) 사용자가 POST를 수행함
- 사용자가 html의 form method="post" ~ /form 부분에 데이터를 입력한다
- submit 버튼을 누른다.
- form method="post" ~ /form 부분이 request로 포장된다.
- request 데이터를 POST한다(Django 서버로 보낸다)

### 2) 서버가 POST 요청을 처리함
- view의 POST 작동부가 작동함.
- request에 들어있는 데이터들을 꺼내서 views에 적힌 로직대로 행동함.
- 이때 form 검증도 함.
  - 채울꺼 채웠는지
  - 이상하게 하진 않았는지
- 검증에 통과하면
  - 보통 저장
  - 리다이렉트해서 POST 창에서 벗어남
- 검증에 실패하면
  - 다시 빈 폼을 렌더링하여 올바르게 입력하도록 유도.

---
### Paginator
```python
def index(request):
    page = request.GET.get('page', '1')  # request.GET : GET 요청에 포함된 쿼리 파라미터들을 의미
    # .get(키, 기본값)메서드 : 쿼리 파라미터에서 키에 해당하는 값을 가져옴. 없으면 기본값 부여.
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10)   # Paginator(리스트, 한 페이지에 보여줄 갯수)메서드 
    page_obj = paginator.get_page(page)  # .get_page(페이지 번호)메서드 
    
    context = {'question_list' : page_obj}
    return render(request, 'pybo/question_list.html', context)
```
- Paginator(리스트, 한 페이지에 보여줄 갯수)메서드
  - : 리스트 형태(리스트, 쿼리셋, 등 리스트처럼 동작하는 것)의 데이터를 페이지 단위로 나누는 메서드임
  - 입력은 위에 두개
  - 출력은 Paginator객체를 반환함
- Paginator객체.get_page(페이지번호)메서드
  - : 특정 페이지 번호에 해당하는 Page 데이터 묶음을 반환해줌
  - 입력은 페이지 번호
  - 출력은 해당 페이지에 들어있는 객체 묶음

---

### django.contrib.auth
```python
# urls.py 에서 바로 auth_views의 'LoginView'로 연결.
path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
```

- django.contrib.auth 인증할 때 username과 password 항목을 넣어서 보내줘야함.
- django.contrib.auth는 로그인에 성공하면 기본적으로 /accounts/profile/이라는 URL로 리다이렉트함.
  - settings.py 에서 **LOGIN_REDIRECT_URL = '/'** 로 설정을 바꿀 수 있음