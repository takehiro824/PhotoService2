from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



app_name = 'app'
urlpatterns = [
    path('index', views.index, name='index'),
    path('photos/new/', views.photos_new, name='photos_new'),
    path('photos/<int:pk>/', views.photos_detail, name='photos_detail'), 
    path('photos/<int:pk>/delete/', views.photos_delete, name='photos_delete'), 
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'), 
    path('share/<int:share_id>', views.share, name='share'),

]