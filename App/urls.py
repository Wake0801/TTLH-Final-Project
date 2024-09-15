from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('products/', views.products, name='products'),
    
    # Movie
    path('movie/', views.movie, name='movie'),
    path('detail/', views.detail, name='detail'),

    # Ticket
    path('seats/', views.seats, name='seats'),
    path('product_order/', views.product_order, name='product_order'),
    path('cart/', views.cart, name='cart'),
    path('payment/', views.payment, name='payment'),
    # Request to DB
    path('updateMovie/', views.updateMovie, name='updateMovie'),
    path('updateDate/', views.updateDate, name='updateDate'),
    path('updateSeat/', views.updateSeat, name='updateSeat'),
    path('updateProduct/', views.updateProduct, name='updateProduct'),
    # Payment
    path('paymentsuccess/', views.paymentSuccess, name='paymentsuccess'),
    path('paymentfail/', views.paymentFail, name='paymentfail'),
    # User
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('user/', views.user, name='user'),
    path('history/', views.history, name='history'),
    path('search/', views.search, name='search')
]
