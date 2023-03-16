from django.shortcuts import redirect, render
import base64
import json
import requests


def make_payment(request):
    return render(request, 'payment/index.html')
import requests

consumer_key = "piumJBdCtSxo6GX9p8j8kqcljVJNXJMA"
consumer_secret = "pd7cx9QgbZReJdZ1"
auth_endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

# Set the headers and data for the request

auth_header = {"Authorization": "Basic " + base64.b64encode((consumer_key + ":" + consumer_secret).encode("ascii")).decode("ascii")}

# Send the authentication request
auth_response = requests.get(auth_endpoint, headers=auth_header)

print(auth_response.content)

# Get the access token from the response
access_token = auth_response.json()["access_token"]

#C2B
# Set the C2B transaction endpoint and parameters
c2b_endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer sWhtK7wQGvOeO6jWP9hD5MLmKJve'
}
c2b_payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMzEyMjAzMjA3",
    "Timestamp": "20230312203207",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254704122212,
    "PartyB": 174379,
    "PhoneNumber": 254704122212,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "Biocontrol consortium",
    "TransactionDesc": "Ticket Receipt" 
  }


# Send the C2B transaction request
c2b_response = requests.post(c2b_endpoint, headers=headers, json=c2b_payload)

# Print the response from the server
print(c2b_response.json())