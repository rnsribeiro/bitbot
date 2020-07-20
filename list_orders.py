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
    'tapi_method': 'list_orders',
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
	#print('status: {}'.format(response['status_code']))
	#print(json.dumps(response,indent=4))

	# Exibe a resposta do servidor
	#print resp.status, resp.reason

	# Exibe o resultado na tela de forma legivel
	#print json.dumps(data, sort_keys=True, indent=4, separators=(',',': '))


finally:
    if conn:
        conn.close()


def getOrdersId(index=0):
	''' order_id: Número de identificação da ordem, único por coin_pair.
	Tipo: Inteiro
	'''
	return result['response_data']['orders'][index]['order_id']

def getOrdersCoinPair(index=0):
	''' coin_pair: Par de moedas.
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
	return result['response_data']['orders'][index]['coin_pair']

def getOrdersOrderType(index=0):
	''' order_type: Tipo da ordem a ser filtrado.
	Tipo: Inteiro
	Domínio de dados:
	1 : Ordem de compra
	2 : Ordem de venda
	'''
	return result['response_data']['orders'][index]['order_type']

def getOrdersStatus(index=0):
	''' status: Estado da ordem.
	Tipo: Inteiro
	Domínio de dados:
	2 : open : Ordem aberta, disponível no livro de negociações. Estado intermediário.
	3 : canceled : Ordem cancelada, executada parcialmente ou sem execuções. Estado final.
	4 : filled : Ordem concluída, executada em sua totalidade. Estado final.
	'''
	return result['response_data']['orders'][index]['status']

def getOrdersHasFills(index=0):
	''' has_fills: Indica se a ordem tem uma ou mais execuções. Auxilia na identificação de ordens parcilamente executadas.
	Tipo: Booleano
	false : Sem execuções.
	true : Com uma ou mais execuções.
	'''
	return result['response_data']['orders'][index]['has_fills']

def getOrdersQuantity(index=0):
	''' quantity: Quantidade da moeda digital a comprar/vender ao preço de limit_price.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orders'][index]['quantity']

def getOrdersLimitPrice(index=0):
	''' limit_price: Preço unitário máximo de compra ou mínimo de venda.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orders'][index]['limit_price']

def getOrdersExecutedQuantity(index=0):
	''' limit_price: Preço unitário máximo de compra ou mínimo de venda.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orders'][index]['executed_quantity']

def getOrdersExecutedPriceAvg(index=0):
	''' executed_price_avg: Preço unitário médio de execução.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orders'][index]['execuder_price_avg']

def getOrdersFee(index=0):
	''' fee: Comissão da ordem, para ordens de compra os valores são em moeda digital, para ordens de venda os valores são em Reais.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['orders'][index]['fee']

def getOrdersCreatedTimestamp(index=0):
	''' created_timestamp: Data e hora de criação da ordem.
	Tipo: String
	Formato: Era Unix
	'''
	return result['response_data']['orders'][index]['']

def getOrdersUpdatedTimestamp(index=0):
	''' updated_timestamp: Data e hora da última atualização da ordem. Não é alterado caso a ordem esteja em um estado final (ver status).
	Tipo: String
	Format: Era Unix
	'''
	return result['response_data']['orders'][index]['updated_timestamp']

def getOrdersOperationsId(index=0,indexOperation=0):
	'''operation_id: Número de identificação da operação, único por coin_pair
		Tipo: Inteiro
	'''
	return result['response_data']['orders'][index]['operations'][indexOperation]['operation_id']

def getOrdersOperationsQuantity(index=0,indexOperation=0):
	'''quantity: Quantidade de moeda digital da operação.
		Tipo: String
	'''
	return result['response_data']['orders'][index]['operations'][indexOperation]['quantity']

def getOrdersOperationsPrice(index=0,indexOperation=0):
	'''price: Preço unitário da operação.
		Tipo: String
	'''
	return result['response_data']['orders'][index]['operations'][indexOperation]['price']

def getOrdersOperationsFeeRate(index=0,indexOperation=0):
	'''fee_rate: Comissão cobrada pelo serviço de intermediação. A comissão varia para ordens executadas e executoras.
		Tipo: String
	'''
	return result['response_data']['orders'][index]['operations'][indexOperation]['fee_rate']

def getOrdersOperationsExecutedTimestamp(index=0,indexOperation=0):
	'''executed_timestamp: Data e hora de execução da operação.
		Tipo: String
		Format: Era Unix
	'''
	return result['response_data']['orders'][index]['operations'][indexOperation]['executed_timestamp']


print(getOrdersOperationsExecutedTimestamp())
