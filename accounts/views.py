from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from accounts.forms import SignupForm, UserForm, UserProfileForm
from accounts.models import Account, UserProfile
from cart.models import Cart, CartItem
from orders.models import Order, OrderProduct
from cart.views import _cart_id
from .verification_otp import sendOTP, checkOTP
from django.contrib.admin.views.decorators import staff_member_required
from twilio.base.exceptions import TwilioRestException
import requests


# Create your views here.
def sign_in(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(
                    cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
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
        otp_value = checkOTP(mobile, get_otp)
        if otp_value:
            user = Account.objects.get(phone=mobile)
            auth.login(request, user)
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
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            request.session['username'] = username
            request.session['phone'] = phone
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
                        messages.success(
                            request,
                            'Please verfiy your account with the OTP sent to your mobile'
                        )
                        return redirect('verify_account')
                    except TwilioRestException:
                        messages.error(request, 'Enter a valid mobile number')
    else:
        form = SignupForm()
    context = {'form': form}
    return render(request, 'user/sign-up.html', context)


def verify_account(request):
    username = request.session['username']
    email = request.session['email']
    phone = request.session['phone']
    password = request.session['password']

    if request.method == 'POST':
        otp = request.POST['otp_code']
        try:
            mobile = request.session['phone']
        except KeyError:
            messages.error(request, )
        verified = checkOTP(mobile, otp)
        if verified:
            user = Account.objects.create_user(username=username,
                                               phone=phone,
                                               email=email,
                                               password=password)
            user.save()

            # Create a user profile
            profile = UserProfile()
            profile.user_id = user.id
            profile.phone = phone
            profile.profile_picture = 'default/default_avatar.png'
            profile.save()

            del request.session['username']
            del request.session['phone']
            del request.session['email']
            del request.session['password']
            return redirect('home')
    return render(request, 'user/otp_verify.html')


@login_required(login_url='sign-in')
def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request, 'You are logged out.')
        return redirect('sign-in')


# user dashboard views


@login_required(login_url='sign-in')
def dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(
        user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    # userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        # 'userprofile': userprofile,
    }
    return render(request, 'user/dashboard.html', context)


@login_required(login_url='sign-in')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,
                                  is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'user/my_orders.html', context)


@login_required(login_url='sign-in')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST,
                                       request.FILES,
                                       instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    print(profile_form)
    return render(request, 'user/edit_profile.html', context)


@login_required(login_url='sign-in')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'user/change_password.html')


@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'user/order_detail.html', context)


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
            messages.info(request, 'Invalid Credentials')
            return redirect('admin_login')

    else:
        return render(request, 'adminpanel/admin_login.html')


@staff_member_required(login_url='access_denied')
def admin_logout(request):
    auth.logout(request)
    return redirect('admin_login')


def access_denied(request):
    return render(request, 'adminpanel/access_denied.html')