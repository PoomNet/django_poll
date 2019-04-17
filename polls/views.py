from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from django.template.defaultfilters import length

from .form import PollForm, CommentForm, ChangePass, RegisterForm
from .models import Poll, Comment, Profile
from .models import Question
from .models import Answer

# poll_list = [
#         {
# 		'id': 1,
# 		'title': 'การสอนวิชา Web Programming',
# 		'questions': [
# 			{
# 				'text': 'อาจารย์บัณฑิตสอนน่าเบื่อไหม',
# 				'choices': [
# 					{'text': 'น่าเบื่อมาก', 'value': 1},
# 					{'text': 'ค่อนข้างน่าเบื่อ', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างสนุก', 'value': 4},
# 					{'text': 'สนุกมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'นักศึกษาเรียนรู้เรื่องหรือไม่',
# 				'choices': [
# 					{'text': 'ไม่รู้เรื่องเลย', 'value': 1},
# 					{'text': 'รู้เรื่องนิดหน่อย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'เรียนรู้เรื่อง', 'value': 4},
# 					{'text': 'เรียนเข้าใจมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'เครื่องคอมพิวเตอร์ใช้งานดีหรือไม่',
# 				'choices': [
# 					{'text': 'เครื่องช้ามาก', 'value': 1},
# 					{'text': 'เครื่องค่อนข้างช้า', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'เครื่องเร็ว', 'value': 4},
# 					{'text': 'เครื่องเร็วมากๆ', 'value': 5}
# 				]
# 			},
#
# 		]
# 	},
#         {
# 		'id': 2,
# 		'title': 'ความยากข้อสอบ mid-term',
# 		'questions': [
# 			{
# 				'text': 'ข้อ 1',
# 				'choices': [
# 					{'text': 'ง่ายมากๆ', 'value': 1},
# 					{'text': 'ค่อนข้างง่าย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างยาก', 'value': 4},
# 					{'text': 'ยากมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'ข้อ 2',
# 				'choices': [
# 					{'text': 'ง่ายมากๆ', 'value': 1},
# 					{'text': 'ค่อนข้างง่าย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างยาก', 'value': 4},
# 					{'text': 'ยากมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'ข้อ 3',
# 				'choices': [
# 					{'text': 'ง่ายมากๆ', 'value': 1},
# 					{'text': 'ค่อนข้างง่าย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างยาก', 'value': 4},
# 					{'text': 'ยากมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'ข้อ 4',
# 				'choices': [
# 					{'text': 'ง่ายมากๆ', 'value': 1},
# 					{'text': 'ค่อนข้างง่าย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างยาก', 'value': 4},
# 					{'text': 'ยากมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'ข้อ 5',
# 				'choices': [
# 					{'text': 'ง่ายมากๆ', 'value': 1},
# 					{'text': 'ค่อนข้างง่าย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างยาก', 'value': 4},
# 					{'text': 'ยากมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'ข้อ 6',
# 				'choices': [
# 					{'text': 'ง่ายมากๆ', 'value': 1},
# 					{'text': 'ค่อนข้างง่าย', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างยาก', 'value': 4},
# 					{'text': 'ยากมากๆ', 'value': 5}
# 				]
# 			},
#
# 		]
# 	},
#
#         {
# 		'id': 4,
# 		'title': 'อาหารที่ชอบ',
# 		'questions': [
# 			{
# 				'text': 'พิซซ่า',
# 				'choices': [
# 					{'text': 'ไม่ชอบเลย', 'value': 1},
# 					{'text': 'ค่อนข้างไม่ชอบ', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างชอบ', 'value': 4},
# 					{'text': 'ชอบมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'ไก่ทอด',
# 				'choices': [
# 					{'text': 'ไม่ชอบเลย', 'value': 1},
# 					{'text': 'ค่อนข้างไม่ชอบ', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างชอบ', 'value': 4},
# 					{'text': 'ชอบมากๆ', 'value': 5}
# 				]
# 			},
# 			{
# 				'text': 'แฮมเบอร์เกอร์',
# 				'choices': [
# 					{'text': 'ไม่ชอบเลย', 'value': 1},
# 					{'text': 'ค่อนข้างไม่ชอบ', 'value': 2},
# 					{'text': 'เฉยๆ', 'value': 3},
# 					{'text': 'ค่อนข้างชอบ', 'value': 4},
# 					{'text': 'ชอบมากๆ', 'value': 5}
# 				]
# 			},
#
# 		]
# 	},
#     ]
def index(request):
	# lab week 1
    # context = {
    #     'page_title': 'welcome to ,y poll',
    #     'poll_list': poll_list
    # }
    # return render(request,'polls/index.html',context=context)

	poll_list = Poll.objects.all()

	for poll in poll_list:
		question_count = Question.objects.filter(poll_id=poll.id).count()
		poll.question_count = question_count
	context = {
		'page_title': 'My Polls',
		'poll_list': poll_list
	}
	print(request.user)
	return render(request, template_name = 'polls/index.html', context=context)
