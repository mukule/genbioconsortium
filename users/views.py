from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import get_user_model
from .forms import UserUpdateForm
from .forms import SetPasswordForm
from .forms import UserRegisterForm
from .token import account_activation_token
from django.contrib.auth.decorators import login_required
from .forms import SetPasswordForm
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth import authenticate, login
from django.conf import settings
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from .forms import PasswordResetForm
from django.db.models.query_utils import Q
from .forms import SetPasswordForm


# Create your views here.
def home(request):
    return render(request, 'users/home.html')

def register(request):
   if request.method == "POST":
     form = UserRegisterForm(request.POST)
     if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        activateEmail(request, user, form.cleaned_data.get('email'))
        return redirect('register')
     else:
         for error in list(form.errors.values()):
            messages.error(request, error)

        # username = form.cleaned_data.get('username')
        # messages.success(request, f'Account created succesfully for { username}')
        # return redirect('login')
   else:
      form = UserRegisterForm
   return render(request, 'users/register.html',{'form':form})

def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('users/acc_active_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Hello {user} , please go to you email {to_email} inbox or check your spam folder and click on \
            received activation link from African Genetic Biocontrol consortium to confirm and complete the registration.')
    else:
        messages.error(request, f'If you did not receive the email, Please confirm that {to_email} this is your actual mail')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thanks for your email confirmation. Log in now ')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')
    
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', None)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            
            if remember_me:
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            else:
                request.session.set_expiry(0)

            return redirect('home')
        else:
            # Handle invalid login
            pass

    return render(request, 'users/login.html')

@login_required
def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f'{user_form}, Your profile has been updated!')
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        return render(request, 'users/profile.html', context={'form': form})

    return redirect("profile")

@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'users/password_reset_confirm.html', {'form': form})


def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("users/template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                       Password reset has been emailed to you please check your mail
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>An authentic error occurred/b>")

            return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the reCAPTCHA test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="users/password_reset.html", 
        context={"form": form}
        )
def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('homepage')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'home/password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")




