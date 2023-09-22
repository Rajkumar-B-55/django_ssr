from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(max_length=150, required=True)
    phone_number = forms.CharField(max_length=13, required=True)
    last_name = forms.CharField(max_length=200, required=False)
    password = forms.CharField(required=True, widget=forms.PasswordInput)


class UpdateForm(forms.Form):
    first_name = forms.CharField(max_length=200, required=True)
    last_name = forms.CharField(max_length=200, required=False)
    phone_number = forms.CharField(max_length=13, required=True)


