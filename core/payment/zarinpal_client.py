from core import settings
import requests
import json

class ZarinPalBox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://127.0.0.1:8000/payment/verify/"

    def __init__(self, merchant_id="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"):
        self.merchant_id = merchant_id

    def payment_request(self, amount):

        payload = {
            "merchant_id":self.merchant_id,
            "amount": amount,
            "callback_url":self._callback_url,
            "description": "This is a test payment.",
            "metadata": {"mobile":"0930xxxxxxx", "email":"info@gmail.com"}
        }
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url=self._payment_request_url, headers=headers, json=payload)
        return response.json()


    def payment_verify(self, amount, authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        response = requests.post(url=self._payment_verify_url, headers=headers, json=payload)
        return response.json()
    
    def generate_payment_url(self, authority):
        return f"{self._payment_page_url}{authority}"