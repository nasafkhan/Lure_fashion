from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.forms import SignupForm
from accounts.models import Account
from .verification_otp import sendOTP, checkOTP
from django.contrib.auth.decorators import login_required
# Create your views here.


def sign_in(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('sign-in')
    return render(request, 'user/sign-in.html')

def sign_in_with_OTP(request):
    if request.method == 'POST':
        mobile = request.POST['phone']
        try:
            if Account.objects.get(phone_number = mobile).exist():
                sendOTP(mobile)
                request.session['has_mobile'] = mobile
                return redirect('verify_otp')
        except:
            messages.info(request, 'User is not registered')
    return render(request, 'user/otp_login.html')

def verify_otp(request):
    if request.method == 'POST':
        get_otp = request.POST['otp_code']
        mobile = request.session['has_mobile']
        otp_value = checkOTP(mobile,get_otp)
        if otp_value:
            return redirect('home')
        else:
            messages.error(request, 'OTP is not valid please try again')
            return 
        
    return render(request, 'user/otp_verify.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name  = form.cleaned_data['last_name']
            phone      = form.cleaned_data['phone']
            email      = form.cleaned_data['email']
            password   = form.cleaned_data['password']
            user_name  = first_name
            user = Account.objects.create_user(first_name = first_name, last_name = last_name,username = user_name,email = email,phone=phone, password = password)
            user.save()
            messages.success(request, 'Registration Successful.')
            return redirect('sign-up')
    else:
        form = SignupForm()
    context = {
        'form'  : form
    }
    return render(request, 'user/sign-up.html', context)

@login_required(login_url = 'sign-in')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('sign-in')



def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
            

            if user.is_superuser:
                auth.login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'You are not an admin')
                return redirect('dashboard')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('admin_login')

    else:
        return render(request,'adminpanel/admin_login.html')