from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
import os
from django.http import FileResponse
from datetime import datetime, timedelta
from django.db.models import Sum
import uuid
from django.utils import timezone
from django.template.defaultfilters import filesizeformat
from django.template.loader import render_to_string
from django.core.mail import send_mail


def checkpackage(request):
    uid = request.session.get("login_id")
    get_details = Userpackagedetails.objects.get(userid=Login(id=uid), package_status="active")
    context = {'packagedetails': get_details}
    return context


def indexpage(request):
    try:
        uid = request.session.get("login_id")
        if uid:
            data = Login.objects.get(id=uid)
            firstname = data.fname
            lastname = data.lname
            countdata = Document.objects.filter(userid=uid, document_bin=0).count()
            userpackagedata = Userpackagedetails.objects.get(userid=uid, package_status="active")
            shareddata = Documentprivilege.objects.filter(sent_to=Login(id=uid), privilege_status="granted").count()
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            package_expiry_date = datetime.strptime(packagedetails.package_expiry_date, '%Y-%m-%d').date()
            last_5_feedbacks = Feedback.objects.order_by('-timestamp')[:5]
            try:
                if package_expiry_date <= datetime.now().date():
                    package_updation = Userpackagedetails.objects.get(userid=Login(id=uid), package_status="active")
                    package_updation.package_status = "expired"
                    package_updation.save()
                    purchase_date = datetime.now()
                    getpackage = Package.objects.get(package_type="Basic")
                    expiry_date = purchase_date + timedelta(days=30)
                    # Format the expiry date as YYYY-MM-DD
                    formatted_expiry_date = expiry_date.strftime('%Y-%m-%d')
                    insert_package = Userpackagedetails(userid=Login(id=uid),
                                                        premium_package_id=Package(id=getpackage.id),
                                                        package_status="active", package_purchase_date="",
                                                        package_expiry_date=formatted_expiry_date)
                    insert_package.save()

                return render(request, "index.html",
                                      {'fname': firstname, 'lname': lastname, 'data': shareddata, 'count': countdata, 'package': userpackagedata, 'feedbacks': last_5_feedbacks})
            except:
                pass
                return redirect(logout)
    except:
        pass
    return render(request, "index.html")


def reroute(request):
    return redirect(indexpage)


def registration(request):
    try:
        uid = request.session.get("login_id")
        if uid:
            return redirect(logout)
    except:
        pass
    return render(request, "auth-register.html")


def savedata(request):
    try:
        uid = request.session.get("login_id")
        if uid:
            return redirect(logout)

        if request.method == "POST":
            mailid = request.POST.get("email")
            f1name = request.POST.get("fname")
            f2name = request.POST.get("lname")
            pnumber = request.POST.get("phno")
            password = request.POST.get("pass")
            cpassword = request.POST.get("cpass")

            if Login.objects.filter(email=mailid).exists():
                messages.error(request, "Email Id already Registered")
                return redirect(registration)

            if Login.objects.filter(number=pnumber).exists():
                messages.error(request, "Phone number already Registered")
                return redirect(registration)

            if password == cpassword:
                hashed_password = make_password(password)
                insertdata = Login(fname=f1name, lname=f2name, email=mailid, number=pnumber, password=hashed_password,
                                   timestamp="")
                insertdata.save()
                getpackage = Package.objects.get(package_type="Basic")
                usermail = Login.objects.get(email=mailid)
                purchase_date = datetime.now()
                expiry_date = purchase_date + timedelta(days=30)
                # Format the expiry date as YYYY-MM-DD
                formatted_expiry_date = expiry_date.strftime('%Y-%m-%d')
                insertpackage = Userpackagedetails(userid=Login(id=usermail.id),
                                                   premium_package_id=Package(id=getpackage.id),
                                                   package_status="active", package_purchase_date="",
                                                   package_expiry_date=formatted_expiry_date)
                insertpackage.save()
                messages.success(request, "Account Created Successfully, Please Login")
                return redirect(login)
            else:
                messages.error(request, "Passwords do not match")
        return render(request, "auth-register.html")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect(registration)


def login(request):
    uid = request.session.get("login_id")
    if uid:
        return redirect(indexpage)
    return render(request, "auth-login.html")


