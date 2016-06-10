from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserLoginForm, UserRegisterForm, UserProfileForm


@login_required
def profile_view(request):
    profile_form = UserProfileForm(request.POST or None, request.FILES or None)
    if profile_form.is_valid():
        instance = profile_form.save(commit=False)
        try:
            request.user.profile.delete()
            instance.user = request.user
        except:
            instance.user = request.user
        instance.save()
        html_message = 'Profile Updated'
        html_message = settings.MESSAGE % ('info', html_message)
        messages.success(request, html_message, extra_tags='html_safe')
        redirect('accounts:profile')

    context = {
        'user': request.user,
        'profile_form': profile_form,
    }
    return render(request, 'profile.html', context)


def login_view(request):
    form = UserLoginForm(request.POST or None)
    next_var = request.GET.get('next')
    title = 'Login'
    # print(request.user.is_authenticated())

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)
        print(request.user.is_authenticated())
        # redirect
        html_message = 'Logged In'
        html_message = settings.MESSAGE % ('success', html_message)
        messages.success(request, html_message, extra_tags='html_safe')
        if next_var:
            return redirect(next_var)
        return redirect('posts:list')
    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'form.html', context)


def register_view(request):
    print(request.user.is_authenticated())
    next_var = request.GET.get('next')
    title = 'Register'
    form = UserRegisterForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        new_user = authenticate(
                username=user.username,
                password=password
        )
        login(request, new_user)
        html_message = 'Registered'
        html_message = settings.MESSAGE % ('info', html_message)
        messages.success(request, html_message, extra_tags='html_safe')
        if next_var:
            return redirect(next_var)
        return redirect('posts:list')

    context = {
        'form': form,
        'title': title,
    }
    return render(request, 'form.html', context)


def logout_view(request):
    logout(request)
    html_message = 'Logged Out'
    html_message = settings.MESSAGE % ('warning', html_message)
    messages.success(request, html_message, extra_tags='html_safe')
    return redirect('posts:list')
