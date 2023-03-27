from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from.import views
urlpatterns = [
    path('',views.index),
    path('vendorlogin',views.vendorlogin),
    path('vendorsignup',views.vendorsignup),
    path('vendor_register',views.vendor_register),
    path('vendor_login',views.vendor_login),
    path('vendor',views.vendor_profile),
    path('vendor_logout',views.vendor_logout),
    path('addproduct',views.add_product),
    path('add_product',views.addproduct),
    path('editproduct/<int:id>',views.edit_product),
    path('addimages',views.addimages),
    path('add_images',views.add_images),
    path('editproduct/update_product/<int:id>',views.update_product),
    path('productdetails/<int:id>',views.product_details),
    path('productdelete/<int:id>',views.product_delete),
    path('login',views.login),
    path('signup',views.signup),
    path('register',views.register),
    path('c_login',views.c_login),
    path('profile',views.customer_profile),
    path('c_logout',views.customer_logout),
    path('cart/<int:id>',views.cart),
    path('cartdetails',views.cartdetails),
    path('cartdelete/<int:id>',views.cartdelete),
    path('apidetails/<int:id>',views.apidetails),
    path('apicart/<int:id>',views.apicart),
    path('api_cartdelete/<int:id>',views.api_cartdelete),
    path('about',views.about),
    path('contact',views.contact),
    path('privacy',views.privacy),
    path('terms',views.terms),
    path('checkout/<int:id>',views.check),
    path('order',views.order_details),
    path('customer_order',views.customer_order),
    path('search',views.search),
    path('edit_profile/<int:id>',views.edit_profile)
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)