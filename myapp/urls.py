from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexpage, name="indexpage"),
    path('index.html', views.reroute, name="reroute"),
    path('register', views.registration, name="registration"),
    path('savedata', views.savedata, name="savedata"),
    path('login', views.login, name="login"),
    path('verifyuser', views.verifyuser, name="verifyuser"),
    path('logout', views.logout, name="logout"),
    path('uploadpublicly', views.formuploadpublic, name="formuploadpublic"),
    path('uploadprivately', views.formuploadprivate, name="formuploadprivate"),
    path('userprivilege', views.userprivilege, name="userprivilege"),
    path('getuserprivilegefile', views.getuserprivilegefile, name="getuserprivilegefile"),
    path('sharefiles', views.sharefiles, name="sharefiles"),
    path('myuploads', views.uploads, name="uploads"),
    path('recyclebin', views.recyclebin, name="recyclebin"),
    path('movetobin', views.movetobin, name="movetobin"),
    path('restore', views.restore, name="restore"),
    path('deletefile', views.deletefile, name="deletefile"),
    path('enquiry', views.enquiry, name="enquiry"),
    path('getenquiry', views.get_enquiry, name="get_enquiry"),
    path('feedback', views.feedback, name="feedback"),
    path('aftertransit', views.aftertransit, name="aftertransit"),
    path('unsend', views.unsend, name="unsend"),
    path('sharedfiles', views.shareduser, name="shareduser"),
    path('getfeedback', views.getfeedback, name="getfeedback"),
    path('publicfiles', views.public_files, name="public_files"),
    path('privatefiles', views.privatefiles, name="privatefiles"),
    path('verifypass', views.verifypass, name="verifypass"),
    path('download', views.download, name="download"),
    path('DocVaultPremium', views.premium, name="premium"),
    path('payment', views.handle_payment, name="handle_payment"),
    path('managepayment', views.manage_payment, name="manage_payment"),
    path('profile', views.profile, name="profile"),
    path('changePassword', views.change_password, name="change_password"),
    path('contact', views.contact, name="contact"),
    path('getcontact', views.get_contact, name="get_contact"),
    path('forgot_password', views.forgot_password, name="forgot_password"),
    path('change_password', views.forgotpassword, name="forgotpassword"),
    path('mypackage', views.my_package, name="my_package"),



    path('checkpackage', views.checkpackage, name="checkpackage"),



    ]
