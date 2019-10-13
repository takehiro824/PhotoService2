from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from .forms import PhotoForm
from django.contrib import messages
from django.views.decorators.http import require_POST 
from .forms import AppliForm, SearchForm, CommentForm
from .models import Good, Friend, Photo, Comment
from django.db.models import Q
from django.http import JsonResponse
import re

def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos})

@login_required
def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    good_user = user.good_user.all()
    apple = user.friend_user.count 
    pan = user.friend_owner.count 
    return render(request, 'app/users_detail.html', {'user': user, 'photos': photos, 'apple':apple, 'pan':pan, 'good_user':good_user})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # ユーザーインスタンスを作成
        if form.is_valid():
            new_user = form.save() # ユーザーインスタンスを保存
            input_username = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            new_user = authenticate(username=input_username, password=input_password)
            if new_user is not None:
                login(request, new_user)
                return redirect('app:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})

@login_required
def photos_new(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, "投稿が完了しました！") 
        return redirect('app:index')
    else:   
        form = PhotoForm()
    return render(request, 'app/photos_new.html', {'form': form})

@login_required
def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    comments = photo.comment_photo.all()
    user = photo.user
    good_user = user.good_user.all()
    return render(request, 'app/photos_detail.html', {'photo': photo, 'good_user':good_user, 'comments': comments})


def photos_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        form = PhotoForm(request.POST,instance=photo)
        if form.is_valid():
            form.save()
        return redirect('app:index')
    else:
        form = PhotoForm(instance=photo)
    return render(request,'app/photos_edit.html',{'form': form, 'photo': photo})

@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('app:users_detail', request.user.id)

@login_required
def share(request, share_id):
    share = Photo.objects.get(id=share_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        pho = Photo()
        pho.user = request.user
        pho.comment = comment
        pho.share_id = share.id
        pho.save()
        share_pho = pho.get_share()
        share_pho.share_count += 1
        share_pho.save()
  
        messages.success(request, 'メッセージをシェアしました！')
        return redirect('app:index')
    

    form = AppliForm(request.user)
    params = {
            'login_user':request.user,
            'form':form,
            'share':share,
        }
    return render(request, 'app/share.html', params)

@login_required
def good(request, good_id):
    
    good_pho = Photo.objects.get(id=good_id)

    is_good = Good.objects.filter(user=request.user).filter(photo=good_pho).count()
    
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect('app:index')
    
    # Messageのgood_countを１増やす
    good_pho.good_count += 1
    good_pho.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.user = request.user
    good.photo = good_pho
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect('app:index')

@login_required
def add(request):
    
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
    
    if add_user == request.user:
        messages.info(request, "自分自身をFriendに追加することはできません。")
        return redirect('app:index')

    
    frd_num = Friend.objects.filter(owner=request.user) \
            .filter(user=add_user).count()
    
    if frd_num > 0:
        messages.info(request, add_user.username + \
                ' は既に追加されています。')
        return redirect('app:index')
    
    
    frd = Friend()
    frd.owner = request.user
    frd.user = add_user
    frd.save()
    
    messages.success(request, add_user.username + ' をフレンドに追加しました！')
    return redirect('app:index')


@login_required
def photos_comment(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if form.is_valid(): 
            comment = form.save(commit=False) 
            comment.photo = photo
            comment.user = request.user
            comment.save()
            messages.success(request, "投稿が完了しました！")
    else:
        form = CommentForm()

    return render(request, 'app/photos_comment.html', {'photo': photo,'form': form})

# 空白文字の削除
def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    query_string = query_string.replace(u'　', ' ')
    query_string = query_string.replace(u'、', ' ')
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

# 検索クエリ作成
def get_query(query_string, search_fields):
    query = None 
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None 
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query

def search(request):
  form = SearchForm(request.GET) 
  if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['username'])
        blogs = User.objects.filter(entry_query).order_by('-pub_date')
  else:
        blogs = User.objects.all().order_by('-pub_date')


# Create your views here.