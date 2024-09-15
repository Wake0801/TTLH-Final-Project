from django.db import models
from App import models as AppModels
import pandas as pd

# Supplier
class ProductSupplier(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.ForeignKey(AppModels.Products, on_delete=models.CASCADE)
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
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    seat = models.IntegerField()

    def __str__(self):
        return self.name

class CinemaSeat(models.Model):
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
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
    date_of_birth = models.DateField()
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
    
class CinemaBill(models.Model):
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    movie = models.ForeignKey(AppModels.Movie, on_delete=models.CASCADE)
    date = models.ForeignKey(AppModels.ShowingDate, on_delete=models.CASCADE)
    time = models.ForeignKey(AppModels.ShowingTime, on_delete=models.CASCADE)
    movie_seat = models.IntegerField()
    product = models.ForeignKey(AppModels.Products, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.total

class ImportDetail(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    staff = models.CharField(max_length=50)
    date_import = models.DateField()

    def __str__(self):
        return self.branch.name

class ExportDetail(models.Model):
    id = models.AutoField(primary_key=True)
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    staff = models.CharField(max_length=50)
    date_export = models.DateField()

    def __str__(self):
        return self.branch.name

class CinemaStatistical(models.Model):
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    date = models.DateField()
    movie_virual = models.IntegerField()
    product_virual = models.IntegerField()
    difference = models.IntegerField()

    def __str__(self):
        return self.branch.name
    def get_total(self):
        if self.movie_virual > self.product_virual:
            return self.difference == (self.movie_virual - self.product_virual)
        else:
            return self.difference == (self.product_virual - self.movie_virual)
        
class CinemaReport(models.Model):
    branch = models.ForeignKey(CinemaBranch, on_delete=models.CASCADE)
    date = models.DateField()
    phantom = models.IntegerField()
    actual = models.IntegerField()
    difference = models.IntegerField()

    def __str__(self):
        return self.branch.name
    def get_total(self):
        if self.phantom > self.actual:
            return self.difference == (self.phantom - self.actual)
        else:
            return self.difference == (self.actual - self.phantom)
    @staticmethod
    def export_to_excel(queryset):
        data = queryset.values('branch__name', 'date', 'phantom', 'actual', 'difference')
        df = pd.DataFrame.from_records(data)
        df.columns = ['Branch', 'Date', 'Phantom', 'Actual', 'Difference']
        df.to_excel('CinemaReport.xlsx', sheet_name='TTLHReport', index=False, header=True)        