from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from home.models import Profile, Contact
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from .helpers import send_forget_password_mail
from blog.models import Post


# Create your views here.
def home(request):
    return render(request, 'home/home.html')


# def about(request):
#     return render(request, 'home/about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        if len(name) < 2 or len(email) < 3 or len(message) < 4:
            messages.error(request, "Please fill the details correctly")
        else:
            contactDetails = Contact(name=name, email=email, message=message)
            contactDetails.save()
            messages.success(request, "Your message has been send successfully")
    return render(request, 'home/contact.html')


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()
        if user_obj is None:
            messages.error(request, 'User not found.')
            return redirect('/login')

        profile_obj = Profile.objects.filter(user=user_obj).first()

        if not profile_obj.is_verified:
            messages.error(request, 'Profile is not verified check your mail..')
            return redirect('/login')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, 'Wrong password')
            return redirect('/login')

        login(request, user)
        return redirect('/')
    return render(request, 'home/login.html')


def register_attempt(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')

        try:
            if User.objects.filter(username=username).first():
                messages.error(request, 'Username is already taken')
                return redirect('home/register')

            if User.objects.filter(email=email).first():
                messages.error(request, 'Email is already taken')
                return redirect('home/register')

            if password != confirmPassword:
                messages.error(request, 'Password does not match')

            user_obj = User.objects.create_user(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())

            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()

            send_mail_after_registration(email, auth_token)

            return redirect('/token')

        except Exception as e:
            print(e)

    return render(request, 'home/register.html')


def success(request):
    return render(request, 'home/success.html')


def token_send(request):
    return render(request, 'home/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified')
                return redirect('/login')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, 'home/error.html')


def send_mail_after_registration(email, token):
    subject = "Your account need to be verified"
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def user_logout(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('/login')


def ChangePassword(request, token):
    context = {}
    try:
        profile_obj = Profile.objects.filter(forget_password_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.error(request, "No user id found")
                return redirect(f'/change_password/{token}/')

            if new_password != confirm_password:
                messages.error(request, "Password does not match")
                return redirect(f'/change_password/{token}/')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')

    except Exception as e:
        print(e)
    return render(request, 'home/change_password.html', context)


import uuid


def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.error(request, 'Not user found with this username')
                return redirect('/forget_password/')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent')
            return redirect('/forget_password/')

    except Exception as e:
        print(e)
    return render(request, 'home/forget_password.html')


def search(request):
    query = request.GET['query']
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        # allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query.")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
