from django.shortcuts import get_object_or_404, redirect, render
from .models import Photo
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required 
from .forms import PhotoForm
from django.contrib import messages
from django.views.decorators.http import require_POST 
from .forms import AppliForm

def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'app/index.html', {'photos': photos})

def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'app/users_detail.html', {'user': user, 'photos': photos})

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

def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'app/photos_detail.html', {'photo': photo})

@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('app:users_detail', request.user.id)

@login_required
def share(request, share_id):
    # シェアするMessageの取得
    share = Photo.objects.get(id=share_id)
    # POST送信時の処理
    if request.method == 'POST':
        # 送信内容を取得
        comment = request.POST['comment']
        image = request.POST['image']
       
        # メッセージを作成し、設定をして保存
        pho = Photo()
        pho.user = request.user
        pho.comment = comment
        pho.share_id = share.id
        pho.save()
        share_pho = pho.get_share()
        share_pho.share_count += 1
        share_pho.save()
        # メッセージを設定
        messages.success(request, 'メッセージをシェアしました！')
        return redirect('app:index')
    
    # 共通処理
    form = AppliForm(request.user)
    params = {
            'login_user':request.user,
            'form':form,
            'share':share,
        }
    return render(request, 'app/share.html', params)
# Create your views here.