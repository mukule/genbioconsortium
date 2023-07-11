import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import base64
from django.views.decorators.csrf import csrf_exempt
import uuid
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from datetime import datetime
from django.http import HttpResponseRedirect
from membership.models import MembershipRegistration,Payment
from genbioconsortium.settings import PAYPAL_CLIENT_ID, PAYPAL_SECRET
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def generate_access_token():
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}"
    auth = auth.encode("ascii")
    auth = base64.b64encode(auth).decode("ascii")
    url = f"{SANDBOX_BASE_URL}/v1/oauth2/token"
    payload = "grant_type=client_credentials"
    headers = {
        "Authorization": f"Basic {auth}"
    }
    response = requests.post(url, data=payload, headers=headers)
    data = response.json()
    
    return data["access_token"]



SANDBOX_BASE_URL = "https://api-m.sandbox.paypal.com"
PRODUCTION_BASE_URL = "https://api-m.paypal.com"

@csrf_exempt
def create_paypal_order(request):
    membership_reg = get_object_or_404(MembershipRegistration, user=request.user)
    access_token = generate_access_token()
    host = request.get_host()
    webhook_url = 'https://{}{}'.format(host, reverse('payment:paypal_webhook'))
    cancel_url = 'https://{}{}'.format(host, reverse('payment:payment_canceled'))
    print(membership_reg.registration_type)
    url = f"{SANDBOX_BASE_URL}/v2/checkout/orders"
    payload = {
    "intent": "CAPTURE",
    "payer": {
        "name": {
            "given_name": membership_reg.first_name,
            "surname": membership_reg.last_name
        },
        "email_address": membership_reg.email
    },
    "application_context": {
        "brand_name": "The African Genetic Biocontrol Consortium",
        "locale": "en-US",
        "landing_page": "BILLING",
        "user_action": "PAY_NOW",
        "webhook_urls": [
            {
                "url": webhook_url
            }
        ],
        "cancel_url": cancel_url
    },
    "purchase_units": [
        {
            "amount": {
                "currency_code": "USD",
                "value": str(membership_reg.membership_price)
            },
            "reference_id": str(membership_reg.id),
            "description": f"membership for {membership_reg.membership}",
        }
    ]
}


    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    order = response.json()
    print(order)
    
    return JsonResponse(order)



@csrf_exempt
def paypal_webhook(request):
    print('PayPal webhook called')
    payload = json.loads(request.body)
    print('Payload:', payload)

    # Retrieve payment details from PayPal API
    access_token = generate_access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    order_id = payload.get("orderID")
    print('order id:', order_id)
    url = f"{SANDBOX_BASE_URL}/v2/checkout/orders/{order_id}"
    response = requests.get(url, headers=headers)
    payment_details = response.json()
    print(payment_details)

    # Check if payment status is 'COMPLETED'
    if payment_details['status'] == 'COMPLETED':
        # Payment was already successful
        print('payment is captured successfully')
        # Do something here, e.g. mark the order as paid in your system
        purchase_unit = payment_details['purchase_units'][0]
        payer = payment_details['payer']
        captures = purchase_unit['payments']['captures'][0]

        first_name = payer['name']['given_name']
        last_name = payer['name']['surname']
        full_name = f"{first_name} {last_name}"

        # Retrieve the MembershipRegistration object
        reference_id = purchase_unit['reference_id']
        membership_reg = MembershipRegistration.objects.get(id=reference_id)

        amount = captures['amount']['value']  # Get the amount from PayPal response
        gross_pay = captures['seller_receivable_breakdown']['gross_amount']['value']  # Get the gross_pay from PayPal response

        payment = Payment.objects.create(
            user=request.user,
            membership_registration=membership_reg,
            transaction_id=order_id,  # Set the transaction_id field
            amount=amount,
            timestamp=datetime.now(),
            full_name=full_name,
            membership_type=purchase_unit['description'],
            payment_id=captures['id'],
            email=payer['email_address'],
            payment_status=payment_details['status'],
            gross_pay=gross_pay,  # Set the gross_pay field
            paypal_fee=captures['seller_receivable_breakdown']['paypal_fee']['value'],
            net_pay=captures['seller_receivable_breakdown']['net_amount']['value'],
            payer_id=payer['payer_id']
        )
        # Mark the registration as paid
        membership_reg.paid = True
        membership_reg.save()

        # Send email notification
        mail_subject = '1ST GLOBAL CONGRESS ON EMERGING GENETIC BIOCONTROL TECHNOLOGIES'
        message = f"Thank you for your payment. You have successfully paid for the congress.\n\nPayment Details:\nTransaction ID: {order_id}\nAmount: USD {amount}\nMembership Type: {purchase_unit['description']}\nTimestamp: {datetime.now()}"
        # to_email = payer['email_address']  # Use the payer's email address
        to_email = request.user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        print(to_email)

        context = {'message': 'Payment completed successfully.'}
        return render(request, 'payment/payment_complete.html', context)
    
    else:
        # Payment was not successful
        # Do something here, e.g. mark the order as failed in your system
        return HttpResponse(status=400)


@login_required
def payment_done(request):
    try:
        latest_payment = Payment.objects.filter(user=request.user).latest('timestamp')
        return render(request, 'payment/payment_complete.html', {'payment': latest_payment})
    except Payment.DoesNotExist:
        return render(request, 'payment/payment_complete.html', {'error_message': 'No payment found.'})


def payment_canceled(request):
    return render(request, 'payment/payment_error.html')

