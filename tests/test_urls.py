from django.test import SimpleTestCase
from django.urls import reverse, resolve

from eShop.views import home
from product_store.views import product_store, search_product, similar_product_suggestion
from product_cart.views import cart, add_product_to_cart, remove_product_from_cart, delete_cart_item
from product_order.views import place_order, make_payment, complete_order
from users.views import FirstNameValidation, LastNameValidation, EmailValidation, Registration, login, customer_dashboard, customer_orders, update_profile, update_password, forgot_password, reset_password, logout

class TestUrls(SimpleTestCase):
    
    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    
    def test_product_store_url_resolves(self):
        url = reverse('product_store')
        self.assertEquals(resolve(url).func, product_store)


    def test_cart_url_resolves(self):
        url = reverse('cart')
        self.assertEquals(resolve(url).func, cart)


    def test_search_product_url_resolves(self):
        url = reverse('search_product')
        self.assertEquals(resolve(url).func, search_product)


    def test_validate_first_name_url_resolves(self):
        url = reverse('validate_first_name')
        self.assertEquals(resolve(url).func.view_class, FirstNameValidation)


    def test_validate_last_name_url_resolves(self):
        url = reverse('validate_last_name')
        self.assertEquals(resolve(url).func.view_class, LastNameValidation)


    def test_validate_email_url_resolves(self):
        url = reverse('validate_email')
        self.assertEquals(resolve(url).func.view_class, EmailValidation)

        
    def test_registration_url_resolves(self):
        url = reverse('registration')
        self.assertEquals(resolve(url).func.view_class, Registration)


    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login)


    def test_customer_dashboard_url_resolves(self):
        url = reverse('customer_dashboard')
        self.assertEquals(resolve(url).func, customer_dashboard)


    def test_update_profile_url_resolves(self):
        url = reverse('update_profile')
        self.assertEquals(resolve(url).func, update_profile)


    def test_update_password_url_resolves(self):
        url = reverse('update_password')
        self.assertEquals(resolve(url).func, update_password)


    def test_forgot_password_url_resolves(self):
        url = reverse('forgot_password')
        self.assertEquals(resolve(url).func, forgot_password)


    def test_reset_password_url_resolves(self):
        url = reverse('reset_password')
        self.assertEquals(resolve(url).func, reset_password)


    def test_similar_product_suggestion_url_resolves(self):
        url = reverse('recommendation')
        self.assertEquals(resolve(url).func, similar_product_suggestion)


    def test_place_order_url_resolves(self):
        url = reverse('place_order')
        self.assertEquals(resolve(url).func, place_order)


    def test_make_payment_url_resolves(self):
        url = reverse('make_payment')
        self.assertEquals(resolve(url).func, make_payment)


    def test_complete_order_url_resolves(self):
        url = reverse('complete_order')
        self.assertEquals(resolve(url).func, complete_order)


    def test_customer_orders_url_resolves(self):
        url = reverse('customer_orders')
        self.assertEquals(resolve(url).func, customer_orders)


    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)
