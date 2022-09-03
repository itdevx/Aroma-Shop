from django.utils import timezone
from http import client
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import View, ListView
from store.models import OrderDetail
from store.models import Order
from store import models
from store.models import Item as Product
from store import forms
from django.contrib.auth.decorators import login_required
import datetime
from django.db.models import Count
# zarinpall
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
import requests
import json
from zeep import Client


class IndexView(View):
    def get(self, request):
        days = datetime.datetime.today() - datetime.timedelta(days=7)

        c = {
            'details': None,
            'products': Product.objects.filter(active=True).order_by('-id')[:4],
            'best_product': Product.objects.filter(orderdetail__date_added__lte=datetime.datetime.today(), orderdetail__date_added__gt=days).annotate(count=Count('orderdetail__count')).order_by('-count')[:5]
        }

        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if open_order is not None:
            c['details'] = open_order.orderdetail_set.all()

        return render(request, 'index.html', c)


class SingleProduct(View):
    template_name = 'single-product.html'
    def get(self, request, slug, pk):
        product = get_object_or_404(Product, slug=slug, id=pk, active=True)
        c = {
            'details': None,
            'product':product,
            'new_order_form' : forms.UserNewOrderForm(request.POST or None, initial={'item_id':pk}),
        }

        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if open_order is not None:
            c['details'] = open_order.orderdetail_set.all()

        return render(request, self.template_name, c)


@login_required(login_url='account:login')
def add_user_order(request):
    new_order_form = forms.UserNewOrderForm(request.POST or None)
    if new_order_form.is_valid():

        # if order is exists
        order:Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()

        # if user has not order, create new order for user
        if order is None:
            order = Order.objects.create(
                owner_id=request.user.id,
                is_paid=False
                )

        item_id = new_order_form.cleaned_data.get('item_id')
        count = new_order_form.cleaned_data.get('count')
        if count < 0:
            count = 1

        item = Product.objects.filter(id=item_id).first()
        order.orderdetail_set.create(item_id=item.id, price=item.price, count=count)
    return redirect('store:cart')


def remove_item_order(request, item_id):
    if item_id is not None:
        order_detail = OrderDetail.objects.get_queryset().get(id=item_id, order__owner_id=request.user.id)
        if order_detail is not None:
            order_detail.delete()

    return redirect('store:cart')


class CartView(View):
    def get(self, request):

        open_order_: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        c = {
            'order': None,
            'details': None,
            'orders': open_order_.orderdetail_set.all() 
        }

        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if open_order is not None:
            c['order'] = open_order
            c['details'] = open_order.orderdetail_set.all()
            c['total'] = open_order.get_total_price()

        return render(request, 'cart.html', c)

    
class ShopView(View):    

    def get(self, request):
        items = Product.objects.filter(active=True)
        days = datetime.datetime.today() - datetime.timedelta(days=7)
        top_product = Product.objects.filter(orderdetail__date_added__lte=datetime.datetime.today(), orderdetail__date_added__gt=days).annotate(count=Count('orderdetail__count')).order_by('-count')[:8]

        c = {
            'details': None,
            'items': items,
            'top_product': top_product,
            'category': models.Category.objects.all().annotate(items_count=Count('item'))

        }

        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if open_order is not None:
            c['details'] = open_order.orderdetail_set.all()

        return render(request, 'shop.html', c)


class Category(ListView):
    template_name = 'shop.html'
    context_object_name = 'items'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['category'] = models.Category.objects.all(),
        context['category'] = models.Category.objects.all().annotate(items_count=Count('item'))
        return context

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = models.Category.objects.filter(category_name__iexact=category_slug).first()
        if category is None:
            pass
        return Product.objects.get_queryset().filter(categories__category_slug__iexact=category_slug, active=True)


class CheckoutView(View):
    def get(self, request):
        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        c = {
            'details': None,
            'order': open_order.orderdetail_set.all()
        }

        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if open_order is not None:
            c['details'] = open_order.orderdetail_set.all()

        return render(request, 'checkout.html', c)


# ============================ ZarinPal ============================
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
CallbackURL = 'http://localhost:8000/verify/'


def send_request(request):
    total_price = 0
    open_order:Order = Order.objects.filter(is_paid=False, owner_id=request.user.id).first()
    if open_order is not None:
        total_price = open_order.get_total_price()
        res = client.service.PaymentRequest(MERCHANT, total_price, description, email, mobile, CallbackURL + str(open_order.id))
        if res.Status == 100:
            return redirect('https://www.zarinpal.com/pg/StartPay')
        else:
            return HttpResponse('Error Code' + str(res.Status))
    raise Http404('page not found :(((')


def verify(request, order_id):
    if request.GET.get('Status') == 'OK':
        user_order = Order.objects.get_queryset().get(id=order_id)
        res = client.service.PaymentRequest(MERCHANT, request.GET('Authority'), user_order.get_total_price())
        if res.Status == 100:
            user_order = Order.objects.get_queryset().get(id=order_id)
            user_order.is_paid = True
            user_order.payment_date = timezone.now()
            user_order.save()
            return HttpResponse('Transaction success.\nRefID' + str(res.RefiD))
        elif res.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(res.Status))
        else:
            return HttpResponse('Transaction failed.\nStatus' + str(res.Status))
    else:
        return HttpResponse('Transaction Failed or canceled by user')


# ============================ ======== ============================    