from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Manager(models.Manager):
    def get_product_by_category(self, category_slug):
        return self.get_queryset().filter(categories__category_slug__iexact=category_slug, actice=True)


class Category(models.Model):
    category_name = models.CharField(max_length=100)
    category_slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.category_name


class Item(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    price = models.FloatField()
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    mojodi = models.BooleanField(default=True)   
    image = models.ImageField(upload_to='Product Image', blank=True, null=True)
    text = models.TextField()
    description = models.TextField()
    active = models.BooleanField(default=False)
    objects = Manager()

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

    def get_total_price(self):
        amount = 0
        for detail in self.orderdetail_set.all():
            amount += detail.price * detail.count
        return amount


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField()
    count = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def get_total_price(self):
        return self.price * self.count

    def __str__(self):
        return self.item.title
