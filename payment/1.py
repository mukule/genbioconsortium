#  # Get the user's email address and the amount to be paid
#     email = request.user.email
#     amount = 1000 # In kobo (NGN)

#     # Generate a unique reference for the payment
#     reference = f"ref-{request.user.username}"

#     # Set up the payload for the Flutterwave API
#     payload = {
#         "email": email,
#         "amount": amount,
#         "reference": reference,
#         "public_key": public_key,
#         "currency": "KES"
#     }

#     # Make a POST request to the Flutterwave API to initiate the payment
#     response = requests.post("https://api.flutterwave.com/v3/payments", json=payload, headers={
#         "Authorization": f"Bearer {secret_key}"
#     })

#     # If the payment was successfully initiated, save the transaction to the database and redirect the user to the payment page
#     if response.status_code == 200:
#         payment_response = response.json()
#         transaction = transaction(user=request.user, amount=amount, reference=reference)
#         transaction.save()
#         return redirect(payment_response["data"]["link"])

#     # If there was an error, display an error message
#     else:
#         error_message = response.json()["message"]
#         return render(request, "payment/payment_error.html", {"error_message": error_message})



# ###############################################
# # import json
# # from json.decoder import JSONDecodeError
# # import requests
# # from django.contrib.auth.decorators import login_required
# # from django.shortcuts import render, redirect
# # from .models import Transaction
# # from genbioconsortium.settings import flutterwave_secret_key
# # from django.urls import reverse


# # @login_required
# # def initiate_payment(request):
# #     if request.method == "POST":
# #         amount = request.POST.get("amount")
# #         username = request.user.username
# #         email = request.user.email
# #         reference = f"ref-{request.user.username}"

# #         payload = {
# #             "tx_ref": reference,
# #             "amount": amount,
# #             "currency": "KES",
# #             "redirect_url": request.build_absolute_uri(reverse("payment_complete")),
# #             "payment_options": "card, mpesa",
# #             "meta": {
# #                 "user_id": request.user.id
# #             },
# #             "customer": {
# #                 "email": email,
# #                 "phonenumber": "254704122212",
# #                 "name": username
# #             },
# #             "customizations": {
# #                 "title": "Genbioconsortium Payment",
# #                 "description": "Payment for genbioconsortium services",
# #                 "logo": "https://assets.piedpiper.com/logo.png"
# #             }
# #         }

# #         headers = {
# #             "Authorization": f"Bearer {flutterwave_secret_key}",
# #             "Content-Type": "application/json"
# #         }

# #         try:
# #             response = requests.post("https://api.flutterwave.com/v3/payments", 
# #                                      json=payload, 
# #                                      headers=headers)
# #             response.raise_for_status()
# #             payment_response = response.json()
# #             # Save the transaction details to the database
# #             transaction = Transaction(user=request.user, amount=amount, reference=reference)
# #             transaction.save()
# #             # Redirect the user to the payment link returned by the API
# #             return redirect(payment_response["data"]["link"])
# #         except requests.exceptions.HTTPError as http_err:
# #             error_message = str(http_err)
# #         except JSONDecodeError as json_err:
# #             error_message = "Invalid response from payment gateway"
# #         except Exception as err:
# #             error_message = str(err)

# #         return render(request, "payment/payment_error.html", {"error_message": error_message})

# #     return render(request, "payment/index.html")


# # def payment_complete(request):
# #     return render(request, 'payment/payment_complete.html')

# from django.shortcuts import redirect, render
# import base64
# import requests
# from genbioconsortium.settings import consumer_key,consumer_secret,auth_endpoint
# from django.contrib.auth.decorators import login_required


#  #Set the headers and data for the request

# auth_header = {"Authorization": "Basic " + base64.b64encode((consumer_key + ":" + consumer_secret).encode("ascii")).decode("ascii")}

# # Send the authentication request
# auth_response = requests.get(auth_endpoint, headers=auth_header)

# print(auth_response.content)

# # Get the access token from the response
# access_token = auth_response.json()["access_token"]
# print(access_token)

# #C2B
# # Set the C2B transaction endpoint and parameters
# c2b_endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
# headers = {
#   'Content-Type': 'application/json',
#   'Authorization': 'Bearer fCrlX6vAGTi8aX3c1ZqzdAyT9PGf'
# }

# @login_required
# def initiate_payment(request):
#      if request.method == "POST":
#          amount = request.POST.get("amount")
#          username = request.user.username
#          email = request.user.email
#          reference = f"ref-{request.user.username}"
#          c2b_payload = {
#             "BusinessShortCode": 174379,
#             "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjMwMzEyMjAzMjA3",
#             "Timestamp": "20230312203207",
#             "TransactionType": "CustomerPayBillOnline",
#             "Amount": amount,
#             "PartyA": 254704122212,
#             "PartyB": 174379,
#             "PhoneNumber": 254704122212,
#             "CallBackURL": "https://mydomain.com/path",
#             "AccountReference": "Biocontrol consortium",
#             "TransactionDesc": "Ticket Receipt" 
#             }
#          # Send the C2B transaction request
#          c2b_response = requests.post(c2b_endpoint, headers=headers, json=c2b_payload)
#          print(c2b_response.json())

#      return render(request, "payment/index.html")


