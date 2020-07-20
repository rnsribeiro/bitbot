import hashlib
import hmac
import sys
from urllib.parse import urlencode

# Parâmetros passado por linha de comando
tapi_method=sys.argv[1]
coin_pair=sys.argv[2]
tapi_nonce = sys.argv[3]
MB_TAPI_SECRET = sys.argv[4]

# constantes
REQUEST_PATH = '/tapi/v3/'

# Parâmetros
params = {
	'tapi_method':tapi_method,
	'tapi_nonce':tapi_nonce,
	'coin_pair':coin_pair
}

# coloca os argumentos em formato url
params = urlencode(params)

# Gerar MAC
params_string = REQUEST_PATH + '?' + params
H = hmac.new(bytes(MB_TAPI_SECRET, encoding='utf-8'), digestmod=hashlib.sha512)
H.update(params_string.encode('utf-8'))
tapi_mac = H.hexdigest()

# Exibe a saida para o sistema
print(tapi_mac)
