import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import messages
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.decorators.http import require_POST

from memoapp.form import Postform, UserForm, LoginForm
from memoapp.models import Memos


def index(request):
    sort = request.GET.get('sort', '')  # url의 쿼리스트링을 가져온다. 없는 경우 공백을 리턴한다

    if sort == 'likes':
        memos = Memos.objects.annotate(like_count=Count('likes')).order_by('-like_count', '-update_date')
        return render(request, 'memoapp/index.html', {'memos': memos})
    elif sort == 'mypost':
        user = request.user
        memos = Memos.objects.filter(name_id=user).order_by('-update_date')  # 복수를 가져올수 있음
        return render(request, 'memoapp/index.html', {'memos': memos})
    else:
        memos = Memos.objects.order_by('-update_date')
        return render(request, 'memoapp/index.html', {'memos': memos})


def post(request):
    if request.method == "POST":
        form = Postform(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.name_id = User.objects.get(username=request.user.get_username())
            memo.generate()
            return redirect('index')
    else:
        form = Postform()
        return render(request, 'memoapp/write.html', {'form': form})


def modify(request, memokey):
    if request.method == "POST":
        memo = Memos.objects.get(pk = memokey)
        form = Postform(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        memo = Memos.objects.get(pk=memokey)
        if memo.name_id == User.objects.get(username=request.user.get_username()):
            form = Postform(instance=memo)
            return render(request, 'memoapp/modify.html', {'memo': memo, 'form': form})
        else:
            return render(request, 'memoapp/warning.html')


def delete(request, memokey):
    memo = Memos.objects.get(pk=memokey)
    if memo.name_id == User.objects.get(username = request.user.get_username()):
        memo.delete()
        return redirect('index')
    else:
        return render(request, 'memoapp/warning.html')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('index')
        else:
            return HttpResponse('사용자명이 이미 존재합니다.')
    else:
        form = UserForm
        return render(request, 'memoapp/adduser.html', {'form': form})


def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요')
    else:
        form = LoginForm()
        return render(request, 'memoapp/login.html', {'form': form})


def signout(request):
    logout(request)
    return redirect('index')

@login_required
@require_POST
def like(request):
    if request.method == 'POST':
        user = request.user # 로그인한 유저를 가져온다.
        memo_id = request.POST.get('pk', None)
        memo = Memos.objects.get(pk = memo_id) #해당 메모 오브젝트를 가져온다.
        print('1\n\n\n')

        if memo.likes.filter(id = user.id).exists(): #이미 해당 유저가 likes컬럼에 존재하면
            memo.likes.remove(user) #likes 컬럼에서 해당 유저를 지운다.
            print('2\n\n\n')
            message = 'You disliked this'
        else:
            memo.likes.add(user)
            print('3\n\n\n')
            message = 'You liked this'

    context = {'likes_count' : memo.total_likes, 'message' : message}
    return HttpResponse(json.dumps(context), content_type='application/json')
    # dic 형식을 json 형식으로 바꾸어 전달한다.
