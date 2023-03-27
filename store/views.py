from django.shortcuts import redirect,render
from store.models import Product
from store.models import Vendor
from store.models import Product_images
from store.models import Customer
from datetime import datetime
from django.db.models import Q
from store.models import Carts
import requests
from store.models import Products_api
from store.models import Api_cart
import json
from django.core.paginator import Paginator
from store.models import Order
# Create your views here.
def index(request):
    product=Product.objects.all()
    product_api=Products_api.objects.all()
    if request.session['vendor']==True:
        data=request.session['vendor_id']
        return render(request,'content/index.html',{'product':product,'data':data,'product_api':product_api})
    elif request.session['customer']==True:
        data=request.session['customer_id']
        return render(request,'content/index.html',{'product':product,'customer':data,'product_api':product_api})

    else:
        return render(request,'content/index.html',{'product':product,'product_api':product_api})
def vendorsignup(request): 
    return render(request,'vendor/vendor_signup.html')
def vendorlogin(request):
    if request.session['vendor']==True:
        return redirect('/vendor')
    elif request.session['customer']==True:
        return redirect('/profile')
    else:
        return render(request,'vendor/vendor_login.html')
def vendor_register(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        contact=request.POST.get('contact')
        image=request.FILES['image']
        pincode=request.POST.get('pin')
        company_name=request.POST.get('company')
        if name != '' and email != '' and password != '':
             vendor=Vendor(fullname=name,email=email,password=password,address=address,contact=contact,image=image,pincode=pincode,company_name=company_name)
             vendor.save()
             return redirect('/vendorlogin')
        else:
            return redirect('/vendorsignup')
def vendor_login(request):
    message=''
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            vendor=Vendor.objects.get(email=email)
            if vendor.password==password:
                request.session['vendor']=True
                request.session['vendor_email']=vendor.email
                request.session['vendor_id']=vendor.id
                return redirect('/vendor')
        except:
            message='Invalid User id or Password!!'
            #return redirect('/vendorlogin')
            return render(request,'vendor/vendor_login.html',{'message':message})
            
def vendor_profile(request):
    if request.session['vendor']==True:
        email=request.session['vendor_email']
        vendor_id=request.session['vendor_id']
        vendor=Vendor.objects.get(email=email)
        product=Product.objects.filter(vendor_id=vendor_id)
        paginator = Paginator(product, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'vendor/vendor_profile.html',{'vendor':vendor,'product':page_obj})
    else:
        return redirect('/vendorlogin')
def vendor_logout(request):
    request.session['vendor']=False
    return redirect('/vendorlogin')
def add_product(request):
    if request.session['vendor']==True:
        return render(request,'vendor/add_product.html')
    else:
        return redirect('/vendorlogin')
def addproduct(request):
    if request.method=="POST":
        title=request.POST.get('title')
        description=request.POST.get('description')
        price=request.POST.get('price')
        discountPercentage=request.POST.get('discountPercentage')
        rating=request.POST.get('rating')
        stock=request.POST.get('stock')
        brand=request.POST.get('brand')
        category=request.POST.get('category')
        thumbnali=request.FILES['thumbnali']
        vendor=request.session['vendor_id']
        product=Product.objects.create(title=title,description=description,price=price,discountPercentage=discountPercentage,rating=rating,stock=stock,brand=brand,category=category,thumbnali=thumbnali,vendor_id=vendor)
        product.save()
        return redirect('/vendor')
def edit_product(request,id):
    if request.session['vendor']==True:
        product=Product.objects.get(id=id)
        request.session['product_id']=id
        return render(request,'vendor/edit_product.html',{'product':product})
    else:
        return redirect('/vendorlogin')
def addimages(request):
    if request.session['vendor']==True:
        return render(request,'vendor/add_images.html')
    else:
        return redirect('/vendorlogin')
def add_images(request):
    if request.method=="POST":
        images=request.FILES.getlist('image')
        p_id=request.session['product_id']
        for image in images:
            product_image=Product_images(product_images=image,product_id=p_id)
            product_image.save()
        return redirect('/vendor')
def update_product(request,id):
    if request.method=="POST":
        title=request.POST.get('title')
        price=request.POST.get('price')
        discountPercentage=request.POST.get('discountPercentage')
        description=request.POST.get('description')
        product=Product.objects.get(id=id)
        product.title=title
        product.price=price
        product.discountPercentage=discountPercentage
        product.description=description
        product.save()
        return redirect('/vendor')
def product_details(request,id):
    product=Product.objects.get(id=id)
    img=Product_images.objects.filter(product_id=id)
    item_already_exist=False
    if request.session['customer_id'] and request.session['customer']==True:
        customer=request.session['customer_id']
        item_already_exist=Carts.objects.filter(Q(product_id=product.id) & Q(customer_id=customer)).exists()
    if request.session['vendor']==True:
        data=request.session['vendor_id']
        return render(request,'content/product_details.html',{'product':product,'data':data,'item_already_exist':item_already_exist})
    elif request.session['customer']==True:
        data=request.session['customer_id']
        return render(request,'content/product_details.html',{'product':product,'customer':data,'item_already_exist':item_already_exist})
    else:
        return render(request,'content/product_details.html',{'product':product,'img':img,'item_already_exist':item_already_exist})
def product_delete(request,id):
    if request.session['vendor']==True:
            product=Product.objects.get(id=id)
            product.delete()
            return redirect('/vendor')
    else:
        return redirect('/vendorlogin')
def login(request):
    if request.session['customer']==True:
        return redirect('/profile')
    else:
        return render(request,'customer/customer_login.html')
def signup(request):
    return render(request,'customer/customer_signup.html')
def register(request):
    if request.method=="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        address=request.POST.get('address')
        contact=request.POST.get('contact')
        image=request.FILES['image']
        pincode=request.POST.get('pin')
        if name != '' and email != '' and password != '':
             customer=Customer(fullname=name,email=email,password=password,address=address,contact=contact,image=image,pincode=pincode)
             customer.save()
             return redirect('/login')
        else:
            return redirect('/login')
def c_login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            customer=Customer.objects.get(email=email)
            if customer.password==password:
                request.session['customer']=True
                request.session['customer_email']=customer.email
                request.session['customer_id']=customer.id
                return redirect('/profile')
        except:
            return redirect('/login')
def customer_profile(request):
    if request.session['customer']==True:
        c_id=request.session['customer_id']
        customer=Customer.objects.get(id=c_id)
        return render(request,'customer/customer_profile.html',{'user':customer})
    else:
        return redirect('/login')
def customer_logout(request):
    request.session['customer']=False
    return redirect('/login')
def cart(request,id):
    p_id=id
    user=request.session['customer_id']
    cart=Carts(product_id=p_id,customer_id=user,date=datetime.today())
    cart.save()
    return redirect('/cartdetails')
def cartdetails(request):
    if request.session['customer']==False:
        return redirect('/')
    c_id=request.session['customer_id']
    cart=Carts.objects.filter(customer_id=c_id) 
    api_cart=Api_cart.objects.filter(customer_id=c_id)
    product=[]
    api_product=[]
    for i in cart:
        p=Product.objects.get(id=i.product_id)
        product.append(p)
    for j in api_cart:
        q=Products_api.objects.get(id=j.api_product_id)
        api_product.append(q)
    if request.session['vendor']==True:
        data=request.session['vendor_id']
        return render(request,'content/cartdetails.html',{'cart':product,'data':data,'api_cart':api_product})
    elif request.session['customer']==True:
        data=request.session['customer_id']
        return render(request,'content/cartdetails.html',{'cart':product,'customer':data,'api_cart':api_product})
    else:
        return render(request,'content/cartdetails.html',{'cart':product,'api_cart':api_product})
def cartdelete(request,id):
    c_id=request.session['customer_id']
    cart=Carts.objects.filter(Q(product_id=id) & Q(customer_id=c_id))
    cart.delete()
    return redirect('/cartdetails')
def apidetails(request,id):
    product=Products_api.objects.get(id=id)
    item_already_exist=False
    if request.session['customer_id'] and request.session['customer']==True:
        customer=request.session['customer_id']
        item_already_exist=Api_cart.objects.filter(Q(api_product_id=product.id) & Q(customer_id=customer)).exists()
    if request.session['vendor']==True:
        data=request.session['vendor_id']
        return render(request,'content/api_product.html',{'product':product,'data':data,'item_already_exist':item_already_exist})
    elif request.session['customer']==True:
        data=request.session['customer_id']
        return render(request,'content/api_product.html',{'product':product,'customer':data,'item_already_exist':item_already_exist})
    else:
        return render(request,'content/api_product.html',{'product':product,'item_already_exist':item_already_exist})
def apicart(request,id):
    p_id=id
    user=request.session['customer_id']
    cart=Api_cart(api_product_id=p_id,customer_id=user,date=datetime.today())
    cart.save()
    return redirect('/cartdetails')
def api_cartdelete(request,id):
    c_id=request.session['customer_id']
    cart=Api_cart.objects.get(Q(api_product_id=id) & Q(customer_id=c_id))
    cart.delete()
    return redirect('/cartdetails')
def about(request):
    return render(request,'content/about.html')
def contact(request):
    return render(request,'content/contact.html')
def privacy(request):
    return render(request,'content/privacy.html')
def terms(request):
    return render(request,'content/terms.html')
def check(request,id):
    product=Product.objects.get(id=id)
    product_price=int(product.price)
    discount=int(product.discountPercentage)
    discount_price=(product_price*discount)/100
    total_price=product_price-discount_price
    if request.session['customer']==True:
        if request.method=="POST":
            delivery_address=request.POST.get('address')
            c_id=request.session['customer_id']
            p_id=id
            order=Order(delivary_address=delivery_address,order_date=datetime.today(),customer_id=c_id,product_id=p_id)
            order.save()
            cart=Carts(customer_id=c_id,product_id=p_id,date=datetime.today())
            cart.save()
            return redirect('/order')
        return render(request,'content/checkout.html',{'product':product,'total_price':total_price})
    else:
        return redirect('/login')
def order_details(request):
    c_id=request.session['customer_id']
    order=Order.objects.filter(customer_id=c_id)
    order_id=[]
    for i in order:
        product=Product.objects.get(id=i.product_id)
        order_id.append(product)
    return render(request,'content/order_details.html',{'product':order_id})
def customer_order(request):
    order=Order.objects.all()
    vendor_id=request.session['vendor_id']
    product=[]
    customer=[]
    for i in order:
        p=Product.objects.get(id=i.product_id)
        c=Customer.objects.get(id=i.customer_id)
        if p.vendor_id==vendor_id:
            product.append(p)
            customer.append(c)
    return render(request,'vendor/customer_order.html',{'order':product,'customer':customer})
def search(request):
    if request.method=="POST":
        search=request.POST.get('search')
        product=Product.objects.filter(category=search)
        if request.session['vendor']==True:
            data=request.session['vendor_id']
            return render(request,'content/ajax_search.html',{'product':product,'data':data})
        elif request.session['customer']==True:
            data=request.session['customer_id']
            return render(request,'content/ajax_search.html',{'product':product,'customer':data})
        else:
            return render(request,'content/ajax_search.html',{'product':product})
def edit_profile(request,id):
    user=Customer.objects.get(id=id)
    if request.session['customer']==True:
        if request.method=="POST":
            name=request.POST.get('name')
            address=request.POST.get('address')
            pin=request.POST.get('pin')
            mobile=request.POST.get('mobile')
            email=request.POST.get('email')
            cpassword=request.POST.get('c_password')
            npassword=request.POST.get('n_password')
            if cpassword==user.password:
                user.fullname=name
                user.address=address
                user.pincode=pin
                user.contact=mobile
                user.email=email
                user.password=npassword
                user.save()
                message="Profile updated successfully"
                return render(request,'customer/edit_profile.html',{'user':user,'s_message':message})
            else:
                message="Password doesn't match"
                return render(request,'customer/edit_profile.html',{'user':user,'f_message':message})
        else:
            return render(request,'customer/edit_profile.html',{'user':user})
    else:
        return redirect('/login')