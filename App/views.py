from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse
import json,uuid
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.

# Home Page
def index(requests):
    movies_NS = Movie.objects.filter(status = 'N')
    movies_CS = Movie.objects.filter(status = 'C')
    context = {
        'movies_NS': movies_NS,
        'movies_CS': movies_CS
    }
    return render(requests, 'app/home.html', context)

def about(requests):
    return render(requests, 'app/about.html')

def products(requests):
    products = Products.objects.all()
    context = {'products': products}
    return render(requests, 'app/product.html', context)
# Movie Page

def movie(requests):
    movies_NS = Movie.objects.filter(status = 'N')
    movies_CS = Movie.objects.filter(status = 'C')
    context = {
        'movies_NS': movies_NS,
        'movies_CS': movies_CS
    }
    return render(requests, 'app/movie.html', context)

def detail(request):
    id = request.GET.get('id', None)
    movie = Movie.objects.filter(id=id)
    dates = ShowingDate.objects.filter(movie=id)
    date_times = []
    for date in dates:
        times = ShowingTime.objects.filter(movie=id, date=date.id)
        date_times.append({'date': date, 'times': times})
    context = {'movie': movie, 'date_times': date_times}
    return render(request, 'app/detail.html', context)
# Ticket Page
def seats(requests):
    id = requests.GET.get('id', None)
    movie = Movie.objects.filter(id=id)
    dates = ShowingDate.objects.filter(movie=id)
    times = ShowingTime.objects.all()
    context = {'movie': movie, 'dates': dates, 'times': times}
    return render(requests, 'app/ticket/seats.html', context)

def product_order(requests):
    products_singles = Products.objects.filter(status__in=['S', 'P', 'T'])
    products_combos = Products.objects.filter(status='C')
    context = {
        'products_singles': products_singles,
        'products_combos': products_combos
    }
    return render(requests, 'app/ticket/products.html', context)

def cart(requests):
    if requests.user.is_authenticated:
        user = requests.user
        order, created = Booking.objects.get_or_create(user=user)
        items = order.bookingcomfirm_set.all()
        items_product = order.productcomfirm_set.all()
    else:
        items = []
    context = { 'items': items,
                'items_product' : items_product,
                'order': order,
    }
    return render(requests, 'app/ticket/cart.html', context)

# Save data to database
@csrf_exempt
def updateMovie(requests):
    if requests.method == 'POST':
        data = json.loads(requests.body)
        movieId = data['movieId']
        action = data['action']

        user = requests.user

        order, created = Booking.objects.get_or_create(user=user)
            
        order.save()
            
        return redirect('detail')
    
    return render(requests, 'app/ticket/seats.html')
    
def updateDate(request):
    data = json.loads(request.body)
    movieId = data.get('movieId')
    dateId = data.get('dateId')
    timeId = data.get('timeId')
    action = data.get('action')
    if request.method == 'POST':
        user = request.user
        movie = Movie.objects.get(id=movieId)
        date = ShowingDate.objects.get(id=dateId)
        time = ShowingTime.objects.get(id=timeId)

        order, created = Booking.objects.get_or_create(user=user)
        

        order.save()
        
        request.session['movie'] = movieId
        request.session['date'] = dateId
        request.session['time'] = timeId

        return JsonResponse({'message': 'Thành công'}, status=200)

