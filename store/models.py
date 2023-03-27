from django.db import models

# Create your models here.
class Vendor(models.Model):
    fullname=models.CharField(max_length=122,null=False)
    email=models.EmailField(max_length=122,null=False)
    password=models.CharField(max_length=122,null=False)
    address=models.TextField()
    contact=models.CharField(max_length=15)
    image=models.FileField(upload_to='profile_image')
    pincode=models.CharField(max_length=6,null=False)
    company_name=models.CharField(max_length=122,null=False)
class Product(models.Model):
    title=models.CharField(max_length=122,null=False)
    description=models.TextField()
    price=models.CharField(max_length=122)
    discountPercentage=models.CharField(max_length=122)
    rating=models.CharField(max_length=122)
    stock=models.CharField(max_length=122)
    brand=models.CharField(max_length=122)
    category=models.CharField(max_length=122)
    thumbnali=models.FileField(upload_to="product_image")
    vendor=models.ForeignKey(Vendor,on_delete=models.CASCADE)
class Customer(models.Model):
    fullname=models.CharField(max_length=122,null=False)
    email=models.EmailField(max_length=122,unique=True,null=False)
    password=models.CharField(max_length=122)
    address=models.TextField()
    contact=models.CharField(max_length=15,unique=True)
    image=models.ImageField(upload_to='profile_image')
    pincode=models.CharField(max_length=6,null=False)
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    delivary_address=models.TextField()
    order_date=models.DateField()
class Delivary(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    excepted_delivary_date=models.DateField()
    delivary_status=models.TextField()
    delivaried_date=models.DateField()
class Product_images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    product_images=models.FileField(upload_to="product_image")
class Products_api(models.Model):
    title=models.CharField(max_length=100)
    price=models.FloatField()
    description=models.TextField()
    category=models.TextField()
    image_url=models.CharField(max_length=100) 
class Carts(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    date=models.DateField()
class Api_cart(models.Model):
    api_product=models.ForeignKey(Products_api,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    date=models.DateField()