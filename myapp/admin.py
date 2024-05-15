from django.contrib import admin
from .models import *
from .forms import PackageForm
# Register your models here.


@admin.register(Login)
class loginAdmin(admin.ModelAdmin):
    list_display = ['fname', 'lname', 'email', 'number', 'password', 'timestamp']


@admin.register(Securitytechnique)
class securityTechniqueAdmin(admin.ModelAdmin):
    list_display = ['security_name']


@admin.register(Document)
class documentAdmin(admin.ModelAdmin):
    list_display = ['userid', 'document_security_technique', 'document_type', 'document_title',
                    'document_description', 'document_status', 'document_size', 'document',
                    'document_publish_date_time', 'document_password', 'document_bin', 'document_sent']


@admin.register(Documentprivilege)
class documentprivilegeAdmin(admin.ModelAdmin):
     list_display = ['docid', 'userid', 'privilege_status']


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    form = PackageForm  # Associate the custom form with the admin class
    list_display = ['package_type', 'package_publish_date_time',
                    'package_status', 'max_uploads', 'file_size', 'package_price', 'package_duration', 'package_description']


@admin.register(Userpackagedetails)
class userpackagedetailsAdmin(admin.ModelAdmin):
    list_display = ['userid', 'premium_package_id',
                    'package_status', 'package_purchase_date', 'package_expiry_date']


@admin.register(Usercarddetails)
class usercarddetailsAdmin(admin.ModelAdmin):
    list_display = ['userid', 'card_no', 'cvv', 'expiry_date']


@admin.register(Inquiry)
class inquiryAdmin(admin.ModelAdmin):
    list_display = ['userid', 'fname', 'lname', 'email', 'subject', 'message', 'timestamp', 'status']


@admin.register(Feedback)
class feedbackAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'email', 'message', 'rating', 'timestamp']


@admin.register(Contact)
class contactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'message', 'timestamp', 'status']


@admin.register(Payment)
class paymentAdmin(admin.ModelAdmin):
    list_display = ['userid', 'premium_package_id', 'payment_status', 'package_purchase_date', 'transactionid', 'amount']
