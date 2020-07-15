require("socket")
require("json")
https = require("ssl.https")

--[[ 
	Métodos da API
	ticker: Retorna informações com o resumo das últimas 24 horas de negociações.
		high: Maior preço unitário de negociação das últimas 24 horas.
		Tipo: Decimal

		low: Menor preço unitáio de negociação das últimas 24 horas.
		Tipo: Decimal

		vol: Quantidade negociada nas últimas 24 horas.
		Tipo: Decimal

		last: Preço unitário da última negociação.
		Tipo: Decimal

		buy: Maior preço de oferta de compra das últimas 24 horas.
		Tipo: Decimal

		sell: Menor preço de oferta de venda das últimas 24 horas.
		Tipo: Decimal

		date: Data e hora da informação em Era Unix
		Tipo: Inteiro
--]]

-- Requisição do ticker
local body,code,headers,status = https.request("https://www.mercadobitcoin.net/api/BTC/ticker/")

-- Tabela para receber os valores do body
local table = {}

-- Verifica se houve erro na requisição
local error = nil

-- Verifica se a requisição foi um sucesso, se sim, converte a string body em tabela
if string.match(tostring(status),"OK") then
	table = json.decode.decode(body)
else
	error = 1
end

-- Cria uma tabela para gerenciar as funções
local ticker = {}

-- Retorna o maio preço unitário de negociação das últimas 24 horas.
function ticker.high()
	if error then return nil else return table.ticker.high end
end

-- Retorna o menor preço unitário de negociação das últimas 24 horas.
function ticker.low()
	if error then return nil else return table.ticker.low end
end

-- Retorna a quantidade negociada nas últimas 24 horas.
function ticker.vol()
	if error then return nil else return table.ticker.vol end
end

-- Retorna o preço unitário da última negociação.
function ticker.last()
	if error then return nil else return table.ticker.last end
end

-- Retorna o maior preço de oferta de compra das últimas 24 horas.
function ticker.buy()
	if error then return nil else return table.ticker.buy end
end

-- Retorna o menor preço de oferta de venda das últimas 24 horas.
function ticker.sell()
	if error then return nil else return table.ticker.sell end
end

-- Retorna a data e hora da informação em Era Unix
function ticker.date()
	if error then return nil else return table.ticker.date end
end

-- Retorna o objeto tabela para a função chamadora.
return ticker