def verifyuser(request):
    if request.method == "POST":
        email = request.POST.get("mail")
        pwd = request.POST.get("pass")

        try:
            user = Login.objects.get(email=email)
            if check_password(pwd, user.password):
                request.session["login_id"] = user.id
                request.session.save()
                messages.success(request, "Login Successfull")
                return redirect(indexpage)
            else:
                messages.success(request, "Incorrect Password, please try again")
                return redirect(login)
        except:
            messages.success(request, "Invalid Email")
            return redirect(login)

    return render(request, "auth-login.html")


def logout(request):
    try:
        del request.session["login_id"]
        messages.success(request, "Logged Out")
        return redirect(indexpage)
    except:
        pass
    return redirect(indexpage)


def formuploadpublic(request):
    uid = request.session.get("login_id")
    try:
        if uid:
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            context = {'package': packagedetails}
            return render(request, "form_upload.html", context)
    except:
        pass
    return redirect(login)


def formuploadprivate(request):
    uid = request.session.get("login_id")
    try:
        if uid:
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            context = {'package': packagedetails}
            return render(request, "form_upload_private.html", context)
    except:
        pass
    return redirect(login)


def userprivilege(request):
    uid = request.session.get("login_id")
    try:
        if uid:
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            context = {'package': packagedetails}
            return render(request, "user_privilege.html", context)
    except:
        pass
    return redirect(login)


def getuserprivilegefile(request):
    try:
        uid = request.session.get("login_id")
        if request.method == 'POST':
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            # Convert package_expiry_date to datetime object
            package_expiry_datetime = datetime.strptime(packagedetails.package_expiry_date, '%Y-%m-%d').date()

            if package_expiry_datetime >= datetime.now().date():

                if packagedetails.premium_package_id.max_uploads == -1 and packagedetails.premium_package_id.file_size == -1:

                    uploaded_files = request.FILES['files']
                    documentname = request.POST.get("docname")
                    private = request.POST.get("security")
                    security_technique = Securitytechnique.objects.get(security_name=private)
                    documentdesc = request.POST.get("docdesc")
                    dpass = request.POST.get("docpass")
                    dcpass = request.POST.get("docpassc")
                    docsize = uploaded_files.size
                    documenttype = os.path.splitext(uploaded_files.name)[1]

                    if dpass:

                        if dpass == dcpass:

                            hashed_password = make_password(dpass)
                            doc = Document(userid=Login(id=uid),
                                           document_security_technique=Securitytechnique(id=security_technique.id),
                                           document_type=documenttype, document_title=documentname,
                                           document_description=documentdesc,
                                           document_status="published", document=uploaded_files, document_size=docsize,
                                           document_password=hashed_password,
                                           document_publish_date_time="")
                            doc.save()
                            messages.success(request, "Your Private Document Uploaded Successfully")
                            return redirect(formuploadprivate)
                        messages.success(request, "Password did not Matched")
                        return redirect(formuploadprivate)
                    doc = Document(userid=Login(id=uid), document_security_technique=Securitytechnique(id=security_technique.id),
                                   document_type=documenttype, document_title=documentname,
                                   document_description=documentdesc,
                                   document_status="published", document=uploaded_files, document_size=docsize,
                                   document_publish_date_time="")
                    doc.save()
                    if security_technique.security_name == "public":
                        messages.success(request, "Public File Uploaded Successfully")
                        return redirect(formuploadpublic)
                    messages.success(request, "File Uploaded Successfully")
                    return redirect(userprivilege)
                else:
                    count_data = Document.objects.filter(userid=uid, document_bin=0).count()
                    package = packagedetails.premium_package_id
                    if count_data < package.max_uploads:
                        total_size_db = Document.objects.filter(userid=Login(id=uid)).aggregate(total_size=Sum('document_size'))[
                            'total_size']
                        uploaded_files = request.FILES['files']
                        docsize = uploaded_files.size
                        if total_size_db is None:
                            total_size_db = 0
                        available_size = package.file_size - total_size_db
                        if total_size_db < package.file_size and docsize < available_size:
                            private = request.POST.get("security")
                            security_technique = Securitytechnique.objects.get(security_name=private)
                            documentname = request.POST.get("docname")
                            documentdesc = request.POST.get("docdesc")
                            dpass = request.POST.get("docpass")
                            dcpass = request.POST.get("docpassc")
                            documenttype = os.path.splitext(uploaded_files.name)[1]

                            if dpass:
                                if dpass == dcpass:
                                    hashed_password = make_password(dpass)
                                    doc = Document(userid=Login(id=uid),
                                                   document_security_technique=Securitytechnique(id=security_technique.id),
                                                   document_type=documenttype, document_title=documentname,
                                                   document_description=documentdesc,
                                                   document_status="published", document=uploaded_files,
                                                   document_size=docsize,
                                                   document_password=hashed_password,
                                                   document_publish_date_time="")
                                    doc.save()
                                    messages.success(request, "Private File Uploaded successfully")
                                    return redirect(formuploadprivate)
                                messages.success(request, "Password did not Matched")
                                return redirect(formuploadprivate)
                            doc = Document(userid=Login(id=uid), document_security_technique=Securitytechnique(id=security_technique.id),
                                document_type=documenttype, document_title=documentname, document_description=documentdesc,
                                document_status="published", document=uploaded_files, document_size=docsize,
                                document_publish_date_time="")
                            doc.save()
                            if security_technique.security_name == "public":
                                messages.success(request, "Public File Uploaded Successfully")
                                return redirect(formuploadpublic)
                            messages.success(request, "File Uploaded Successfully")
                            return redirect(userprivilege)
                        messages.success(request, "You have exhausted file size as per Your Plan")
                        return redirect(userprivilege)
                    messages.success(request, "You have exhausted your Free Upload Limit")
                    return redirect(userprivilege)
            messages.success(request, "Oops! Your Package is Expired, we will Assign You Basic Package")
            return redirect(indexpage)
        else:
            messages.success(request, "There is some Issue, please write feedback")
            return redirect(enquiry)
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect(feedback)