@login_required
@permission_required('polls.view_poll')
def detail(request,id1):
	# lab week 1
    # for i in range(len(poll_list)):
    #     j = poll_list[i]["id"]
    #     if(id1 == str(j)):
    #         context = {
    #             'poll_list': poll_list[i],
	#
    #         }
	poll = Poll.objects.get(pk=id1)
	for question in poll.question_set.all():
		choice_id = request.GET.get(str(question.id))
		if choice_id:
			try:
				ans = Answer.objects.get(question_id=question.id)
				ans.choice_id=choice_id
				ans.save()
			except Answer.DoesNotExist:
				Answer.objects.create(
					question_id=question.id,
					choice_id=choice_id
				)
            # break
    # return render(request,'polls/detail.html',context=context)

	return render(request, 'polls/detail.html', {'poll': poll})

@login_required
@permission_required('polls.add_poll')
def create(request):
	if request.method=="POST":
		form = PollForm(request.POST)
		if form.is_valid():
			poll=Poll.objects.create(
				title=form.cleaned_data.get("title"),
				start_date=form.cleaned_data.get("start_date"),
				end_date=form.cleaned_data.get("end_date"),
			)

			for i in range(1, form.cleaned_data.get("no_questions")+1):
				Question.objects.create(
					text="Q"+str(i),
					type="01",
					poll=poll
				)

	else:
		form = PollForm()

	context = {"form" : form}
	return render(request, 'polls/create.html',context=context)

	# else:
	# 	return render(request, 'polls/create.html', context)

def my_login(request):
	context ={}
	if request.method == 'POST':
		username= request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request,username=username,password=password)

		if user:
			login(request,user)

			next_url=request.POST.get('next_url')
			if next_url:
				return redirect(next_url)
			else:
				return redirect("index")
		else:
			context['username']=username
			context['password']=password
			context['error']= 'Wrong username or password'
	next_url = request.GET.get('next')
	if next_url:
		context['next_url'] = next_url

	return render(request, template_name='polls/login.html',context=context)

def my_logout(requset):
	logout(requset)
	return redirect('login')

def comment(request):
	if request.method=="POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			poll=Comment.objects.create(
				title=form.cleaned_data.get("title"),
				body=form.cleaned_data.get("body"),
				email=form.cleaned_data.get("email"),
				tel=form.cleaned_data.get("tel"),
			)

	else:
		form = CommentForm()

	context = {"form": form}
	return render(request, 'polls/comment.html',context=context)

@login_required
@permission_required('polls.view_poll')
def change_pass(request):
	if request.method=="POST":
		form = ChangePass(request.POST)
		if form.is_valid():
			u = User.objects.get(username='qwe')
			u.set_password(form.cleaned_data.get("new_pass"))
			u.save()

	else:
		form = ChangePass()

	context = {"form" : form}
	return render(request, 'polls/change.html',context=context)


def my_register(request):
	if request.method=="POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data.get("user"))
			user = User.objects.create_user(form.cleaned_data.get("user"),form.cleaned_data.get("email"),form.cleaned_data.get("newpass"))
			user.save()
			poll = Profile.objects.create(

				line_id=form.cleaned_data.get("line_id"),
				facebook=form.cleaned_data.get("facebook"),
				gender=form.cleaned_data.get("gender"),
				birthdate=form.cleaned_data.get("birth"),
				user=user,
			)

	else:
		form = RegisterForm()

	context = {"form" : form}
	return render(request, 'polls/register.html',context=context)