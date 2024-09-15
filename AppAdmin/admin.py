from django.contrib import admin
from .models import *


class ProductSupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
admin.site.register(ProductSupplier, ProductSupplierAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier')
admin.site.register(Product, ProductAdmin)

class CinemaBranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
admin.site.register(CinemaBranch, CinemaBranchAdmin)

class CinemaRoomAdmin(admin.ModelAdmin):
    list_display = ('branch', 'name', 'seat')
admin.site.register(CinemaRoom, CinemaRoomAdmin)

class CinemaSeatAdmin(admin.ModelAdmin):
    list_display = ('branch', 'room', 'number_of_seats', 'status')
admin.site.register(CinemaSeat, CinemaSeatAdmin)

class CinemaWarehouseAdmin(admin.ModelAdmin):
    list_display = ('cinemabranch', 'product', 'quantity')
admin.site.register(CinemaWarehouse, CinemaWarehouseAdmin)

class CinemaStaffAdmin(admin.ModelAdmin):
    list_display = ('branch', 'name', 'day_of_work', 'status')
admin.site.register(CinemaStaff, CinemaStaffAdmin)

class CinemaBillAdmin(admin.ModelAdmin):
    list_display = ('branch', 'movie', 'date', 'product', 'product_quantity', 'total')
admin.site.register(CinemaBill, CinemaBillAdmin)

class ImportDetailAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'quantity','staff', 'date_import')
admin.site.register(ImportDetail, ImportDetailAdmin)

class ExportDetailAdmin(admin.ModelAdmin):
    list_display = ('branch', 'product', 'quantity','staff', 'date_export')
admin.site.register(ExportDetail, ExportDetailAdmin)

class CinemaStatisticalAdmin(admin.ModelAdmin):
    list_display = ('branch', 'difference')
admin.site.register(CinemaStatistical, CinemaStatisticalAdmin)

def export_selected_to_excel(modeladmin, request, queryset):
    CinemaReport.export_to_excel(queryset)
export_selected_to_excel.short_description = "Export Selected To Excel"

class CinemaReportAdmin(admin.ModelAdmin):
    list_display = ('branch', 'difference')
    actions = [export_selected_to_excel]
admin.site.register(CinemaReport, CinemaReportAdmin)