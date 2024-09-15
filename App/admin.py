from django.contrib import admin
from .models import *

# Register your models here.

# Movie API
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'director', 'display_genre', 'status')

    search_fields = ['title', 'status']
admin.site.register(Movie, MovieAdmin)

class ShowingDateAdmin(admin.ModelAdmin):
    list_display = ('movie', 'branch', 'date')
admin.site.register(ShowingDate, ShowingDateAdmin)

class ShowingTimeAdmin(admin.ModelAdmin):
    list_display = ('movie', 'branch','date',  'time')
admin.site.register(ShowingTime, ShowingTimeAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'status')
admin.site.register(Products, ProductAdmin)
# Booking API
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user_order', 'total_complete_payment', 'status')
admin.site.register(CompletedPayment, PaymentAdmin)

class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
admin.site.register(Branch, BranchAdmin)