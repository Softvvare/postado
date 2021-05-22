from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages

from app.forms import RegisterForm, CreatePostForm
from app.models import Post, Like
from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request=request, template_name='landing.html')


@login_required
def feed(request):
    # arkadaşları ekleyince request.user yerine arkadaşlarını al
    user = request.user
    posts = Post.objects.filter(user=user)
    context = {
        'user': user,
        'posts': posts
    }
    return render(request=request, template_name='feed.html', context=context)


def login_request(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        if username:
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect(feed)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(request=request,
                  template_name="login.html",
                  context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, f"Logged out.")
    return redirect(login_request)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.info(request, f"You are now logged in as {username}")
            redirect(feed)

    else:
        form = RegisterForm()

    return render(request=request,
                  template_name="register.html",
                  context={"form": form})


@login_required
def create(request):
    user = request.user
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            messages.success(request, f'Posted Successfully')
            return redirect("feed")
        else:
            messages.error(request, f'Something went wrong!')
            return redirect("create")
    else:
        form = CreatePostForm()
    return render(request=request, template_name="create.html", context={'form': form})


@login_required
def delete(request, id):
    post = Post.objects.filter(id=id)
    post.delete()
    return redirect('feed')


@login_required
def like(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    like = Like.objects.filter(post=post, user=user)
    if like.exists():
        like.delete()
        post.likes_count -= 1
    else:
        like.create(user=user, post=post)
        post.likes_count += 1
    post.save()
    return redirect('feed')
