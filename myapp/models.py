from django.db import models

# Create your models here.


class Login(models.Model):
    fname = models.CharField(max_length=60)
    lname = models.CharField(max_length=60)
    email = models.EmailField()
    number = models.IntegerField()
    password = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fname} {self.lname}"


class Securitytechnique(models.Model):
    security_name = models.CharField(max_length=60)

    def __str__(self):
        return self.security_name


class Document(models.Model):
    userid = models.ForeignKey(Login, on_delete=models.CASCADE)
    document_security_technique = models.ForeignKey(Securitytechnique, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=60)
    document_title = models.CharField(max_length=60)
    document_description = models.TextField()
    document_status = models.CharField(max_length=60, choices=[('draft', 'Draft'),
                                                               ('published', 'Published'), ('deleted', 'Deleted')])
    document_size = models.FloatField()
    document = models.FileField()
    document_publish_date_time = models.DateTimeField(auto_now=True)
    document_password = models.CharField(max_length=100, blank=True)
    document_bin = models.IntegerField(default=0)
    document_sent = models.IntegerField(default=0)

    def __str__(self):
        return self.document_title


class Documentprivilege(models.Model):
    docid = models.ForeignKey(Document, on_delete=models.CASCADE)
    userid = models.ForeignKey(Login, on_delete=models.CASCADE)
    privilege_status = models.CharField(max_length=60, choices=[('draft', 'Draft'), ('granted', 'Granted'),
                                                                ('revoked', 'Revoked')])
    sent_to = models.ManyToManyField(Login, related_name='received_documents')


class Package(models.Model):
    package_type = models.CharField(max_length=60)
    package_publish_date_time = models.DateTimeField(auto_now=True)
    package_status = models.CharField(max_length=60)
    max_uploads = models.IntegerField(blank=True, default=-1)
    file_size = models.BigIntegerField(blank=True, default=-1)
    package_price = models.FloatField()
    package_duration = models.IntegerField()
    package_description = models.TextField()

    def __str__(self):
        return self.package_type


class Userpackagedetails(models.Model):
    userid = models.ForeignKey(Login, on_delete=models.CASCADE)
    premium_package_id = models.ForeignKey(Package, models.CASCADE)
    package_status = models.CharField(max_length=60, choices=[('active', 'ACTIVE'),
                                                              ('expired', 'EXPIRED')])
    package_purchase_date = models.DateTimeField(auto_now=True)
    package_expiry_date = models.CharField(max_length=60)


class Usercarddetails(models.Model):
    userid = models.ForeignKey(Login, on_delete=models.CASCADE)
    card_no = models.IntegerField()
    cvv = models.IntegerField()
    expiry_date = models.CharField(max_length=10)


class Inquiry(models.Model):
    userid = models.ForeignKey(Login, on_delete=models.CASCADE)
    fname = models.CharField(max_length=60)
    lname = models.CharField(max_length=60)
    email = models.EmailField()
    subject = models.CharField(max_length=60)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=60, choices=[('pending', 'PENDING'), ('resolved', 'RESOLVED')])


class Feedback(models.Model):
    firstname = models.CharField(max_length=60)
    lastname = models.CharField(max_length=60)
    email = models.EmailField()
    message = models.TextField()
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)

    def rating_stars(self):
        return range(self.rating)


class Contact(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    phone = models.BigIntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=60, choices=[('pending', 'PENDING'),
                                                      ('resolved', 'RESOLVED')])


class Payment(models.Model):
    userid = models.ForeignKey(Login, on_delete=models.CASCADE)
    premium_package_id = models.ForeignKey(Package, models.CASCADE)
    payment_status = models.CharField(max_length=60, choices=[('completed', 'COMPLETED'), ('pending', 'PENDING')])
    package_purchase_date = models.DateTimeField()
    amount = models.FloatField()
    transactionid = models.CharField(max_length=100)
