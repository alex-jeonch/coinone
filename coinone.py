import requests


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


