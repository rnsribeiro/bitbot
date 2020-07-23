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
coin_pair =''   #'BRLXRP'
quantity = 0   #0.1
limit_price = 0.0 #1.0601 # Preço em Reais R$

# Para obter variação de forma simples
# timestamp pode ser utilizado:
tapi_nonce = str(int(time.time()))


def placeSellOrder(coin_pair,quantity,limit_price):
    coin_pair=coin_pair
    quantity=quantity
    limit_price=limit_price

#placeSellOrder(coin_pair,quantity,limit_price)

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

def getOrderType():
    '''
    order_type: Tipo da ordem a ser filtrado.
    Tipo: Inteiro
    Domínio de dados:
    1 : Ordem de compra
    2 : Ordem de venda
    '''
    return 	result['response_data']['order']['order_type']

def getOrderStatus():
    '''
    status: Estado da ordem.
    Tipo: Inteiro
    Domínio de dados:
    2 : open : Ordem aberta, disponível no livro de negociações. Estado intermediário.
    3 : canceled : Ordem cancelada, executada parcialmente ou sem execuções. Estado final.
    4 : filled : Ordem concluída, executada em sua totalidade. Estado final.
    '''
    return 	result['response_data']['order']['status']

def getOrderHasFills():
    '''
    has_fills: Indica se a ordem tem uma ou mais execuções. Auxilia na identificação de ordens parcilamente executadas.
    Tipo: Booleano
    false : Sem execuções.
    true : Com uma ou mais execuções.
    '''
    return 	result['response_data']['order']['has_fills']

def getOrderQuantity():
    '''
    quantity: Quantidade da moeda digital a comprar/vender ao preço de limit_price.
    Tipo: String
    Formato: Ponto como separador decimal, sem separador de milhar
    '''
    return 	result['response_data']['order']['quantity']

def getOrderLimitPrice():
    '''
    limit_price: Preço unitário máximo de compra ou mínimo de venda.
    Tipo: String
    Formato: Ponto como separador decimal, sem separador de milhar
    '''
    return 	result['response_data']['order']['limit_price']

def getOrderExecutedQuantity():
    '''
    executed_quantity: Quantidade da moeda digital executada.
    Tipo: String
    Formato: Ponto como separador decimal, sem separador de milhar
    '''
    return 	result['response_data']['order']['executed_quantity']

def getOrderExecutedPriceAvg():
    '''
    executed_price_avg: Preço unitário médio de execução.
    Tipo: String
    Formato: Ponto como separador decimal, sem separador de milhar
    '''
    return 	result['response_data']['order']['executed_price_avg']

def getOrderFee():
    '''
    fee: Comissão da ordem, para ordens de compra os valores são em moeda digital, para ordens de venda os valores são em Reais.
    Tipo: String
    Formato: Ponto como separador decimal, sem separad
    '''
    return 	result['response_data']['order']['fee']

def getOrderCreatedTimestamp():
    '''
    created_timestamp: Data e hora de criação da ordem.
    Tipo: String
    Format: Era Unix 
    '''
    return 	result['response_data']['order']['created_timestamp']

def getOrderUpdatedTimestamp():
    '''
    updated_timestamp: Data e hora da última atualização da ordem. Não é alterado caso a ordem esteja em um estado final (ver status).
    Tipo: String
    Format: Era Unix 
    '''
    return 	result['response_data']['order']['updated_timestamp']

def getOrderOperationsId(index=0):
    '''
    operations: Lista de operações ou execuções realizadas por essa ordem.
     operation_id: Número de identificação da operação, único por coin_pair
    Tipo: Inteiro
    '''
    return result['response_data']['order']['operations'][index]['operation_id']

def getOrderOperationsQuantity(index=0):
    '''
    quantity: Quantidade de moeda digital da operação.
    Tipo: String
    '''
    return result['response_data']['order']['operations'][index]['quantity']

def getOrderOperationsPrice(index=0):
    '''
    price: Preço unitário da operação.
    Tipo: String
    '''
    return result['response_data']['order']['operations'][index]['price']

def getOrderOperationsFeeRate(index=0):
    '''
    fee_rate: Comissão cobrada pelo serviço de intermediação. A comissão varia para ordens executadas e executoras.
    Tipo: String
    '''
    return 	result['response_data']['order']['operations'][index]['fee_rate']

def getOrderOperationsExecutedTimestamp(index=0):
    '''
    executed_timestamp: Data e hora de execução da operação.
    Tipo: String
    Format: Era Unix
    '''
    return 	result['response_data']['order']['operations'][index]['executed_timestampe']

print(getOrderId())
print(getOrderCoinPair())
print(getOrderType())
print(getOrderStatus())
print(getOrderHasFills())
print(getOrderQuantity())
print(getOrderLimitPrice())
print(getOrderExecutedQuantity())
print(getOrderExecutedPriceAvg())
print(getOrderFee())
print(getOrderCreatedTimestamp())
print(getOrderUpdatedTimestamp())
#print(getOrderOperationsId())
#print(getOrderOperationsQuantity())
#print(getOrderOperationsPrice())
#print(getOrderOperationsFeeRate())
#print(getOrderOperationsExecutedTimestamp())
