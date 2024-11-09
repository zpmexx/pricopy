from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from SushiBar.settings import P24
import hashlib
import urllib
import requests


class Przelewy24:
    id = 130191 #id nadane przez P24
    crcKey = "43340078b513ca2d" #klucz CRC z panelu P24
    apikey = "4ec4564dd12c62266e3f0eb1ef9e8018"


    def registerPayment(order,email):
        url = P24['url']+"register/"
        payload = {'merchantId': Przelewy24.id,
                   'posId': Przelewy24.id,
                   'sessionId': order.sessionId,
                   'amount': int(order.total_price * 100),
                   'currency': "PLN",
                   'description': "Zamowienie",
                   'email': email,
                   'country': "PL",
                   'language': "pl",
                   'urlReturn': P24['urlReturn']+order.sessionId,
                   'urlStatus': P24['urlStatus']+order.sessionId,
                   'sign': order.getRegistrationOrderSign()}
        # headers = {
        #     'Authorization': 'Basic MTMwMTkxOjRlYzQ1NjRkZDEyYzYyMjY2ZTNmMGViMWVmOWU4MDE4',
        #     'Cookie': 'PHPSESSID=548b5c7c94bc26f5e34cde085e3c4e7c'
        # }

        response = requests.request("POST", url, data=payload, auth=HTTPBasicAuth(Przelewy24.id, Przelewy24.apikey))
        #response = requests.request("POST", url, headers=headers, data=payload)
        print("registerPayment: ", response.text)

        return response.text

    def getPaymentInfo(sessionId):
        url = P24['url']+"by/sessionId/"+sessionId
        # headers = {
        #     "Authorization": "Basic MTMwMTkxOjRlYzQ1NjRkZDEyYzYyMjY2ZTNmMGViMWVmOWU4MDE4",
        #     "Content-Type": "application/json",
        #     "Postman-Token": "ff930d0f-66a2-4477-b9e5-0297f12ef39c",
        #     "cache-control": "no-cache"
        # }
        r = requests.get(url, auth=HTTPBasicAuth(Przelewy24.id, Przelewy24.apikey))

        return r.text

        
    @csrf_exempt
    def p24status(request):
        if request.method == "POST":
            order = Przelewy24.getOrder(request)
        else:
            return HttpResponse("No Post Data!")
        if order is not None:
            receivedSign = request.POST.get("p24_sign", "")
            result = Przelewy24.confirmPayment(order, receivedSign)
        else:
            return HttpResponse("None of orders fit!")
        if result == 'error=0':
                status = Przelewy24.setOrderAsPayd(order)
                return HttpResponse(status)
        else:
            return HttpResponse("Niepoprawana płatność!")

    # zamiast tworzyć obiekt z danych z requestu. weź tylko
    # znajdź zamówienie na podstawie p24_session_id z własnej bazy
    # z requesta pobierz dodatkowo tylko p24_order_id


    def getOrder(request,orderId):
        from .models import Order
        order = Order.objects.get(sessionId=sessionId)
        orderId = request.POST.get('p24_order_id')
        order.paymentOrderId = orderId
        order.save()
        return order


    def confirmPayment(order):
        url = P24['url']+"verify"

        payload = {'merchantId': Przelewy24.id,
                   'posId': Przelewy24.id,
                   'sessionId': order.sessionId,
                   'amount': int(order.total_price * 100),
                   'currency': order.currency,
                   'orderId': order.paymentOrderId,
                   'sign': order.getVerifySign()}
        # headers = {
        #     'Authorization': 'Basic MTMwMTkxOjRlYzQ1NjRkZDEyYzYyMjY2ZTNmMGViMWVmOWU4MDE4',
        #     'Cookie': 'PHPSESSID=548b5c7c94bc26f5e34cde085e3c4e7c'
        # }

        #response = requests.request("PUT", url, headers=headers, data=payload)
        response = requests.request("PUT", url, data=payload, auth=HTTPBasicAuth(Przelewy24.id, Przelewy24.apikey))
        print("confirmPayment: ", response.text)

        return response.text

    # Tutaj ustaw odniesienie do zamówienia w bazie
    # i zmiana jego statusu
    def setOrderAsPayd(order):
        return "OK"