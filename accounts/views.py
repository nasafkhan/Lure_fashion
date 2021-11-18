from django.shortcuts import render, redirect
from django.contrib import messages, auth
from accounts.forms import SignupForm
from accounts.models import Account
from .verification_otp import sendOTP, checkOTP
from django.contrib.admin.views.decorators import staff_member_required
from twilio.base.exceptions import TwilioRestException

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
            Account.objects.get(phone=mobile)
            sendOTP(mobile)
            request.session['has_mobile'] = mobile
            return redirect('verify_otp')
        except:
            messages.info(request, "User is not registered!")
    return render(request, 'user/otp_login.html')

def verify_otp(request):
    if request.method == 'POST':
        get_otp = request.POST['otp_code']
        mobile = request.session['has_mobile']
        otp_value = checkOTP(mobile,get_otp)
        if otp_value:
            user=Account.objects.get(phone=mobile)
            auth.login(request,user) 
            return redirect('home')
        else:
            messages.error(request, 'OTP is not valid please try again')
            return redirect(request, 'verify_otp')
        
    return render(request, 'user/otp_verify.html')


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone      = form.cleaned_data['phone']
            email      = form.cleaned_data['email']
            password   = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            request.session['username'] = username
            request.session['phone']  = phone
            request.session['email'] = email
            request.session['password'] = password

            if password == confirm_password:
                if Account.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already taken!')
                    return redirect('sign-up')

                elif Account.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already taken!')
                    return redirect('sign-up')

                elif Account.objects.filter(phone=phone).exists():
                    messages.info(request, 'Phone number is already taken!')
                    return redirect('sign-up')

                else:
                    try:
                        sendOTP(phone)
                        messages.success(request, 'Please verfiy your account with the OTP sent to your mobile')
                        return redirect('verify_account')
                    except TwilioRestException:
                        messages.error(request, 'Enter a valid mobile number')                  
    else:
        form = SignupForm()
    context = {
        'form'  : form
    }
    return render(request, 'user/sign-up.html', context)

def verify_account(request):
    username = request.session['username']
    email    = request.session['email']
    phone    = request.session['phone']
    password = request.session['password']

    if request.method == 'POST':
        otp = request.POST['otp_code']
        try:
            mobile = request.session['phone']
        except KeyError:
            messages.error(request, )
        verified =  checkOTP(mobile, otp)
        if verified:
            user = Account.objects.create_user(username = username, phone=phone, email=email, password=password )
            user.save()
            del request.session['username']
            del request.session['phone']
            del request.session['email']
            del request.session['password']
            return redirect('home')
    return render(request, 'user/otp_verify.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'You are logged out.')
        return redirect('sign-in')


def admin_login(request):
    if request.user.is_authenticated:
        return redirect ('dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_superuser:
                auth.login(request,user)
                return redirect('dashboard')
            else:
                messages.info(request, 'You are not an admin')
                return redirect('dashboard')

        else:
            messages.info(request,'Invalid Credentials')
            return redirect('admin_login')

    else:
        return render(request,'adminpanel/admin_login.html')


@staff_member_required(login_url='access_denied')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')


def access_denied(request):
    return render(request, 'adminpanel/access_denied.html')