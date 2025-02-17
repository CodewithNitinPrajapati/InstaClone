from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse
from user.models import User 
from django.contrib import messages
from django.db.models import Q

from user.forms import UserEditForm
from core.models import Follow
# Create your views here.



class ProfileView(View):
    

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            return HttpResponse('<h1>This page does not exist.</h1>')

        
        if username == request.user.username:
            context = { 'user': user }
            return render(request, 'user/authenticated_profile.html', context=context)
        else:
            try:
                Follow.objects.get(user=request.user, followed=user)
                is_follows_this_user = True
            except Exception as e:
                is_follows_this_user = False
                    
            context = { 'user': user, 'is_follows_this_user': is_follows_this_user }
            return render(request, 'user/anonymous_profile.html', context=context)


class ProfileEditView(View):
    template_name = 'user/profile_edit.html'
    form_class = UserEditForm

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')

        if username != request.user.username:
            return HttpResponse('<h1>This page does not exist.</h1>')

        form = self.form_class(instance=request.user)
        context = {'form': form}
        return render(request, 'user/profile_edit.html', context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Saved your details in a safe place.')
            return redirect('profile_edit_view', request.user.username)
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' is-invalid'
            context = {'form': form}
            return render(request, 'user/profile_edit.html', context=context)


class AllProfilesView(View):
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('query')

        if search_term:
            all_profiles = User.objects.filter(
                    Q(username__contains=search_term) | Q(full_name__contains=search_term)
                ).exclude(
                    username=request.user.username
                )
        else:
            all_profiles = User.objects.none()

        context = {'all_profiles': all_profiles}
        return render(request, 'user/all_profiles.html', context=context)