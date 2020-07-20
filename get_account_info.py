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

# variável que pode ser passada por parâmetro
#coin='xrp'

# Nonce
# Para obter variação de forma simples
# timestamp pode ser utilizado:
tapi_nonce = str(int(time.time()))

# Parâmetros
params = {
    'tapi_method': 'get_account_info',
    'tapi_nonce': tapi_nonce
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

finally:
    if conn:
        conn.close()


def getBalanceAvailable(coin='btc'):
	'''
	available: Saldo disponível para operações.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['balance'][coin]['available']

def getBalanceTotal(coin='btc'):
	'''
	total: Saldo disponível mais valores em ordens de venda abertas e transferências não autorizadas.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['balance'][coin]['total']

def getBalanceAmountOpenOrders(coin='btc'):
	'''
	amount_open_orders: Quantidade de ordens de compra ou venda abertas.
	Tipo: Inteiro
	'''
	return result['response_data']['balance'][coin]['amount_open_orders']

def getWithdrawalLimitsAvailable(coin='btc'):
	'''
	withdrawal_limits: Limites de saques e transferências.
	available: Limite de transferência disponível.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['withdrawal_limits'][coin]['available']

def getWithdrawalLimitsTotal(coin='btc'):
	'''
	total: Limite de transferência.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['withdrawal_limits'][coin]['total']

coin='xrp'
print(getBalanceAvailable(coin))
print(getBalanceTotal(coin))
print(getBalanceAmountOpenOrders(coin))
print(getWithdrawalLimitsAvailable(coin))
print(getWithdrawalLimitsTotal(coin))
