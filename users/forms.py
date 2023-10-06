from django import forms

from users.models import User


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=150, required=True)
    phone_number = forms.CharField(max_length=13, required=True, )
    last_name = forms.CharField(max_length=200, required=False, )
    password = forms.CharField(max_length=200, required=True, widget=forms.PasswordInput())


class RegistrationForm_(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['is_superuser', 'groups', 'user_permissions', 'is_staff', 'is_active', 'date_joined', 'role',
                   'last_login', 'username']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', ]
    # first_name = forms.CharField(max_length=200, required=True)
    # last_name = forms.CharField(max_length=200, required=False)
    # phone_number = forms.CharField(max_length=13, required=True)
