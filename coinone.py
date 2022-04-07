import requests
import key
import base64
import hashlib
import hmac
import httplib2
import time
import json

access_key = key.access_key
secret_key = bytes(key.secret_key,'utf-8')


#public requests
def get_orderbook(coin):

    url = 'https://api.coinone.co.kr/orderbook/?currency=' + coin

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)

    return response.text


def get_ticker(coin):

    url = 'https://api.coinone.co.kr/ticker/?currency=' + coin

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers)

    return response.text


# private requests
def get_encoded_payload(payload):
    payload['nonce'] = int(time.time() * 1000)

    dumped_json = json.dumps(payload)
    encoded_json = base64.b64encode(bytes(dumped_json,'utf-8'))

    return encoded_json


def get_signature(encoded_payload):
    signature = hmac.new(secret_key, encoded_payload, hashlib.sha512)

    return signature.hexdigest()


def get_response(action, payload):
    url = '{}{}'.format('https://api.coinone.co.kr/', action)

    encoded_payload = get_encoded_payload(payload)

    headers = {
        'Content-type': 'application/json',
        'X-COINONE-PAYLOAD': encoded_payload,
        'X-COINONE-SIGNATURE': get_signature(encoded_payload),
    }

    http = httplib2.Http()
    response, content = http.request(url, 'POST', body=encoded_payload, headers=headers)

    return content


def get_balance():
    url = 'v2/account/balance/'

    payload = {
        'access_token': access_key,
    }

    response = get_response(url, payload)
    #content = json.loads(response.text)

    return response


def cancle_order(coin,order_id,price,qty):
    url = 'v2/order/cancel'

    payload = {
        'access_token': access_key,
        'order_id': order_id,
        'price':price,
        'qty':qty,
        'is_ask':'1',
        'currnecy':coin,

    }

    response = get_response(url, payload)

    return response


def limit_buy(coin,price,qty):
    url = 'v2/order/limit_buy'

    payload = {
        'access_token': access_key,
        'price': price,
        'qty': qty,
        'currnecy': coin,

    }

    response = get_response(url, payload)

    return response


def limit_sell(coin,price,qty):
    url = 'v2/order/limit_sell'

    payload = {
        'access_token': access_key,
        'price': price,
        'qty': qty,
        'currnecy': coin,

    }

    response = get_response(url, payload)

    return response


def limit_orders(coin,price,qty):
    url = 'v2/order/limit_orders'

    payload = {
        'access_token': access_key,
        'currnecy': coin,

    }

    response = get_response(url, payload)

    return response


def complete_orders(coin,price,qty):
    url = 'v2/order/complete_orders'

    payload = {
        'access_token': access_key,
        'currnecy': coin,

    }

    response = get_response(url, payload)

    return response


def order_information(coin,order_id):
    url = 'v2/order/complete_orders'

    payload = {
        'access_token': access_key,
        'order_id':order_id,
        'currnecy': coin,

    }

    response = get_response(url, payload)

    return response


def coin_transaction_history(coin):
    url = 'v2/order/complete_orders'

    payload = {
        'access_token': access_key,
        'currnecy': coin,

    }

    response = get_response(url, payload)

    return response
