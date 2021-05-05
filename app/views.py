from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


def feed(request):
    return render(request, 'feed.html')


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
                  template_name="templates/login.html",
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
                  template_name="templates/register.html",
                  context={"form": form})
