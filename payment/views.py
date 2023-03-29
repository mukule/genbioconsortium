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





SANDBOX_BASE_URL = "https://api-m.sandbox.paypal.com"
PRODUCTION_BASE_URL = "https://api-m.paypal.com"

@csrf_exempt
def create_paypal_order(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    
    access_token = generate_access_token()
    url = f"{SANDBOX_BASE_URL}/v2/checkout/orders"
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": "USD",
                    "value": str(event.fee)
                }
            }
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post(url, json=payload, headers=headers)
    order = response.json()
    return JsonResponse(order)



@csrf_exempt
def capture_paypal_order(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    data = json.loads(request.body)
    order_id = data['orderID']

    access_token = generate_access_token()
    url = f"{SANDBOX_BASE_URL}/v2/checkout/orders/{order_id}/capture"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.post(url, headers=headers)
    result = response.json()
    status = result['status']
    print(status)
    if status == 'COMPLETED':
        for purchase_unit in result['purchase_units']:
            payments = purchase_unit['payments']
            for capture in payments['captures']:
                amount = Decimal(capture['amount']['value'])
                currency = capture['amount']['currency_code']
                payer_email = result['payment_source']['paypal']['email_address']
                country_code = result['payment_source']['paypal']['address']['country_code']
                time_paid = capture['create_time']
                print(f"Payment captured successfully. Amount: {amount} {currency}")

                # Save ticket object
                num_tickets_sold = Ticket.objects.filter(event=event).count()
                ticket_number = f'T{event.id:06d}-{num_tickets_sold+1:06d}'
                ticket = Ticket(event=event, user=request.user, num_tickets=1, ticket_number=ticket_number,
                                price=amount, paid=True, country_code=country_code, time_paid=time_paid,
                                currency=currency, payer_email=payer_email)
                ticket.save()

        # Redirect to payment done page after all captures have been processed
        print('Redirecting to payment_done')
        print(reverse('payment:payment_done'))
        return HttpResponseRedirect(reverse('payment:payment_done'))
        
    else:
        print("Payment capture failed")

    return HttpResponse()

@csrf_exempt
def payment_done(request):
    return HttpResponseRedirect('/payment/payment_done/')


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