from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':'Username', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Username"'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'name', 'placeholder':'Password', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Password"'}))


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control', 'id':'name', 'placeholder':'Username', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Username"'})
        self.fields['email'].widget.attrs.update({'class':'form-control', 'id':'email', 'placeholder':'Email', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Email"'})
        self.fields['password1'].widget.attrs.update({'class':'form-control', 'id':'Password', 'placeholder':'Password', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Password"'})
        self.fields['password2'].widget.attrs.update({'class':'form-control', 'id':'confirmPassword', 'placeholder':'conf Password', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "conf Password"'})

    email = forms.EmailField(widget=forms.EmailInput())
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


# class RegisterForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id':'name', 'placeholder':'Username', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Username"'}))
#     email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'id':'email', 'placeholder':'Email', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Email"'}))
#     password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'Password', 'placeholder':'Password', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "Password"'}))
#     password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'confirmPassword', 'placeholder':'conf Password', 'onfocus':'this.placeholder = ""', 'onblur':'this.placeholder = "conf Password"'}))

#     def clean_username(self):
#         username = self.cleaned_data.get('username')
#         if User.objects.filter(username).exists():
#             raise forms.ValidationError('username has alredy exists!')
#         return username

#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         if User.objects.filter(email=email).exists():
#             raise forms.ValidationError('email has alredy exists please change new email')
    
#     def clean_password2(self):
#         data = self.cleaned_data
#         pass1 = self.cleaned_data.get('password1')
#         pass2 = self.cleaned_data.get('password2')
#         if pass1 and pass2:
#             if pass1 != pass2:
#                 raise forms.ValidationError('the password if different')
#             if len(pass1) < 8:
#                 raise forms.ValidationError('password must not be less than 8 characters')
#         return data