def sharefiles(request):
    uid = request.session.get("login_id")
    if uid:
        try:

            security = Securitytechnique.objects.get(security_name="user privilege")
            shareddata = Document.objects.filter(userid=Login(id=uid),
                                                 document_security_technique=Securitytechnique(id=security.id),
                                                 document_sent=0, document_bin=0)

            getshareddata = Document.objects.filter(userid=Login(id=uid),
                                                    document_security_technique=Securitytechnique(id=security.id),
                                                    document_sent=1)
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            return render(request, "share_files.html", {'sharedata': shareddata, 'getsharedata': getshareddata, 'package': packagedetails})
        except:
            pass
    return redirect(login)


def aftertransit(request):
    uid = request.session.get("login_id")
    try:
        if uid:
            if request.method == "POST":
                mailid = request.POST.get("mail")
                doc_id = request.POST.get("docid")

                if Login.objects.filter(email=mailid).exists():
                    mail = Login.objects.get(email=mailid)
                    emailid = Login.objects.get(id=uid)
                    current_user_email = emailid.email
                    if not mail.email == current_user_email:
                        # Create a Documentprivilege object
                        senddoc = Documentprivilege.objects.create(
                            docid=Document.objects.get(id=doc_id),  # Assuming Document has an 'id' field
                            userid=Login.objects.get(id=uid),  # Assuming Login has an 'id' field
                            privilege_status="granted"
                        )
                        updatedata = Document.objects.filter(id=doc_id)
                        updatedata.update(document_sent=1)
                        # Now that senddoc is saved to the database, you can set the many-to-many relationship
                        senddoc.sent_to.set([mail])  # Assuming mail is a Login object

                        # Save the object after setting the many-to-many relationship
                        senddoc.save()
                        messages.success(request, "Access Granted as per your request")
                        return redirect(sharefiles)
                    messages.success(request, "You cannot share File to Yourself")
                    return redirect(sharefiles)
                messages.success(request, "No such User exists")
                return redirect(sharefiles)
            messages.success(request, "Documents Data not Fetched")
            return redirect(sharefiles)
    except:
        pass
    return redirect(login)


def shareduser(request):
    uid = request.session.get("login_id")
    if uid:
        docs = Documentprivilege.objects.filter(sent_to=Login(id=uid), privilege_status="granted")
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        return render(request, "received_docs.html", {'doc': docs, 'package': packagedetails})
    return redirect(login)


