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