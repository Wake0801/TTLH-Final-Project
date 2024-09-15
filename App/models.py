from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Movie Model

class Genre(models.Model):
    name = models.CharField(max_length=100, help_text="Enter a genre of movie")

    def __str__(self) -> str:
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=200,help_text="Title Movie",null=False,blank=False)
    sologan = models.CharField(max_length=200,help_text="Sologan Movie",null=False,blank=False, default="")
    description = models.TextField(max_length=2000, help_text="Enter description of the movie")
    director = models.CharField(max_length=100, help_text="Director")
    cast = models.CharField(max_length=200, help_text="Cast")
    genre = models.ManyToManyField(Genre, help_text="Select a genre for this movie")
    duration = models.IntegerField(default=0, help_text="Duration of movie")
    poster = models.ImageField(null=False,blank=False, upload_to="poster/")
    trailer_url = models.URLField(null=False,blank=False, help_text="Enter link trailer")
    price = models.IntegerField(default=0, help_text="Price of movie")
    LOAN_STATUS = (
        ('N', 'Now Showing'),
        ('C', 'Coming Soon'),
        ('E', 'End Showing'),
           
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=False,
        default='C',
        help_text='Movie availability',
    )
    

    def  __str__(self) -> str:
        return self.title
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description = 'Genre'

class Branch(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name

class ShowingDate(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    date = models.DateField(null=False, blank=False)

    def __str__(self) -> str:
        return str(self.date)

class ShowingTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    date = models.ForeignKey(ShowingDate, on_delete=models.CASCADE)
    time = models.TimeField(null=False, blank=False)

    def __str__(self) -> str:
        return str(self.time)

# Product Model

class Products(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    price = models.IntegerField(default=0)
    image = models.ImageField(null=False,blank=False, upload_to="product/")
    LOAN_STATUS_PRODUCT = (
        ('S', 'Soda'),
        ('P', 'PopCorn'),
        ('T', 'Tea'),
        ('C', 'Combo'),       
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS_PRODUCT,
        blank=False,
        default='C',
    )
    def __str__(self) -> str:
        return self.name

# Order Model

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username

class BookingComfirm(models.Model):
    user_order = models.ForeignKey(Booking, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True)
    date = models.ForeignKey(ShowingDate, on_delete=models.CASCADE)
    time = models.ForeignKey(ShowingTime, on_delete=models.CASCADE)
    seats_quantity = models.IntegerField(null=False, default=0)
    total_price = models.IntegerField(null=False, default=0)

    def __str__(self) -> str:
        return str(self.movie)
    def save(self, *args, **kwargs):
        self.total_price = self.movie.price * self.seats_quantity
        super().save(*args, **kwargs)

class ProductComfirm(models.Model):
    user_order = models.ForeignKey(Booking, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=0)
    total_price = models.IntegerField(null=False, default=0)

    def __str__(self) -> str:
        return str(self.product)
    
    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

class CompletedPayment(models.Model):
    user_order = models.ForeignKey(Booking, on_delete=models.CASCADE, null = True)
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    date = models.ForeignKey(ShowingDate, on_delete=models.SET_NULL, null=True)
    time = models.ForeignKey(ShowingTime, on_delete=models.SET_NULL, null=True)
    seats_quantity = models.IntegerField(null=True)
    booking_total_price = models.IntegerField(null=True)
    product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(null=True)
    product_total_price = models.IntegerField(null=True)
    total_complete_payment = models.IntegerField(null=True)

    LOAN_STATUS_PAYMENT = (
        ('S', 'Success'),
        ('F', 'Fail'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS_PAYMENT,
        blank=False,
        default='F',
    )
    def __str__(self) -> str:
        return self.user_order.user.username
    def save(self, *args, **kwargs):
        self.booking_total_price = self.movie.price * self.seats_quantity
        self.product_total_price = self.product.price * self.quantity
        self.total_complete_payment = self.booking_total_price + self.product_total_price
        super().save(*args, **kwargs)
