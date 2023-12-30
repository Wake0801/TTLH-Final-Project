from django.db import models

# Supplier
class ProductSupplier(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    supplier = models.ForeignKey(ProductSupplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
# Cinema
class CinemaBranch(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class CinemaRoom(models.Model):
    name = models.CharField(max_length=50)
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    seat = models.IntegerField()

    def __str__(self):
        return self.name

class CinemaSeat(models.Model):
    room = models.ForeignKey(CinemaRoom, on_delete=models.CASCADE)
    number_of_seats = models.IntegerField()
    LOAN_STATUS = (
        ('St', 'Standard Seat'),
        ('Pr', 'Premium Seat'),
        ('Sw', 'Sweetbox Seat'),
    )
    status = models.CharField(
        max_length=2,
        choices=LOAN_STATUS,
        blank=True,
        default='St',
    )

    def __str__(self):
        return str(self.seat)

class CinemaWarehouse(models.Model):
    cinemabranch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.quantity)

class CinemaStaff(models.Model):
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()
    day_of_work = models.DateField()
    LOAN_STATUS = (
        ('M', 'CinemaManager'),
        ('P', 'ProductManager'),
        ('S', 'Staff'),
    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='S',
    )
    def __str__(self):
        return self.name