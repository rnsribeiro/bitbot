'''
place_sell_order Descrição:
Abre uma ordem de venda (sell ou ask) do par de moedas, 
quantidade de moeda digital e preço unitário limite informados.
A criação contempla o processo de confrontamento da ordem com o livro de negociações.
Assim, a resposta pode informar se a ordem foi executada (parcialmente ou não)
imediatamente após sua criação e, assim, se segue ou não aberta e ativa no livro.
'''

import hashlib
import hmac
import json
import time
import userinfo

from http import client
from urllib.parse import urlencode

# Constantes
MB_TAPI_ID = userinfo.id
MB_TAPI_SECRET = userinfo.secret
REQUEST_HOST = 'www.mercadobitcoin.net'
REQUEST_PATH = '/tapi/v3/'

# Parâmetros que podem ser passado por linha de comando.
coin_pair = 'BRLXRP'
quantity = 0.1
limit_price = 1.0601 # Preço em Reais R$

# Nonce
# Para obter variação de forma simples
# timestamp pode ser utilizado:
tapi_nonce = str(int(time.time()))


def placeSellOrder(coin_pair,quantity,limit_price):
    coin_pair=coin_pair
    quantity=quantity
    limit_price=limit_price

placeSellOrder(coin_pair,quantity,limit_price)

# Parâmetros
params = {
    'tapi_method': 'place_sell_order',
    'tapi_nonce': tapi_nonce,
    'coin_pair': coin_pair,
    'quantity': quantity,
    'limit_price':limit_price
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
	
	#print(json.dumps(result, indent=4))

finally:
    if conn:
        conn.close()



def getOrderId():
    '''
    order_id: Número de identificação da ordem, único por coin_pair.
    Tipo: Inteiro
    '''
    return 	result['response_data']['order']['order_id']

def getOrderCoinPair():
    '''
    coin_pair: Par de moedas.
    Tipo: String
    Domínio de dados:
    BRLBTC : Real e Bitcoin
    BRLBCH : Real e BCash
    BRLETH : Real e Ethereum
    BRLLTC : Real e Litecoin
    BRLXRP : Real e XRP (Ripple)
    BRLMBPRK01 : Real e Precatório MB SP01
    BRLMBPRK02 : Real e Precatório MB SP02
    BRLMBPRK03 : Real e Precatório MB BR03
    BRLMBPRK04 : Real e Precatório MB RJ04
    BRLMBCONS01 : Real e Cota de Consórcio
    BRLUSDC : Real e USDC (USD Coin)
    '''
    return 	result['response_data']['order']['coin_pair']

print(getOrderId())
print(getOrderCoinPair())
