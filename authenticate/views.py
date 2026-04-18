from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import PasswordReset
from django.urls import reverse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from userprofile.models import Profile

# Create your views here.

def signup( request ):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_data_have_error = False
        
        if User.objects.filter( username = username ).exists():
            user_data_have_error = True
            messages.error(request, 'This Username is already taken')
           

        if User.objects.filter( email = email ).exists():
            user_data_have_error = True
            messages.error(request, 'This email is alreday exists.')
            
        
        if len(password) < 5:
            user_data_have_error = True
            messages.error(request, 'The length of the password must be minimum of five characters.')
        
        
        if user_data_have_error == True:
            return redirect('signup')
        
        else:
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                password = password,
            )
            user.save()
            messages.success(request, 'The User is created successfully.')
            Profile.objects.get_or_create(
                user = user,
                defaults = {
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )
            messages.success(request, 'The User Profile is created successfully.')
            return redirect('home')
    return render( request, 'authenticate/signup.html' )



def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate( request, username = username, password = password )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'There are error in your credentials.')
            return redirect('login')
    return render( request, 'authenticate/login.html' )


def LogoutView(request):
    logout(request)
    return redirect('home')

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get ( email = email )
            new_reset_password = PasswordReset( user = user )
            new_reset_password.save()
            
            password_reset_url = reverse('reset_password', kwargs = {'reset_id': new_reset_password.reset_id}) 
            full_password_reset_url = f"{request.scheme}://{request.get_host()}{password_reset_url}"
            
            
            email_body = f"Reset your password using below link:\n\n\n{full_password_reset_url}"
            email_message = EmailMessage(
                'Reset Your Password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.fail_silently = True
            email_message.send()
            
            messages.success(request, f'Password Reset is sent to your registered email: "{email}"' )
            return redirect('forget_password_sent', reset_id=new_reset_password.reset_id)
        except User.DoesNotExist:
            messages.error( request, 'We could not find the request.')
            return redirect('forget_password')
            
    return render(request, 'authenticate/forget_password.html')

def forget_password_sent(request, reset_id):
    if PasswordReset.objects.filter( reset_id = reset_id ).exists():
        return render( request, 'authenticate/forget_password_sent.html')
    else:
        messages.error( request, 'The Password Reset does not exists.')
        return redirect('forget_password+reset', reset_id = PasswordReset.reset_id)

def reset_password(request, reset_id):
    try:
        password_reset_id = PasswordReset.objects.get( reset_id = reset_id )
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            password_reset_have_error = False
            
            if password != confirm_password:
                password_reset_have_reset = True
                messages.error(request, 'The Password does not match with Confirm Password.')
            
            if len(password) < 5:
                password_reset_have_error = True
                messages.error(request, 'The length of the password must be minimum of five characters.')
            
            expiration_time = password_reset_id.created_at + timezone.timedelta( minutes = 10 )
            if timezone.now() > expiration_time:
                messages.error( request, 'The Password Reset Link is expired.')
                return redirect('reset_password', reset_id = password_reset_id.reset_id )
            
            if password_reset_have_error == True:
                messages.error(request, 'There is error in credentials.')
                return redirect('reset_password', reset_id = password_reset_id.reset_id)
            
            else:
                user = password_reset_id.user
                user.set_password(password)
                user.save()
                password_reset_id.delete()
                messages.success( request, 'Password Reset has been successful')
                return redirect('login')
    except PasswordReset.DoesNotExist:
        messages.error(request, 'The Password Reset Does Not Exist.')
        return redirect( 'reset_password', reset_id = PasswordReset.reset_id )
    return render(request, 'authenticate/reset_password.html')