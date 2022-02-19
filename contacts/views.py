from django.shortcuts import render, redirect
from django.contrib import messages
from contacts.models import Contacts
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
from helper.email_smtp_ssl import send_email

# load local environment variables
load_dotenv()

# Create your views here.
def contacts(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contacts.objects.all().filter(listing_id=listing_id,
                user_id=user_id
            )

            if has_contacted:
                messages.error(request, 
                'You have already made an inquiry for this listing'
                )

                return redirect('/listings/' + listing_id)

        contacts = Contacts(listing=listing, 
            listing_id=listing_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user_id=user_id
        )

        # send mail
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
        #     os.environ.get('email_host_user'),
        #     [realtor_email, 'noreply.romadv@gmail.com'],
        #     fail_silently=False
        # )
        email_message = """Subject: Property Listing Inquiry

        There has been an inquiry for """ + listing + """. Sign into the admin panel for more info."""

        email_success, email_error = send_email(
            sender_email=os.environ.get('email_host_user'),
            password=os.environ.get('email_host_password'),
            receiver_email=[realtor_email, 'noreply.romadv@gmail.com'],
            message=email_message
        )

        if not email_success:
            messages.error(request, 
            f'Unable to send request to realtor: {email_error}'
            )
            return redirect('/listings/' + listing_id)

        contacts.save()
        messages.success(request, 
        'Your request has been submitted, a realtor will back to you soon'
        )
        return redirect('/listings/' + listing_id)