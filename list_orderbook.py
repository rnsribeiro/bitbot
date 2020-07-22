'''
	Descrição
	Retorna informações do livro de negociações
	(orderbook) do Mercado Bitcoin para o par de moedas (coin_pair)
	informado. Diferente do método orderbook público descrito em
	/api-doc/#method_trade_api_orderbook, aqui são fornecidas
	informações importantes para facilitar a tomada de ação de
	clientes TAPI e sincronia das chamadas. Dentre elas, o
	número da última ordem contemplada (latest_order_id) e número
	das ordens do livro (order_id), descritos abaixo. Importante
	salientar que nesse método ordens de mesmo preço não são
	agrupadas como feito no método público.
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
coin_pair = 'BRLXRP'

# Nonce
# Para obter variação de forma simples
# timestamp pode ser utilizado:
tapi_nonce = str(int(time.time()))

# Parâmetros
params = {
    'tapi_method': 'list_orderbook',
    'tapi_nonce': tapi_nonce,
    'coin_pair': coin_pair
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


# Funções que retornam informações com as ordens de compra.
def getOrderbookBidsID(index=0):
	'''
	bids: Lista de ordens de compra (bid) abertas, ordenadas pelo maior preço.
	'''
	return result['response_data']['orderbook']['bids'][index]['order_id']

def getOrderbookBidsQuantity(index=0):
	'''
	quantity: Quantidade disponível para compra ao preço de limit_price.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orderbook']['bids'][index]['quantity']

def getOrderbookBidsLimitPrice(index=0):
	'''
	limit_price: Preço unitário de compra.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orderbook']['bids'][index]['limit_price']

def getOrderbookBidsIsOwner(index=0):
	'''
	is_owner: Informa se ordem pertence ao proprietário da chave TAPI.
	Tipo: Booleano
	Domínio de dados:
	true : Pertence ao proprietário da chave TAPI
	false : Não pertence ao proprietário da chave TAPI
	'''
	return result['response_data']['orderbook']['bids'][index]['is_owner']


# Funções que retornam informações com as ordens de venda
def getOrderbookAsksID(index=0):
	'''
	bids: Lista de ordens de venda (asks) abertas, ordenadas pelo menor preço.
	'''
	return result['response_data']['orderbook']['asks'][index]['order_id']

def getOrderbookAsksQuantity(index=0):
	'''
	quantity: Quantidade disponível para venda ao preço de limit_price.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orderbook']['asks'][index]['quantity']

def getOrderbookAsksLimitPrice(index=0):
	'''
	limit_price: Preço unitário de venda.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orderbook']['asks'][index]['limit_price']

def getOrderbookAsksIsOwner(index=0):
	'''
	is_owner: Informa se a ordem pertence ao proprietário da chave TAPI.
	Tipo: Booleano
	Domínio de dados:
	true : Pertence ao proprietário da chave TAPI
	false : Não pertence ao proprietário da chave TAPI
	'''
	return result['response_data']['orderbook']['asks'][index]['is_owner']

print("Resultados com ordens de compra:")
print(getOrderbookBidsID())
print(getOrderbookBidsQuantity())
print(getOrderbookBidsLimitPrice())
print(getOrderbookBidsIsOwner())
print("Resultados com ordens de venda:")
print(getOrderbookAsksID())
print(getOrderbookAsksQuantity())
print(getOrderbookAsksLimitPrice())
print(getOrderbookAsksIsOwner())
