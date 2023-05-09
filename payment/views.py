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
from membership.models import MembershipRegistration
from genbioconsortium.settings import PAYPAL_CLIENT_ID, PAYPAL_SECRET
from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest


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
    return_url = 'https://{}{}'.format(host, reverse('payment:payment_done'))
    cancel_url = 'https://{}{}'.format(host, reverse('payment:payment_canceled'))
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
        "return_url": return_url,
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
        print('payment is captured succesfully')
        # Do something here, e.g. mark the order as paid in your system
        return redirect('payment:payment_done')

    # Capture payment
    url = f"{SANDBOX_BASE_URL}/v2/checkout/orders/{order_id}/capture"
    response = requests.post(url, headers=headers)
    payment_details = response.json()

    # Check if payment status is 'COMPLETED'
    if payment_details['status'] == 'COMPLETED':
        # Payment was successful
        # Do something here, e.g. mark the order as paid in your system
        return redirect('payment:payment_done')
    else:
        # Payment was not successful
        # Do something here, e.g. mark the order as failed in your system
        return HttpResponse(status=400)


@csrf_exempt
def payment_done(request):
    return render(request, 'payment/payment_complete.html')





# Your code here

def payment_canceled(request):
    return render(request, 'payment/payment_error.html')
