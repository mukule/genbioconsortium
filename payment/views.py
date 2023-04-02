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
from .models import Event, Ticket, Payment
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from datetime import datetime
from django.http import HttpResponseRedirect
from membership.models import MembershipRegistration
from genbioconsortium.settings import PAYPAL_CLIENT_ID, PAYPAL_SECRET


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
