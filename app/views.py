from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from app.forms import RegisterForm, CreatePostForm, CreateCommentForm, UpdateUserForm, UpdateProfileForm
from app.models import Comment, Post, Like, Profile, UserFollowing
from django.contrib.auth.decorators import login_required


def landing(request):
    return render(request=request, template_name='landing.html')


@login_required
def feed(request):
    user = request.user
    follow_posts = Post.objects.filter(
        user__followers__user_id=user)
    self_posts = Post.objects.filter(user=user)
    posts = (follow_posts | self_posts).distinct()
    context = {
        'user': user,
        'posts': posts
    }
    return render(request=request, template_name='feed.html', context=context)


def explore(request):
    user = request.user

    if request.method != "POST":
        posts = Post.objects.all()
        context = {
            'user': user,
            'posts': posts
        }
        print("1")
        return render(request=request, template_name='explore.html', context=context)

    else:
        queried_tags = request.POST.get('selected_tag')
        if queried_tags is not None:
            tag_list = queried_tags.split(',')
            posts = Post.objects.filter(tags__name__in=tag_list)
            context = {
                'user': user,
                'posts': posts
            }
            print("2")
            print(queried_tags)
            return render(request=request, template_name='explore.html', context=context)
        else:
            posts = Post.objects.all()
            context = {
                'user': user,
                'posts': posts
            }
            print("3")
            print(queried_tags)
            return render(request=request, template_name='explore.html', context=context)


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
            form.save_m2m()
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
    post = Post.objects.get(id=id)
    like = Like.objects.filter(post=post)
    comment = Comment.objects.filter(post=post)
    like.delete()
    comment.delete()
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


@login_required
def comments(request, id):
    user = request.user
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post)
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            post.comments_count += 1
            post.save()
            data = form.save(commit=False)
            data.user = user
            data.post = post
            data.save()
            messages.success(request, f'Posted comment Successfully')
            return redirect(reverse("comments", kwargs={'id': id}))
        else:
            messages.error(request, f'Something went wrong!')
            return redirect(reverse("comments", kwargs={'id': id}))
    form = CreateCommentForm()
    context = {
        'users': user,
        'posts': post,
        'comments': comments,
        'form': form
    }
    return render(request=request, template_name='comments.html', context=context)


@login_required
def profile(request, user_name):
    user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user)
    session_user = request.user

    is_following = False
    session_following = UserFollowing.objects.filter(
        user_id=session_user, following_user_id=user)
    if session_following.exists():
        is_following = True
    else:
        is_following = False

    context = {
        "session_user": session_user,
        "profile": profile,
        "followings": user.following.all(),
        "followers": user.followers.all(),
        "posts": posts,
        "is_following": is_following
    }

    return render(request=request, template_name="profile.html", context=context)


@login_required
def follow(request, user_name):
    user = User.objects.get(username=user_name)
    session_user = request.user
    session_following = UserFollowing.objects.filter(
        user_id=session_user, following_user_id=user)

    if session_following.exists():
        session_following.delete()  # unfollow
    else:
        session_following.create(user_id=session_user,
                                 following_user_id=user)  # follow
    return redirect(reverse("profile", kwargs={'user_name': user_name}))


@login_required
def update_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        p_form = UpdateProfileForm(
            request.POST, request.FILES, instance=profile)
        u_form = UpdateUserForm(request.POST, instance=user)
        if p_form.is_valid() and u_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Updated Successfully')
            return redirect("update_profile")
        else:
            messages.error(request, f'Something went wrong!')
            return redirect("update_profile")
    else:
        p_form = UpdateProfileForm(instance=user)
        u_form = UpdateUserForm(instance=user)
    context = {
        'p_form': p_form,
        'u_form': u_form
    }
    return render(request=request, template_name="update_profile.html", context=context)
