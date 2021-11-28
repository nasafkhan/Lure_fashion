from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Order
from .forms import OrderForm
import datetime
from forex_python.converter import CurrencyRates
from cart.models import CartItem


# Create your views here.
def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_item_count = cart_items.count()
    if cart_item_count <= 0:
        return redirect('home')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (18 * total) / 100
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            # Store all the billing information inside Order table
            data = Order()
            data.user          = current_user
            data.first_name    = form.cleaned_data['first_name']
            data.last_name     = form.cleaned_data['last_name']
            data.phone         = form.cleaned_data['phone']
            data.company_name  = form.cleaned_data['company_name']
            data.email         = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.landmark      = form.cleaned_data['landmark']
            data.city          = form.cleaned_data['city']
            data.state         = form.cleaned_data['state']
            data.postcode      = form.cleaned_data['postcode']
            data.order_notes   = form.cleaned_data['order_notes']
            data.order_total   = grand_total
            data.tax           = tax
            data.ip            = request.META.get('REMOTE_ADDR')
            data.save()

            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            convert_currency = CurrencyRates()
            converted_amount = convert_currency.convert('INR', 'USD', grand_total)
            print("convert currency:", converted_amount)

            order = Order.objects.get(user=current_user, order_number=order_number)
            context = {
                'order' : order,
                'cart_items' : cart_items,
                'total' : total,
                'tax' : tax,
                'grand_total' : grand_total, 
                'converted_amount' : converted_amount
            }

            return render(request, 'user/review_order.html', context)
    else:
        return redirect('checkout')
