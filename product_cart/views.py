from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from product_store.models import Product, Variation
from product_cart.models import Cart, CartProduct
from django.core.exceptions import ObjectDoesNotExist


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        
        if request.user.is_authenticated:
            cart_items = CartProduct.objects.filter(user=request.user, status=True)
        
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartProduct.objects.filter(cart=cart, status=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (total * (18/100)) # 18 is TZ VAT
        grand_total = total + tax
    
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'grand_total': grand_total,
        'quantity': quantity,
        'tax': tax,
        'cart_items': cart_items
    }

    return render(request, 'product/cart.html', context)


def add_product_to_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    #authenticated
    if current_user.is_authenticated:
        product_variation = []
        
        if request.method == 'POST':
            
            for item in request.POST:
                key = item
                value = request.POST[key]
                
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                
                except:
                    pass

        cart_item_exists = CartProduct.objects.filter(product=product, user=current_user).exists()
        
        if cart_item_exists:
            cart_item = CartProduct.objects.filter(product=product, user=current_user)
            existing_variation = []
            ids = []

            for item in cart_item:
                variations = item.variation.all()
                existing_variation.append(list(variations))
                ids.append(item.id)

            if product_variation in existing_variation:
                index = existing_variation.index(product_variation)
                item_id = ids[index]
                item = CartProduct.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            
            else:
                item = CartProduct.objects.create(product=product, quantity=1, user=current_user)
                
                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                
                item.save()
        
        else:
            cart_item = CartProduct.objects.create(
                product = product,
                quantity = 1,
                user=current_user,
            )

            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                
            cart_item.save()

        return redirect('cart')
    
    # not-authenticated
    else:
        product_variation = []

        if request.method == 'POST':

            for item in request.POST:
                key = item
                value = request.POST[key]

                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variation.append(variation)
                
                except:
                    pass
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))

        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
        
        cart.save()

        cart_item_exists = CartProduct.objects.filter(product=product, cart=cart).exists()

        if cart_item_exists:
            cart_item = CartProduct.objects.filter(product=product, cart=cart)
            existing_variation = []
            ids = []

            for item in cart_item:
                variations = item.variation.all()
                existing_variation.append(list(variations))
                ids.append(item.id)

            if product_variation in existing_variation:
                index = existing_variation.index(product_variation)
                item_id = ids[index]
                item = CartProduct.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartProduct.objects.create(product=product, quantity=1, cart=cart)

                if len(product_variation) > 0:
                    item.variation.clear()
                    item.variation.add(*product_variation)
                
                item.save()

        else:
            cart_item = CartProduct.objects.create(
                product = product,
                quantity = 1,
                cart = cart,
            )

            if len(product_variation) > 0:
                cart_item.variation.clear()
                cart_item.variation.add(*product_variation)
                
            cart_item.save()

        return redirect('cart')


def remove_product_from_cart(request, product_id, cart_product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.is_authenticated:
            cart_item = CartProduct.objects.get(product=product, user=request.user, id=cart_product_id)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartProduct.objects.get(product=product, cart=cart, id=cart_product_id)
    
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()

        else:
            cart_item.delete()
    
    except:
        pass

    return redirect('cart')


def delete_cart_item(request, product_id, cart_product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated:
        cart_item = CartProduct.objects.get(product=product, user=request.user, id=cart_product_id)
    
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartProduct.objects.get(product=product, cart=cart, id=cart_product_id)
    
    cart_item.delete()

    return redirect('cart')


@login_required(login_url='login') 
def checkout(request, total=0, quantity=0, cart_items=None):
    try: 
        tax = 0
        grand_total = 0
        
        if request.user.is_authenticated:
            cart_items = CartProduct.objects.filter(user=request.user, status=True)
            
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartProduct.objects.filter(cart=cart, status=True)
            
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (total * (18/100)) # 18 is TZ VAT
        grand_total = total + tax
    
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    
    return render(request, 'product/checkout.html', context)

