from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    '''
    to create a new user in admin panel
    '''
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name', 'address', 'zip_code')

    def clean_password2(self):
        '''
        to check password and confirm password are match
        '''
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError('password do not match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="You can change your password using <a href=\"../password/\"> this form </a>")

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'full_name', 'password', 'last_login', 'address', 'zip_code',)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('phone_number', 'address', 'zip_code',)


class UserRegistrationForm(forms.Form):
    phone = forms.CharField(max_length=11)
    email = forms.CharField()
    full_name = forms.CharField(label='full name')
    address = forms.CharField()
    zip_code = forms.CharField(label='zip code')
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number already exists')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class UserVerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLogInForm(forms.Form):
    phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
