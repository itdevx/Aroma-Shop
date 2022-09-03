from django.urls import path
from store import views

app_name = 'store'


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('single-product/<slug:slug>/<int:pk>', views.SingleProduct.as_view(), name='single-product'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('shop/', views.ShopView.as_view(), name='shop'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('add-user-order/', views.add_user_order, name='add-user-order'),
    path('cart-delete/<item_id>/', views.remove_item_order, name='remove-orderdetail'),
    path('shop/<category_slug>/', views.Category.as_view(), name='category')
]