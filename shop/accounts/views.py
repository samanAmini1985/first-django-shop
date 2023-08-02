from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import UserRegistrationForm, UserVerifyCodeForm, UserLogInForm, UserProfileForm
import random
from utils import send_otp_code
from .models import OtpCode, User
from django.contrib import messages
import pytz
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone_number': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'address': form.cleaned_data['address'],
                'zip_code': form.cleaned_data['zip_code'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we sent you code', 'info')
            return redirect('accounts:verify_code')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = UserVerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user_session = request.session['user_registration_info']  # add a session with name user_registration_info
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                expired_time = datetime.now(tz=pytz.timezone('Asia/Tehran')) - timedelta(minutes=2)
                if OtpCode.objects.filter(created__gt=expired_time):
                    User.objects.create_user(user_session['phone_number'], user_session['email'],
                                             user_session['full_name'], user_session['address'],
                                             user_session['zip_code'],
                                             user_session['password'], )
                    code_instance.delete()
                    messages.success(request, 'you registered successfully', 'success')
                    return redirect('home:home')
                else:
                    code_instance.delete()
                    messages.error(request, 'time is over, please try again', 'danger')
                    return redirect('accounts:user_register')
            else:
                messages.error(request, 'code is wrong!', 'danger')
                return redirect('accounts:verify_code')
        return redirect('home:home')


class UserLogInView(View):
    class_form = UserLogInForm
    template_name = 'accounts/user_login.html'

    def get(self, request):
        form = self.class_form
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.class_form(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                return redirect('home:home')
            messages.error(request, 'phone or password is wrong', 'danger')
            return render(request, self.template_name)


class UserLogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'info')
        return redirect('home:home')


class UserProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/user_profile.html'
    form_class = UserProfileForm

    def dispatch(self, request, *args, **kwargs):
        user = User.objects.get(id=kwargs['user_id'])
        if not user.id == request.user.id:
            messages.error(request, 'You can not change details of this user', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = self.form_class(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        form = self.form_class(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your detail changed successfully', 'success')
            return redirect('home:home')


class UserPasswordResetView(auth_views.PasswordResetView):
    '''
    this class make an emil and generate a link to reset password of user.
    reverse_lazy method makes sure that this url is made.
    '''
    template_name = 'accounts/password_reset_form.html'  # template to show a form to reset password
    success_url = reverse_lazy('accounts:password_reset_done')  # redirect user after sending email
    email_template_name = 'accounts/password_reset_email.html'  # email that will be send to user


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class UserPasswordConfirmView(auth_views.PasswordResetConfirmView):
    '''
    to shows a form to user to change password.
    '''
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
