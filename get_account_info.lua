user = require ("userinfo")

-- Nome do método que irá acessar na TAPI
metodo = "get_account_info"

-- Criar tonce
tonce = tostring(os.time(os.date("!*t")))

-- Parametros
params {
	'method': metodo,
	'tonce' : tonce
}
