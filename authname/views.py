from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages
from django.http import HttpResponse
from django.urls import reverse_lazy
from authname.forms import UserForm
from user.models import User
from django.contrib.auth import (authenticate,login, logout, )
from django.contrib.auth.views import (PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView,)
# Create your views here.

class SignInView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_feed_view')
        return render(request, 'authname/signin.html')

    def post(self, request, *args, **kwargs):
        email_username = request.POST.get('email_username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=email_username)
            email = user_obj.email
        except Exception as e:
            email = email_username

        user = authenticate(request, email=email, password=password)
        
        if user is None:
            messages.error(request, 'Invalid Login.', extra_tags="error")
            return render(request, 'authname/signin.html') 

        login(request, user)
        messages.success(request, 'Thanks for Login, Welcome to Insta Clone.', extra_tags='success')
        return redirect('home_feed_view')
        


class SignUpView(View):
    form_class = UserForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home_feed_view')
        # ye wala code run kardo
        return render(request, 'authname/signup.html')

    def post(self, request, *args, **kwargs):
        # ye wala code run kardo
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin_view')

        context = {'form': form}

        return render(request, 'authname/signup.html', context)


class SignOutView(View):
    def post(self, request, *args, **kwargs):
        # is user is not authenticated
        logout(request)
        return redirect('signin_view')


class PRView(PasswordResetView):
    email_template_name = 'authname/password_reset_email.html'
    template_name = 'authname/password_reset.html'

class PRDone(PasswordResetDoneView):
    template_name = 'authname/password_reset_done.html'

class PRConfirm(PasswordResetConfirmView):
    template_name = 'authname/password_reset_confirm.html'

class PRComplete(PasswordResetCompleteView):
    template_name = 'authname/password_reset_complete.html'


class PWDChangeView(PasswordChangeView):
    template_name = 'authname/password_change.html'
    success_url = reverse_lazy('password_change_done_view')

class PWDChangeDoneView(PasswordChangeDoneView):
    template_name = 'authname/password_change_done.html'