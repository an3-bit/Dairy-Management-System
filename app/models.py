from django.contrib.auth.models import User
from django.db import models

# Create your models here.
TOWN_CHOICES = {
    ("Nairobi", "Rongai"),
    ("Mombasa", "Nyali"),
    ("Kisumu", "K'Ogelo"),
    ("Nakuru", "Njiru"),
    ("Eldoret", "Moiben"),
    ("Thika", "Kiamaiko"),
    ("Kitale", "Kajibroa"),
    ("Malindi", "Tendawema"),
    ("Garissa", "Kainuk"),
    ("Nyeri", "Mathira" ),
}




CATEGORY_CHOICES = {
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','Lassi'),
    ('MS', 'Milkshake'),
    ('PN','Paneer'),
    ('GH','Ghee'),
    ('CZ','Cheese'),
    ('IC','Ice-Creams')
}


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description =models.TextField()
    composition = models.TextField(default='')
    propapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return self.title

class Customer(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    name= models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    mobile=models.IntegerField(default=0)
    zipcode=models.IntegerField()
    town=models.CharField(choices=TOWN_CHOICES, default='Unknown', max_length=100)
    def __str__(self):
        return self.name
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')  # Ensure each product appears only once per user

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"