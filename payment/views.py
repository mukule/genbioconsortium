from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .forms import TicketForm
from .models import *
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from urllib.request import urlopen
from urllib.parse import urlencode
from paypal.standard.models import ST_PP_COMPLETED
from django.http import HttpResponseBadRequest
from paypal.standard.ipn.models import PayPalIPN
from django.http import HttpResponseServerError
import paypalrestsdk
from genbioconsortium.settings import PAYPAL_CLIENT_ID, PAYPAL_SECRET, access_token
from django.http import JsonResponse
import json
from paypalrestsdk import Order
import requests
import base64
import uuid
from .models import Event, Ticket, Payment
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from datetime import datetime
from django.http import HttpResponseRedirect
from membership.models import MembershipRegistration


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
    url = f"{SANDBOX_BASE_URL}/v2/checkout/orders"
    payload = {
        "intent": "CAPTURE",
        "application_context": {
            "brand_name": "African Genetic Biocontrol Consortium",
            "locale": "en-US",
            "landing_page": "BILLING",
            "user_action": "PAY_NOW",
            "webhook_urls": [
                {
                    "url": 'http://{}{}'.format(host,
                                           reverse('payment:paypal_webhook'))
                }
            ]
        },
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(membership_reg.membership_price)

                },
                "reference_id": str(membership_reg.id)
                
            }
        ]
    }
    print(payload)
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
    print(request.body)
    return HttpResponse(status=200)


@csrf_exempt
def payment_done(request):
    return HttpResponseRedirect('/payment/payment_done/')


# Your code here


class EventListView(ListView):
    model = Event
    template_name = 'payment/index.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'payment/event_detail.html'

    
 

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/payment_fail.html')