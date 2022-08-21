from re import A
from telnetlib import AYT
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, CreateView
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from account import forms



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


User = get_user_model()
# def register_view(request):
#     if request.method == 'POST':
#         form = forms.RegisterForm(request.POST)
#         context = {'form':form}
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password1')
#             User.objects.create_user(username=username, email=email, password=password)

#             if User.save():
#                 user = authenticate(request, username=username, password=password)
#                 if user is not None:
#                     login(request, user)
#                     return redirect('store:index')
#         else :
#             form = forms.RegisterForm()
#     return render(request, 'register.html', context)

class RegisterView(View):
    template_name = 'register.html'
    form_class = forms.RegisterForm
    
    def get(self, request):
        form = self.form_class()
        context = {
            'form':form
        }
        return render(request, self.template_name, context)
    
    def post(self, form):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            email = form.cleaned_data.get('email') 
            password = form.cleaned_data.get('password1') 
            remember_me = self.request.POST.get('remember')
            User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(self.request, username=username, password=password)
            if user is not None:
                login(self.request, user)
                if not remember_me:
                    self.request.session.set_expiry(0)
                return redirect('store:index')

        return render(self.request, self.template_name, {'form':form})


