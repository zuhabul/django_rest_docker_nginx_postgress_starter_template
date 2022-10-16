from django.urls import path

from user import views

app_name = 'user'

urlpatterns = [
    path('oauth/create/', views.CreateUserView.as_view(), name ='create'),
    path('oauth/social/', views.SocialLoginView.as_view(), name ='create'),
    path('oauth/login/', views.LoginUserView.as_view(), name='authorize'),
    path('oauth/logout/', views.LogoutView.as_view(), name='logout'),
    path('me/', views.ManageUserView.as_view(), name ='me'),
    path('me/upload/', views.UserImageUploadProfileView.as_view(), name ='image_upload'),
]
