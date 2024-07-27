from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from product_cart.models import CartProduct
from product_store.models import Product
from .models import Order, Payment, ProductOrder
import datetime
import json 



def place_order(request, total=0, quantity=0,):
    current_user = request.user
    cart_items = CartProduct.objects.filter(user=current_user)
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('product_store')

    grand_total = 0
    tax = 0

    for cart_item in cart_items:
        total += (cart_item.product.selling_price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (total * (18/100)) # 18 is TZ VAT
    grand_total = total + tax

    if request.method == 'POST':
        form = OrderForm(request.POST)
        
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.country = form.cleaned_data['country']
            data.city = form.cleaned_data['city']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.save()
            # order-number = year+month+date+orderid
            year = int(datetime.date.today().strftime('%Y'))
            day = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            current_day = datetime.date(year,month,day)
            current_date = current_day.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
            }

            return render(request, 'order/payment.html', context)
    
    else:
        return redirect('checkout')


def make_payment(request):
    # get-transaction-details-from-paypal-and-store-inside-payment-table
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID']) 

    payment = Payment(
        user = request.user,
        payment_id = body['transactionID'],
        payment_method = body['paymentMethod'],
        amount = order.order_total,
        status = body['status']
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()
    # transfer-all-products-from-cart-to-product-order-table
    products_in_cart = CartProduct.objects.filter(user=request.user)

    for item in products_in_cart:
        product_order = ProductOrder()
        product_order.order_id = order.id
        product_order.payment = payment
        product_order.user_id = request.user.id
        product_order.product_id = item.product_id
        product_order.quantity = item.quantity
        product_order.product_price = item.product.selling_price
        product_order.is_ordered = True
        product_order.save()
        # store-product-variation(many-to-many)
        product_in_cart = CartProduct.objects.get(id=item.id)
        variation = product_in_cart.variation.all()
        product_order = ProductOrder.objects.get(id=product_order.id)
        product_order.variation.set(variation)
        product_order.save()
        # reduce-stock-according-to-quantity-of-sold-products
        product = Product.objects.get(id=item.product_id)
        product.product_stock -= item.quantity
        product.save()

    # on-success-delete-all-product-inside-cart
    CartProduct.objects.filter(user=request.user).delete()
    # send-order-email-to-customer
    mail_subject = 'Thank you for your order!'
    message = render_to_string('order/received-order.html', {
        'user': request.user,
        'order': order,
    })
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    # send-orderNumber-and-transactionID-back-to-sendDataFromPayPal()-via-JsonResponse
    data = {
        'order_number': order.order_number,
        'transactionID': payment.payment_id,
    }

    return JsonResponse(data)

    return render(request, 'order/payment.html')


def complete_order(request):
    order_number = request.GET.get('order_number')
    transactionID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        product_orders = ProductOrder.objects.filter(order_id=order.id)

        subtotal = 0
        for product in product_orders:
            subtotal += product.product_price * product.quantity

        payment = Payment.objects.get(payment_id=transactionID)

        context = {
            'order': order,
            'product_orders': product_orders,
            'order_number': order.order_number,
            'transactionID': payment.payment_id,
            'payment': payment,
            'subtotal': subtotal
        }
        
        return render(request, 'order/complete-order.html', context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('home')
