from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, ListView
from store.models import OrderDetail
from store.models import Order
from store.models import Item as Product
from store import forms
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import redirect
import requests
import json


class IndexView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.filter(active=True)
    context_object_name = 'products'


class SingleProduct(View):
    template_name = 'single-product.html'
    def get(self, request, slug, pk):
        product = get_object_or_404(Product, slug=slug, id=pk, active=True)
        c = {
            'product':product,
            'new_order_form' : forms.UserNewOrderForm(request.POST or None, initial={'item_id':pk})
        }
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
        c = {
            'order': None,
            'details': None
        }

        open_order: Order = Order.objects.filter(owner_id=request.user.id, is_paid=False).first()
        if open_order is not None:
            c['order'] = open_order
            c['details'] = open_order.orderdetail_set.all()

        return render(request, 'cart.html', c)


    
class ShopView(View):
    def get(self, request):
        return render(request, 'shop.html')


class CheckoutView(View):
    def get(self, request):
        return render(request, 'checkout.html')
