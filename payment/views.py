import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import base64
from base64 import b64encode
from genbioconsortium.settings import consumer_key, consumer_secret
import datetime
from django.views.decorators.csrf import csrf_exempt
from .decorators import user_not_authenticated

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
shortcode = 174379






@login_required
def index(request):
    if request.method == 'POST':
        # Get form data
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        

        # Get an OAuth access token
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
        querystring = {"grant_type": "client_credentials"}

        credentials = f"{consumer_key}:{consumer_secret}"
        credentials_b64 = base64.b64encode(credentials.encode("ascii")).decode("ascii")

        headers = {"Authorization": f"Basic {credentials_b64}"}

        response = requests.request("GET", url, headers=headers, params=querystring)

        response_json = response.json()
        access_token = response_json["access_token"]


        # Make M-Pesa payment request
        passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
        password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode("ascii")).decode("ascii")
        
       
        
        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
       
        payload = {
            'BusinessShortCode': shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': 1,
            'PartyA': phone_number,
            'PartyB': 174379,
            'PhoneNumber': phone_number,
            'CallBackURL': 'http://python.kenyaweb.com/',
            'AccountReference': 'conference',
            'TransactionDesc': 'ticket',
        }

        response = requests.post(url, headers=headers, json=payload)
      
       # Check payment status and redirect to appropriate view
       # Check payment status and redirect to appropriate view
        if response.status_code == 200:
            response_json = response.json()
            if response_json["ResponseCode"] == "0":
                return redirect('payment_complete')
            else:
                return redirect('payment_fail')
        else:
        
         return render(request, 'payment/payment_error.html', {'error_message': 'HTTP Error: {}'.format(response.status_code)})
    return render(request, 'payment/index.html')


def payment_complete(request):
    return render(request, 'payment/payment_complete.html')

def payment_fail(request):
    message = "Payment failed!"
    return HttpResponse(message)
def payment_success(request):
    return render(request, 'payment/payment_success.html')

def payment_complete_error(request):
    return render(request, 'payment/payment_complete_error.html')

@csrf_exempt
def daraja_webhook(request):
    data = json.loads(request.body.decode('utf-8'))
    result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
    if result_code == 0:
        return redirect('payment_success')
    else:

        return HttpResponse(status=200)
