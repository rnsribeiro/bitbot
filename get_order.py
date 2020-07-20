'''
	Descrição:
	Retorna os dados da ordem de acordo com o ID informado.
	Dentre os dados estão as informações das Operações executadas dessa ordem.
	Apenas ordens que pertencem ao proprietário da chave da TAPI pode ser consultadas.
	Erros específicos são retornados para os casos onde o order_id informado
	não seja de uma ordem válida ou pertença a outro usuário.
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
order_id = '8155792'

# Nonce
# Para obter variação de forma simples
# timestamp pode ser utilizado:
tapi_nonce = str(int(time.time()))

# Parâmetros
params = {
    'tapi_method': 'get_order',
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
	
	#print(json.dumps(result, indent=4))

finally:
    if conn:
        conn.close()


def getId():
	'''
	order_id: Número de identificação da ordem, único por coin_pair.
	Tipo: Inteiro
	'''
	return result['response_data']['order']['order_id']

def getCoinPair():
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
	return result['response_data']['order']['coin_pair']

def getType():
	'''
	order_type: Tipo da ordem a ser filtrado.
	Tipo: Inteiro
	Domínio de dados:
	1 : Ordem de compra
	2 : Ordem de venda
	'''
	return result['response_data']['order']['order_type']

def getStatus():
	'''
	status: Estado da ordem.
	Tipo: Inteiro
	Domínio de dados:
	2 : open : Ordem aberta, disponível no livro de negociações. Estado intermediário.
	3 : canceled : Ordem cancelada, executada parcialmente ou sem execuções. Estado final.
	4 : filled : Ordem concluída, executada em sua totalidade. Estado final.
	'''
	return result['response_data']['order']['status']

def getHasFills():
	'''
	has_fills: Indica se a ordem tem uma ou mais execuções. Auxilia na identificação de ordens parcilamente executadas.
	Tipo: Booleano
	false : Sem execuções.
	true : Com uma ou mais execuções.
	'''
	return result['response_data']['order']['has_fills']

def getQuantity():
	'''
	quantity: Quantidade da moeda digital a comprar/vender ao preço de limit_price.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['order']['quantity']

def getLimitPrice():
	'''
	limit_price: Preço unitário máximo de compra ou mínimo de venda.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['order']['limit_price']

def getExecutedQuantity():
	'''
	limit_price: Preço unitário máximo de compra ou mínimo de venda.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['order']['executed_quantity']

def getExecutedPriceAvg():
	'''
	executed_price_avg: Preço unitário médio de execução.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['order']['executed_price_avg']

def getFee():
	'''
	fee: Comissão da ordem, para ordens de compra os valores são em moeda digital, para ordens de venda os valores são em Reais.
	Tipo: String
	Formato: Ponto como separador decimal, sem separador de milhar
	'''
	return result['response_data']['order']['fee']

def getCreatedTimestamp():
	'''
	created_timestamp: Data e hora de criação da ordem.
	Tipo: String
	Formato: Era Unix
	'''
	return result['response_data']['order']['created_timestamp']

def getUpdatedTimestamp():
	'''
	updated_timestamp: Data e hora da última atualização da ordem. Não é alterado caso a ordem esteja em um estado final (ver status).
	Tipo: String
	Format: Era Unix
	'''
	return result['response_data']['order']['updated_timestamp']

def getOrdersOperationsId(indexOperation=0):
	'''
	operation_id: Número de identificação da operação, único por coin_pair
	Tipo: Inteiro
	'''
	return result['response_data']['order']['operations'][indexOperation]['operation_id']

def getOperationsQuantity(indexOperation=0):
	'''
	quantity: Quantidade de moeda digital da operação.
	Tipo: String
	'''
	return result['response_data']['order']['operations'][indexOperation]['quantity']

def getOperationsPrice(indexOperation=0):
	'''
	price: Preço unitário da operação.
	Tipo: String
	'''
	return result['response_data']['order']['operations'][indexOperation]['price']

def getOperationsFeeRate(indexOperation=0):
	'''
	fee_rate: Comissão cobrada pelo serviço de intermediação. A comissão varia para ordens executadas e executoras.
	Tipo: String
	'''
	return result['response_data']['order']['operations'][indexOperation]['fee_rate']

def getOperationsExecutedTimestamp(indexOperation=0):
	'''
	executed_timestamp: Data e hora de execução da operação.
	Tipo: String
	Format: Era Unix
	'''
	return result['response_data']['order']['operations'][indexOperation]['executed_timestamp']

# Para testar a função
print(getId())
print(getCoinPair())
print(getType())
print(getStatus())
print(getHasFills())
print(getQuantity())
print(getLimitPrice())
print(getExecutedQuantity())
print(getExecutedPriceAvg())
print(getFee())
print(getCreatedTimestamp())
print(getUpdatedTimestamp())
print(getOrdersOperationsId())
print(getOperationsQuantity())
print(getOperationsPrice())
print(getOperationsFeeRate())
print(getOperationsExecutedTimestamp())

