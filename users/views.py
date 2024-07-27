from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import JsonResponse
from django.contrib import messages, auth
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from users.models import Account
from validate_email import validate_email
from product_cart.views import _cart_id
from product_cart.models import Cart, CartProduct
from product_order.models import Order, ProductOrder
from .models import Account, UserProfile, Vendor
import json
import requests



# vendor

class VendorFirstNameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        first_name = data['first_name']

        if not str(first_name).isalnum():
            return JsonResponse({'first_name_error': 'First name should contains only alphanumeric characters'}, status=400)

        return JsonResponse({'first_name_valid': True})

class VendorLastNameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        last_name = data['last_name']

        if not str(last_name).isalnum():
            return JsonResponse({'last_name_error': 'Last name should contains only alphanumeric characters'}, status=400)

        return JsonResponse({'last_name_valid': True})

class VendorEmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid email address'}, status=400)

        if Account.objects.filter(email=email).exists():
            return JsonResponse({'email_error': ' Email is already taken, try another one'}, status=409)

        return JsonResponse({'email_valid': True})

class VendorRegistration(View): 
    def get(self, request):
        return render(request, 'authentication/vendor/registration.html')

    def post(self, request):
        if request.method == "POST":
            first_name = request.POST.get("first_name") 
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            username = email.split("@")[0]
            is_staff = '1'

            context = {
                'input_values': request.POST
            }

            if password == "":
                messages.error(
                    request, 'Fill in all required fields')
                return render(request, 'authentication/vendor/registration.html', context)

            if len(password) < 8:
                messages.error(
                    request, 'Password length must be greater than 7 characters.')
                return render(request, 'authentication/vendor/registration.html', context)

            
            elif password != confirm_password:
                messages.error(request, 'Password does not match')
                return render(request, 'authentication/vendor/registration.html', context)
            
            
            elif Account.objects.filter(email=email).exists():
                messages.error(
                    request, 'This email is already taken, try another one')
                return render(request, 'authentication/vendor/registration.html', context)
            
            else:
                user = Account.objects.create_user(
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    is_staff = is_staff,
                    username=username)
                
                user.set_password(password)
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Account activation notification'
                message = render_to_string('authentication/verification.html', {
                    'user': user,
                    'domain': current_site,
                    #encode-primary-key
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    #create-unique-token
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                return redirect('/authentication/login/?command=verification&email='+email)

def activate_vendor_account(request, uidb64, token):
    try:
        #decode-primary-key
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True 
        user.save()
        messages.success(
            request, 'Account is successful activated!')
        return redirect('vendor_login')

    else:
        messages.error(request, 'Invalid activation link')
        return redirect('vendor_registration')
 
@login_required(login_url='login')
def vendor_dashboard(request):
    return render(request, 'vendor/dashboard.html')

# customer 
class FirstNameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        first_name = data['first_name']

        if not str(first_name).isalnum():
            return JsonResponse({'first_name_error': 'First name should contains only alphanumeric characters'}, status=400)

        return JsonResponse({'first_name_valid': True})


class LastNameValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        last_name = data['last_name']

        if not str(last_name).isalnum():
            return JsonResponse({'last_name_error': 'Last name should contains only alphanumeric characters'}, status=400)

        return JsonResponse({'last_name_valid': True})


class EmailValidation(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Invalid email address'}, status=400)

        if Account.objects.filter(email=email).exists():
            return JsonResponse({'email_error': ' Email is already taken, try another one'}, status=409)

        return JsonResponse({'email_valid': True})


class Registration(View): 
    def get(self, request):
        return render(request, 'authentication/registration.html')

    def post(self, request):
        if request.method == "POST":
            first_name = request.POST.get("first_name") 
            last_name = request.POST.get("last_name")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")
            username = email.split("@")[0]

            context = {
                'input_values': request.POST
            }

            if password == "":
                messages.error(
                    request, 'Fill in all required fields')
                return render(request, 'authentication/registration.html', context)

            if len(password) < 8:
                messages.error(
                    request, 'Password length must be greater than 7 characters.')
                return render(request, 'authentication/registration.html', context)

            
            elif password != confirm_password:
                messages.error(request, 'Password does not match')
                return render(request, 'authentication/registration.html', context)
            
            
            elif Account.objects.filter(email=email).exists():
                messages.error(
                    request, 'This email is already taken, try another one')
                return render(request, 'authentication/registration.html', context)
            
            else:
                user = Account.objects.create_user(
                    first_name=first_name, 
                    last_name=last_name, 
                    email=email, 
                    username=username)
                
                user.set_password(password)
                user.save()

                current_site = get_current_site(request)
                mail_subject = 'Account activation notification'
                message = render_to_string('authentication/verification.html', {
                    'user': user,
                    'domain': current_site,
                    #encode-primary-key
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    #create-unique-token
                    'token': default_token_generator.make_token(user),
                })
                to_email = email
                send_email = EmailMessage(mail_subject, message, to=[to_email])
                send_email.send()

                return redirect('/authentication/login/?command=verification&email='+email)


def activate_customer_account(request, uidb64, token):
    try:
        #decode-primary-key
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, 'Account is successful activated!')
        return redirect('login')

    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password) 

        if user is not None and user.is_staff == 1:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists = CartProduct.objects.filter(cart=cart).exists()
                
                if cart_item_exists:
                    cart_item = CartProduct.objects.filter(cart=cart)
                   
                    #get-product-variation
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))
                    
                    #get-cart-items-from-customer-to-access-product-variation
                    cart_item = CartProduct.objects.filter(user=user)
                    existing_variation = [] 
                    ids = []
                    
                    for item in cart_item:
                        product_variations = item.variation.all()
                        existing_variation.append(list(product_variations))
                        ids.append(item.id)

                    #check-products-found-in-product_variation-and-existing_variation
                    for product in product_variation:
                        if product in existing_variation:
                            index = existing_variation.index(product)
                            item_id = ids[index]
                            item = CartProduct.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        
                        else:
                            cart_item = CartProduct.objects.filter(cart=cart)
                            
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            
            try:
                query = requests.utils.urlparse(url).query
                #next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            
            except:
                return redirect('vendor_dashboard')
        
        
        if user is not None and user.is_staff == 0:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item_exists = CartProduct.objects.filter(cart=cart).exists()
                
                if cart_item_exists:
                    cart_item = CartProduct.objects.filter(cart=cart)
                   
                    #get-product-variation
                    product_variation = []
                    for item in cart_item:
                        variation = item.variation.all()
                        product_variation.append(list(variation))
                    
                    #get-cart-items-from-customer-to-access-product-variation
                    cart_item = CartProduct.objects.filter(user=user)
                    existing_variation = [] 
                    ids = []
                    
                    for item in cart_item:
                        product_variations = item.variation.all()
                        existing_variation.append(list(product_variations))
                        ids.append(item.id)

                    #check-products-found-in-product_variation-and-existing_variation
                    for product in product_variation:
                        if product in existing_variation:
                            index = existing_variation.index(product)
                            item_id = ids[index]
                            item = CartProduct.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        
                        else:
                            cart_item = CartProduct.objects.filter(cart=cart)
                            
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            
            auth.login(request, user)
            url = request.META.get('HTTP_REFERER')
            
            try:
                query = requests.utils.urlparse(url).query
                #next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            
            except:
                return redirect('customer_dashboard')

        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
        

    return render(request, 'authentication/login.html')


