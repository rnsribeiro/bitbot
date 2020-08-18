'''
Created on 10 de julho de 2020

@author: Rodrigo Nunes
@author: Arnaldo Nunes

	Descrição
	Retorna informações do livro de negociações
	(orderbook) do Mercado Bitcoin para o par de moedas (coin_pair)
	informado.  Dentre elas, o
	número da última ordem contemplada (latest_order_id) e número
	das ordens do livro (order_id), descritos abaixo. Importante
	salientar que nesse método ordens de mesmo preço não são
	agrupadas como feito no método público.
'''

from list_orderbook import ListOrderBook