def unsend(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":

            doc_id = request.POST.get("doc_un_send_id")
            retrieve_doc = Document.objects.filter(id=doc_id, document_sent=1)
            retrieve_doc.update(document_sent=0)

            retrieve_access = Documentprivilege.objects.filter(docid=doc_id, userid=uid, privilege_status="granted")
            retrieve_access.update(privilege_status="revoked")
        return redirect(sharefiles)
    return redirect(login)


def uploads(request):
    uid = request.session.get("login_id")
    if uid:
        security = Securitytechnique.objects.get(security_name="private")
        data = Document.objects.filter(userid=Login(id=uid), document_bin=0, document_status="published").exclude(
            document_security_technique=Securitytechnique(id=security.id))
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        return render(request, "myuploads.html", {'mydata': data, 'package':packagedetails})
    return redirect(login)


def recyclebin(request):
    uid = request.session.get("login_id")
    if uid:
        data = Document.objects.filter(document_bin=1, document_status="published")
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        context = {'mydata': data, 'package': packagedetails}
        return render(request, "recycle_bin.html", context)
    return redirect(login)


def movetobin(request):
    uid = request.session.get("login_id")
    if uid:
        getFile = request.POST.get("uploads")
        if getFile == "fromPrivate":
            if request.method == "POST":
                bin_id = request.POST.get("bin")
                data = Document.objects.filter(id=bin_id)
                data.update(document_bin=1)
                return redirect(privatefiles)
        else:
            if request.method == "POST":
                bin_id = request.POST.get("bin")
                data = Document.objects.filter(id=bin_id)
                data.update(document_bin=1)
                return redirect(uploads)
    return redirect(login)


def restore(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":
            restore_id = request.POST.get("bin")
            data = Document.objects.filter(id=restore_id)
            data.update(document_bin=0)
            return redirect(recyclebin)
    return redirect(login)


def deletefile(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":
            filedata = request.POST.get("permanentdelete")
            delete_data = Document.objects.filter(id=filedata)
            delete_data.update(document_status="deleted")
            return redirect(recyclebin)
        return redirect(recyclebin)
    return redirect(recyclebin)


def enquiry(request):
    uid = request.session.get("login_id")
    if uid:
        userdata = Login.objects.get(id=uid)
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        return render(request, "enquiry.html", {'data': userdata, 'package': packagedetails})
    return redirect(login)


def get_enquiry(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":
            first_name = request.POST.get("fname")
            last_name = request.POST.get("lname")
            email = request.POST.get("mail")
            sub = request.POST.get("subject")
            msg = request.POST.get("message")

            insert_feedback = Inquiry(userid=Login(id=uid), fname=first_name, lname=last_name, email=email, subject=sub, message=msg,
                                     timestamp="",
                                     status="pending")
            insert_feedback.save()
            # Load HTML email template
            full_name = first_name + " " + last_name
            html_message = render_to_string('email_enquiry.html', {'name': full_name})
            send_mail(
                sub,

                'notifications.jansevakendra@gmail.com',
                'INDIADOCS',
                [email],
                html_message=html_message,  # Include the HTML content
                fail_silently=False,
            )
            messages.success(request, "Enquiry Submitted")
            return redirect(enquiry)
        messages.success(request, "Enquiry Did not sent, please provide feedback")
        return redirect(enquiry)
    return redirect(login)


def feedback(request):
    uid = request.session.get("login_id")
    try:
        if uid:
            userdata = Login.objects.get(id=uid)
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            return render(request, "feedback.html", {'data': userdata, 'package': packagedetails})
    except:
        pass
    messages.success(request, "Please Login")
    return redirect(login)


def getfeedback(request):
    if request.method == "POST":
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        email = request.POST.get("mail")
        rate = request.POST.get('rating')
        msg = request.POST.get("message")

        insertfeedback = Feedback(firstname=first_name, lastname=last_name, email=email,
                                     message=msg, rating=rate, timestamp="")

        # Load HTML email template
        full_name = first_name + " " + last_name
        html_message = render_to_string('email_feedback.html', {'name': full_name})
        send_mail(
            'Acknowledgement',

            'notifications.jansevakendra@gmail.com',
            'INDIADOCS',
            [email],
            html_message=html_message,  # Include the HTML content
            fail_silently=False,
        )
        insertfeedback.save()
        messages.success(request, "Feedback Submitted")
        return redirect(feedback)
    messages.success(request, "Feedback did not sent, please try again after sometime.")
    return redirect(feedback)


def public_files(request):
    uid = request.session.get("login_id")
    if uid:
        public_security = Securitytechnique.objects.get(security_name="public")
        public_files1 = Document.objects.filter(document_bin=0, document_security_technique=Securitytechnique(
            id=public_security.id)).exclude(
                userid=Login(id=uid))
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        return render(request, "public_files.html", {'file': public_files1, 'package': packagedetails})
    return redirect(login)


def privatefiles(request):
    uid = request.session.get("login_id")
    if uid:
        try:
            security = Securitytechnique.objects.get(security_name="private")
            private_files = Document.objects.filter(userid=Login(id=uid), document_bin=0, document_security_technique=Securitytechnique(id=security.id))
            context = checkpackage(request)
            packagedetails = context.get('packagedetails')
            context = {'file': private_files, 'package': packagedetails}
            return render(request, "private_files.html", context)
        except:
            pass
    return redirect(login)


def verifypass(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":
            try:
                get_doc_id = request.POST.get("docid")
                get_doc_password = request.POST.get("pass")
                security = Securitytechnique.objects.get(security_name="private")
                document = Document.objects.get(id=get_doc_id, userid__id=uid, document_bin=0,
                                                document_security_technique__id=security.id)
                if check_password(get_doc_password, document.document_password):
                    # Build the file path
                    file_path = document.document.path
                    # Open the file and serve it for download
                    response = FileResponse(open(file_path, 'rb'))
                    response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
                    return response
                else:
                    # Set error message
                    messages.error(request, 'Password Incorrect')
                    return redirect(privatefiles)
            except (Securitytechnique.DoesNotExist, Document.DoesNotExist):
                # Set error message
                messages.error(request, 'Incorrect Password')
                return redirect('privatefiles')
        return redirect('privatefiles')
    return redirect('login')


def download(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":
            get_doc_id = request.POST.get("doc_id")
            sec = request.POST.get("security")
            security = Securitytechnique.objects.get(security_name=sec)
            # Fetching document based on ID and user ID, ignoring security technique
            document = Document.objects.get(id=get_doc_id, document_security_technique=Securitytechnique
            (id=security.id), document_bin=0)

            # Build the file path
            file_path = document.document.path
            # Open the file and serve it for download
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{document.document.name}"'
            return response
        return redirect(indexpage)
    return redirect(login)


def premium(request):
    uid = request.session.get("login_id")
    if uid:
        all_packages = Package.objects.all()
        current_package = Userpackagedetails.objects.get(userid=Login(id=uid), package_status='active')
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        return render(request, "premium.html", {'packages': all_packages, 'cp': current_package, 'package': packagedetails})
    else:
        return redirect(login)


def handle_payment(request):
    if request.method == "POST":
        package_price = request.POST.get("amount")

        context = {'amount': package_price}
        return render(request, "payment.html", context)
    return redirect(premium)


def manage_payment(request):
    uid = request.session.get("login_id")
    if uid:
        card_number = request.POST.get("cardNumber")
        cvv = request.POST.get("cvv")
        expiry_date = request.POST.get("expiryDate")
        amount = request.POST.get("amount")

        card_details = Usercarddetails.objects.first()
        card_num = card_details.card_no
        card_cvv = card_details.cvv
        card_exp = card_details.expiry_date

        package = Package.objects.get(package_price=amount)
        if int(card_number) == card_num and int(cvv) == card_cvv and expiry_date == card_exp:
            transaction_id = uuid.uuid4()
            purchase_date = datetime.now().date()
            expiry_date = purchase_date + timedelta(days=package.package_duration)
            # Format the expiry date as YYYY-MM-DD
            formatted_expiry_date = expiry_date.strftime('%Y-%m-%d')
            get_payment = Payment(userid=Login(id=uid), premium_package_id=Package(id=package.id), payment_status="completed",
                                  package_purchase_date=timezone.now(), transactionid=transaction_id, amount=amount)
            get_payment.save()
            allocate_package = Userpackagedetails(userid=Login(id=uid),premium_package_id=Package(id=package.id),
                                                  package_status="active", package_purchase_date="",
                                                  package_expiry_date=formatted_expiry_date)
            package_update = Userpackagedetails.objects.get(userid=Login(id=uid), package_status="active")
            package_update.package_status = "expired"
            package_update.save()
            allocate_package.save()
            messages.success(request, "Payment Successful")
        else:
            get_payment = Payment(userid=Login(id=uid), premium_package_id=Package(id=package.id),
                                  payment_status="pending",
                                  package_purchase_date=timezone.now(), amount=amount)
            get_payment.save()
            messages.success(request, "Payment Failed")
    return redirect(premium)


def profile(request):
    uid = request.session.get("login_id")
    if uid:
        user_details = Login.objects.get(id=uid)
        context = checkpackage(request)
        packagedetails = context.get('packagedetails')
        return render(request, "profile.html",
                      {'user': user_details, 'package': packagedetails})
    return redirect(login)


def change_password(request):
    uid = request.session.get("login_id")
    if uid:
        if request.method == "POST":
            user_email = request.POST.get("email")
            phone_number = request.POST.get("p_number")
            old_pass = request.POST.get("old_password")
            new_pass = request.POST.get("new_password")
            c_new_pass = request.POST.get("c_new_password")

            user = Login.objects.get(email=user_email, number=phone_number)
            if check_password(old_pass, user.password):
                if new_pass == c_new_pass:
                    hashed_password = make_password(new_pass)
                    user.password = hashed_password
                    user.save()
                    messages.success(request, "Password Changed Successfully")
                    return redirect(profile)
                messages.success(request, "Password Did not Match")
                return redirect(profile)
            messages.success(request, "Incorrect Old Password")
            return redirect(profile)
        return redirect(profile)
    return redirect(login)


def contact(request):
    uid = request.session.get("login_id")
    if uid:
        return redirect(enquiry)
    return render(request, "contact.html")


def get_contact(request):
    uid = request.session.get("login_id")
    if uid:
        return redirect(contact)
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("mail")
        phonenum = request.POST.get("number")
        msg = request.POST.get("message")

        contact_user = Contact(name=full_name, email=email, phone=phonenum, message=msg,
                               timestamp="",
                               status="pending")
        contact_user.save()
        # Load HTML email template
        html_message = render_to_string('email_contact.html', {'name': full_name})
        send_mail(
            'Acknowledgement',

            'notifications.jansevakendra@gmail.com',
            'INDIADOCS',
            [email],
            html_message=html_message,  # Include the HTML content
            fail_silently=False,
        )
        messages.success(request, "Request Submitted")
        return redirect(indexpage)
    messages.success(request, "There is Some Issue")
    return redirect(enquiry)


def forgot_password(request):
    uid = request.session.get("login_id")
    if uid:
        return redirect(indexpage)
    return render(request, "forgotpassword.html")


def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('email')

        try:
            user = Login.objects.get(email=username)
            user_name = user.fname + " " + user.lname
        except Login.DoesNotExist:
            user = None

        if user is not None:
            #################### Password Generation ##########################
            import random
            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                       'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
            numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
            symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

            nr_letters = 6
            nr_symbols = 1
            nr_numbers = 3
            password_list = []

            for char in range(1, nr_letters + 1):
                password_list.append(random.choice(letters))

            for char in range(1, nr_symbols + 1):
                password_list += random.choice(symbols)

            for char in range(1, nr_numbers + 1):
                password_list += random.choice(numbers)

            random.shuffle(password_list)

            password = ""  #we will get final password in this var.
            for char in password_list:
                password += char

            ##############################################################


            # msg = "hello here it is your new password  "+password   #this variable will be passed as message in mail

            ############ code for sending mail ########################
            # Load HTML email template
            html_message = render_to_string('email_password.html', {'password': password, 'name':user_name})
            send_mail(
                'Your New Password',

                'notifications.jansevakendra@gmail.com',
                'INDIADOCS',
                [username],
                html_message=html_message,  # Include the HTML content
                fail_silently=False,
            )

            #now update the password in model
            cuser = Login.objects.get(email=username)
            hashed_password = make_password(password)
            cuser.password = hashed_password
            cuser.save(update_fields=['password'])

            messages.info(request, 'Your New Password is sent to your Registered Email Id, You can change password in Profile.')
            return redirect(indexpage)
        else:
            messages.info(request, 'This account does not exist')
    return redirect(indexpage)


def my_package(request):
    uid = request.session.get("login_id")
    if uid:
        try:
            user_package_details = Userpackagedetails.objects.get(userid=uid, package_status='active')
            payment_details = Payment.objects.filter(userid=Login(id=uid))
            return render(request, "my_package.html", {'package': user_package_details,  'payment': payment_details})
        except:
            pass
    return redirect(login)
