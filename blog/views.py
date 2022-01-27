from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponseRedirect, redirect
from blog.models import Post, BlogComment
from django.contrib import messages
from .form import PostForm
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

def blogHome(request):
    allPosts = Post.objects.all()
    context = {'allPosts': allPosts}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict = {}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context = {'post': post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}
    return render(request, "blog/blogPost.html", context)


def postComment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        postSno = request.POST.get('postSno')
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get('parentSno')
        if parentSno == "":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")

    return redirect(f"/blog/{post.slug}")


def addpost(request):
    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                form = PostForm(request.POST)
                if form.is_valid():
                    title = form.cleaned_data['title']
                    content = form.cleaned_data['content']
                    user = request.user
                    pst = Post(title=title, content=content, user=user)
                    if len(title) < 4 or len(content) < 10:
                        messages.error(request, 'Please write something!!')
                    else:
                        pst.save()
                        messages.success(request, "Post added successfully")
                        form = PostForm()
            else:
                form = PostForm()
            return render(request, 'blog/addpost.html', {'form': form})
        else:
            return HttpResponseRedirect('/login/')
    except Exception as e:
        print(e)


def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        posts = Post.objects.filter(user=user)
        return render(request, 'blog/dashboard.html', {'posts': posts})
    else:
        return render(request, 'home,login.html')


def update_post(request, id):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                pi = Post.objects.get(sno=id)
                form = PostForm(request.POST, instance=pi)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Post updated Successfully")
            else:
                pi = Post.objects.get(sno=id)
                form = PostForm(instance=pi)
            return render(request, 'blog/updatepost.html', {'form': form})
        else:
            return HttpResponseRedirect('/login/')
    except Exception as e:
        print(e)


def delete_post(request, id):
    try:
        if request.user.is_authenticated:
            if request.method == 'POST':
                pi = Post.objects.get(sno=id)
                pi.delete()
                messages.success(request, "Post deleted successfully")
                return HttpResponseRedirect('/blog/dashboard/')
        else:
            return HttpResponseRedirect('/login/')
    except Exception as e:
        print(e)
