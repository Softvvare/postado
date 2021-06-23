from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import ChatRoom, Messages
from django.contrib import messages
from .forms import CreateMessagesForm, CreateRoomForm
from django.contrib.auth.models import User
from app.models import UserFollowing


@login_required
def navigator(request):
    user = request.user
    rooms = ChatRoom.objects.filter(auth=user)

    if request.method == 'POST':
        form = CreateRoomForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.auth = user
            name = form.cleaned_data["receiver"].following_user_id

            data.name = "From-{}-to-{}".format(
                user.username, form.cleaned_data["receiver"].following_user_id.username)

            dup = UserFollowing.objects.get(following_user_id = form.cleaned_data["receiver"].following_user_id)
            print("\n\n",type(dup),"\n\n")

            if ChatRoom.objects.filter(receiver=dup).exists():
                messages.error(request, f'You can not open second chat room!')
                return redirect(navigator)

            data.save()
            return redirect(navigator)
        else:
            messages.error(request, f'Something went wrong!')
            return redirect(navigator)
    form = CreateRoomForm()
    try:
        ff = UserFollowing.objects.get(following_user_id=user)
        received = ChatRoom.objects.filter(receiver=ff)
        context = {
            'user': user,
            'rooms': rooms,
            'received': received,
            'form': form
        }
    except:
        context = {
            'user': user,
            'rooms': rooms,
            'form': form
        }

    return render(request=request, template_name='chat/navigator.html', context=context)


@login_required
def room(request, name):
    user = request.user
    chat_room = ChatRoom.objects.get(name=name)
    msg = Messages.objects.filter(room=chat_room)
    if request.method == 'POST':
        form = CreateMessagesForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.room = chat_room
            data.save()
            return redirect(reverse("room", kwargs={'name': name}))
        else:
            messages.error(request, f'Something went wrong!')
            return redirect(reverse("room", kwargs={'name': name}))
    form = CreateMessagesForm()
    context = {
        'users': user,
        'room': chat_room,
        'msg': msg,
        'form': form
    }
    return render(request=request, template_name='chat/room.html', context=context)
