from re import T
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Item(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    price = models.FloatField()
    # categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    mojodi = models.BooleanField(default=True)   
    image = models.ImageField(upload_to='Product Image', blank=True, null=True)
    text = models.TextField()
    description = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_single_product_url(self):
        return reverse('store:single-product', kwargs={
            'slug':self.slug,
            'pk':self.id
        })


class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateTimeField(blank=True, null=True)

    def __str__(self) -> str:
        return self.owner.username  


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField()
    count = models.IntegerField()

    @property
    def get_total_price(self):
        return self.price * self.count

    def __str__(self):
        return self.item.title