def updateSeat(request):
    data = json.loads(request.body)
    action = data.get('action')
    seats_quantity = data.get('seatCount')
    
    request.session['seats_quantity'] = seats_quantity
    if request.method == 'POST':
        seats_quantity = int(seats_quantity) if seats_quantity else None
        if seats_quantity is None or seats_quantity <= 0:
            return JsonResponse({'error': 'Invalid input'}, status=400)
        else:
            movie_id = request.session.get('movie')
            date_id = request.session.get('date')
            time_id = request.session.get('time')

            user = request.user
            movie = Movie.objects.get(id=movie_id)
            date = ShowingDate.objects.get(id=date_id)
            time = ShowingTime.objects.get(id=time_id)

            order, created = Booking.objects.get_or_create(user=user)

            existing_booking = BookingComfirm.objects.filter(
                user_order=order,
                movie=movie,
                date=date,
                time=time,
            ).first()

            if existing_booking:
                existing_booking.seats_quantity = seats_quantity
                existing_booking.save()
            else:
                booking = BookingComfirm.objects.create(
                    user_order=order,
                    movie=movie,
                    date=date,
                    time=time,
                    seats_quantity=seats_quantity,
                )
        return JsonResponse({'message': 'Thành công'}, status=200)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def updateProduct(request):
    data = json.loads(request.body)
    product_id = data.get('productId')
    product_quantity = data.get('amount')

    request.session['product'] = product_id
    request.session['quantity'] = product_quantity

    if request.method == 'POST':
        product_quantity = int(product_quantity) if product_quantity else None
        if product_quantity <= 0:
            return JsonResponse({'error': 'Invalid input'}, status=400)
        else:
            product = Products.objects.get(id=product_id)

            user = request.user

            order, created = Booking.objects.get_or_create(user=user)

            existing_booking = ProductComfirm.objects.filter(
                user_order=order,
                product=product,
            ).first()

            if existing_booking:
                existing_booking.quantity = product_quantity
                existing_booking.save()
            else:
                booking = ProductComfirm.objects.create(
                    user_order=order,
                    product=product,
                    quantity=product_quantity,
                )
        return JsonResponse({'message': 'Thành công'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
# Payment page
def payment(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Booking.objects.get_or_create(user=user)
        items_movie = order.bookingcomfirm_set.filter(user_order=order)
        items_product = order.productcomfirm_set.filter(user_order=order)
    if items_movie.exists():
        movie = items_movie.first().movie
        total_price_movie = sum(items_movie.total_price for items_movie in items_movie)
    else:
        movie = None
        total_price_movie = 0

    if items_product.exists():
        product = items_product.first().product
        total_price_product = sum(items_product.total_price for items_product in items_product)
    else:
        product = None
        total_price_product = 0

    host = request.get_host()

    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_price_movie + total_price_product,
        'item_movie_name' : movie.title if movie else '',
        'item_product_name' : product.name if product else '',
        'item_movie_price' : total_price_movie,
        'item_product_price' : total_price_product,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f'http://{host}{reverse('paypal-ipn')}',
        'return_url': f'http://{host}{reverse('paymentsuccess')}',
        'cancel_url': f'http://{host}{reverse('paymentfail')}',
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    
    context = {
        'items_movie': items_movie, 
        'items_product' : items_product,
        'order': order,
        'paypal': paypal_payment,
        'movie': movie,
        'product': product,
    }
    return render(request, 'app/ticket/payment.html', context)

def paymentSuccess(requests):
    user = requests.user
    order, created = Booking.objects.get_or_create(user=user)
    
    booking_confirm = order.bookingcomfirm_set.get(user_order=order)
    product_confirm = order.productcomfirm_set.get(user_order=order)

    completed_payment = CompletedPayment.objects.create(
        user_order=order,
        movie=booking_confirm.movie,
        date=booking_confirm.date,
        time=booking_confirm.time,
        seats_quantity=booking_confirm.seats_quantity,
        booking_total_price=booking_confirm.total_price,
        product=product_confirm.product,
        quantity=product_confirm.quantity,
        product_total_price=product_confirm.total_price,
        status='S',
    )
    
    booking_confirm.delete()
    product_confirm.delete()

    return render(requests, 'app/ticket/paymentSuccess.html')

def paymentFail(requests):
    return render(requests, 'app/ticket/paymentFail.html')

# User Page
def signup(requests):
    if requests.method == 'POST':
        username = requests.POST['username']
        firstname = requests.POST['fname']
        lastname = requests.POST['lname']
        email = requests.POST['email']
        password = requests.POST['password']
        comfirm_password = requests.POST['confirmpassword']

        if User.objects.filter(email=email).exists():
            messages.error(requests, 'Email was used, please try again')
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(requests, 'Username was used, please try again')
            return redirect('signup')
        
        if firstname.isdigit() or lastname.isdigit():
            messages.error(requests, 'First name or Last name is invalid, please try again')
            return redirect('signup')
        
        if password != comfirm_password:
            messages.error(requests, 'Password does not match')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(requests, 'Your account has been created successfully')

        return redirect('signin')

    return render(requests, 'app/user/signup.html')

def signin(requests):
    
    if requests.method == 'POST':
        username = requests.POST['username']
        password = requests.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(requests, user)
            firstname = user.first_name
            messages.success(requests, 'You have been logged in successfully')
            redirect('/')
            return render(requests, "app/home.html", {'fname': firstname})
        
        else:
            messages.error(requests, 'Username or Password is incorrect, Please try again')
            redirect('signin')
    
    return render(requests, 'app/user/signin.html')

def signout(requests):
    logout(requests)
    messages.success(requests, 'You have been logged out successfully')
    return redirect('signin')

def user(requests):
    return render(requests, 'app/user/profile.html')

def history(requests):
    user = requests.user
    order, created = Booking.objects.get_or_create(user=user)
    completed_payments = CompletedPayment.objects.filter(user_order=order)
    context = {
        'completed_payments': completed_payments,
    }
    return render(requests, 'app/user/history.html', context)