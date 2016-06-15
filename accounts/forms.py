from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .models import UserProfile
User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):           # this will give errors on the whole form.
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("this user doesn't exists")

            if not user.check_password(password):
                raise forms.ValidationError("INcorrect Password")

            if not user.is_active:
                raise forms.ValidationError("The user is no longer active")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email')
    email2 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'email2',
            'password',
        ]

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError("Passwords must match")
        if not 8 < len(str(password)) < 30 :
            raise forms.ValidationError("Password's length must be in between 8 to 30 characters.")
        return password

    def clean_email2(self):         # this will give error on the field.
        # print(self.cleaned_data)
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')
        if email != email2:
            raise forms.ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered.")
        return email


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = [
            'profile_picture',
            'about',
        ]