@login_required(login_url='login')
def customer_dashboard(request):
    return render(request, 'customer/dashboard.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You have successful logged out.')
    return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = 'Reset password'
            message = render_to_string('authentication/password-reset-verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(
                request, 'Password reset link has been sent to your email.')

            return redirect('login')

        else:
            messages.error(request, 'Email does not exist!')
            return redirect('forgot_password')

    return render(request, 'authentication/forgot-password.html')


def password_validation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Create new password')

        return redirect('reset_password')

    else:
        messages.error(request, 'Link has been expired!')

        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password created successful')

            return redirect('login')

        else:
            messages.error(request, 'Password does not match!')

            return redirect('reset_password')
    else:
        return render(request, 'authentication/reset-password.html')


@login_required(login_url = 'login')
def customer_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-order_date')
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    context = {
        'orders': paged_orders,
    }
    return render(request, 'customer/order.html', context)



@login_required(login_url = 'login')
def vendor_orders(request):
    orders = Order.objects.filter(is_ordered=True).order_by('-order_date')
    paginator = Paginator(orders, 10)
    page = request.GET.get('page')
    paged_orders = paginator.get_page(page)

    context = {
        'orders': paged_orders,
    }
    return render(request, 'vendor/order.html', context)


@login_required(login_url = 'login')
def order_detail(request, order_id):
    order_detail = ProductOrder.objects.filter(order__order_number=order_id)
    order =  Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail' : order_detail,
        'order' : order,
        'subtotal' : subtotal,
    }

    return render(request, 'customer/invoice.html', context)


@login_required(login_url = 'login')
def update_profile(request):

    if request.method == 'POST': 
        user_id = request.POST['user_id']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        town = request.POST['town']
        
        if UserProfile.objects.filter(user_id=user_id).exists():
            messages.success(request, 'Profile has been updated.')
            return redirect('customer_dashboard')
        
        else: 
            profile = UserProfile()
            profile.address_line_1 = address_line_1
            profile.address_line_2 = address_line_2
            profile.city = city 
            profile.town = town
            profile.user_id = user_id
        
            profile.save()

            messages.success(request, 'Profile has been updated.')

        return redirect('customer_dashboard')

    return render(request, 'customer/update-profile.html')


@login_required(login_url = 'login')
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password successful changed!')
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'Enter correct current password!')
                return redirect('update_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('update_password')
    return render(request, 'customer/update-password.html')