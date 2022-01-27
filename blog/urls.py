from django.urls import path, include
from blog import views

urlpatterns = [
    path('postComment', views.postComment, name="postComment"),
    path('', views.blogHome, name='bloghome'),
    path('addpost', views.addpost, name='addpost'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('updatepost/<int:id>/', views.update_post, name='updatepost'),
    path('delete/<int:id>/', views.delete_post, name='deletepost'),
    path('<str:slug>', views.blogPost, name='blogPost'),

]
