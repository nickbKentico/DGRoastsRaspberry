#!/usr/bin/python2.7
import socket, json, time, requests

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

DISPLAY_CURRENCIES = ['USD', 'EUR', 'GBP']

while True:
    response = requests.get("https://blockchain.info/ticker")
    print(response.text)
    ticker = response.json()
    currencies = []
    for currency_name in DISPLAY_CURRENCIES:
        print(currency_name)
        currencies.append(dict(
            val = ticker[currency_name]['last'],
            sym = ticker[currency_name]['symbol'],
        ))

    data = json.dumps(currencies, ensure_ascii=False)
    print(data)
    bitcoinUpdate = "bitcoin/update:%s"
    SendLoad = bitcoinUpdate % data
    
    sock.sendto(SendLoad.encode("utf8"), ('127.0.0.1', 4444))

    time.sleep(60)