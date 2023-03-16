import requests
from django.shortcuts import render, redirect
from django.urls import reverse
import json
import pycountry
import phonenumbers

url = "https://uat.finserve.africa/authentication/api/v3/authenticate/merchant"
JENGA_API_KEY = "tKDD8S1O1SdHEH8sAYiYCyNyjkdqa6b1tLn1uzaxCOI04KbYGoXg7GyTV1zPbpgKHC+3V8+0Ly2o2FkgsOOI+g=="
headers = {
    "Api-Key": "tKDD8S1O1SdHEH8sAYiYCyNyjkdqa6b1tLn1uzaxCOI04KbYGoXg7GyTV1zPbpgKHC+3V8+0Ly2o2FkgsOOI+g==",
    "Content-Type": "application/json"
    
}
data = {
    "merchantCode": "8799393481",
    "consumerSecret": "fn55Wlh6N3lN5HFr6US4liqK3N0N1u"
}
response = requests.post(url, headers=headers, data=json.dumps(data))
access_token = json.loads(response.content)['accessToken']



def initiate_payment(request):
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        customerPhone = request.POST.get('phone')
        customerFirstName = request.user.username
        lastname = request.user.last_name
        customerEmail = request.user.email
        success_url = request.build_absolute_uri(reverse('payment_complete'))
        cancel_url = request.build_absolute_uri(reverse('payment_error'))
        url = "https://uat.finserve.africa/authentication/api/v3/authenticate/merchant"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        access_token = json.loads(response.content)['accessToken']
        merchantCode = 8799393481

        country_codes = []
        for country in pycountry.countries:
               country_codes.append(country.alpha_2)

        

        context = {
                'access_token': access_token,
                'success_url': success_url, 
                'cancel_url': cancel_url, 
                'name': customerFirstName, 
                'lastname':lastname,
                'email':customerEmail,
                'merchantCode': merchantCode,
                'country_codes': country_codes,
                
                 }

        return render(request, 'payment/index.html', context)


def payment_complete(request):
        return render(request, 'payment/index.html')

def payment_error(request):
        return render(request, 'payment/index.html')