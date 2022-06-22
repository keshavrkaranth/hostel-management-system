from django.conf import settings
from django.core.mail import send_mail


def sendMail(emai,  recipient, name=None,password=None, message=None, subject=None):
    if password:
        subject = "Your credential for logging in for HOSTEL MANAGEMENT Website"
        message = f"Hello {name} This is your credentials for logging in for hostel management website\nUSERNAME:{emai}\nPASSWORD:{password}\nHappy to see you again. "

    email_from = settings.EMAIL_HOST_USER
    rec = [recipient]
    send_mail(subject, message, email_from, rec)
