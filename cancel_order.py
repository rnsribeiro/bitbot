'''
cancel_order Descrição:
Cancela uma ordem, de venda ou compra, de acordo com o ID e par de moedas informado.
O retorno contempla o sucesso ou não do cancelamento, bem como os dados e status
atuais da ordem. Somente ordens pertencentes ao próprio usuário podem ser canceladas.
'''

import hashlib
import hmac
import json
import time
import userinfo

import place_sell_order as sellOrder

from http import client
from urllib.parse import urlencode

# Constantes
MB_TAPI_ID = userinfo.id
MB_TAPI_SECRET = userinfo.secret
REQUEST_HOST = 'www.mercadobitcoin.net'
REQUEST_PATH = '/tapi/v3/'

# Parâmetros que podem ser passado por linha de comando.
coin_pair = 'BRLXRP'

# Para obter variação de forma simples
# timestamp pode ser utilizado:
tapi_nonce = str(int(time.time()))

sellOrder.placeSellOrder(coin_pair,0.1,1.065)

time.sleep(30)

order_id = sellOrder.getOrderId()

def cancelOrder(coin_pair,order_id):
    coin_pair=coin_pair
    order_id=order_id

cancelOrder(coin_pair,order_id)

# Parâmetros
params = {
    'tapi_method': 'cancel_order',
    'tapi_nonce': tapi_nonce,
    'coin_pair': coin_pair,
    'order_id': order_id    
}

params = urlencode(params)

# Gerar MAC
params_string = REQUEST_PATH + '?' + params
H = hmac.new(bytes(MB_TAPI_SECRET, encoding='utf8'), digestmod=hashlib.sha512)
H.update(params_string.encode('utf-8'))
tapi_mac = H.hexdigest()

# Gerar cabeçalho da requisição
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'TAPI-ID': MB_TAPI_ID,
    'TAPI-MAC': tapi_mac
}

# Realizar requisição POST
try:
	conn = client.HTTPSConnection(REQUEST_HOST)
	conn.request("POST", REQUEST_PATH, params, headers)

	# Mostra o resultado
	resp = conn.getresponse()
	resp = resp.read()

	result = json.loads(resp)
	
	print(json.dumps(result, indent=4))

finally:
    if conn:
        conn.close()