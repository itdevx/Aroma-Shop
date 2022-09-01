from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import View
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from account import forms
from store import models
from django.contrib.auth.models import User



class Dashboard(LoginRequiredMixin, generic.View):
    login_url = 'account:login'
    def get(self, request):

        items = models.Item.objects.all().order_by('-id')[:10]
        c = {
            'items': items
        }

        return render(request, 'dashboard.html', c) 


class DashboardProfile(generic.View):
    def get(self, request):
        user = User.objects.filter(username=request.user.username).first()
        
        c = {
            'user': user
        }

        return render(request, 'profile.html', c)


class AllUser(generic.View):
    def get(self, request):
        if request.user.is_superuser:

            users = User.objects.all()

            c = {
                'users': users
            }
            return render(request, 'all-users.html', c)

        else:
            raise Http404()




class LoginView(View):
    template_name = 'login.html'
    form_class = forms.LoginForm

    def get(self, request):
        form = self.form_class()
        context = {
            'form':form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = request.POST.get('remember')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                return redirect('store:index')
            else:
                form.add_error(field='username', error='username has not found!')
    
        return render(request, self.template_name, {'form':form})


class LogoutView(View):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('store:index')


class RegisterView(generic.CreateView):
    model = User
    template_name = 'register.html'
    form_class = forms.RegisterForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('store:index')


# User = get_user_model()
# class RegisterView(View):
#     template_name = 'register.html'
#     form_class = forms.RegisterForm
    
#     def get(self, request):
#         form = self.form_class()
#         context = {
#             'form':form
#         }
#         return render(request, self.template_name, context)
    
#     def post(self, form):
#         form = self.form_class(self.request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username') 
#             email = form.cleaned_data.get('email') 
#             password = form.cleaned_data.get('password1') 
#             remember_me = self.request.POST.get('remember')
#             User.objects.create_user(username=username, email=email, password=password)
#             user = authenticate(self.request, username=username, password=password)
#             if user is not None:
#                 login(self.request, user)
#                 if not remember_me:
#                     self.request.session.set_expiry(0)
#                 return redirect('store:index')

#         return render(self.request, self.template_name, {'form':form})
