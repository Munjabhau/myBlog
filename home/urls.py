from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('register/', views.register_attempt, name="register_attempt"),
    path('login/', views.login_attempt, name="login_attempt"),
    path('logout', views.user_logout, name="logout"),
    path('token', views.token_send, name="token_send"),
    path('success', views.success, name="success"),
    path('verify/<auth_token>', views.verify, name="verify"),
    path('error', views.error_page, name="error"),
    path('change_password/<token>/', views.ChangePassword, name="change_password"),
    path('forget_password/', views.ForgetPassword, name="forget_password"),
    path('search', views.search, name="search"),
]
