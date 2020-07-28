# -*- coding: utf-8 -*-
'''
Created on 10 de julho de 2020

@author: Rodrigo Nunes
@author: Arnaldo Nunes

Version: v0.001

    Esse bot será baseado no valor do spreed:
        Passo 1:Obter o valor de compra com base no valor de venda do orderbook
        Passo 2:Realizar a compra com base no valor de venda - spreed definido pelo usuário
        Passo 3:Ápos realizar a compra definir o percentual de ganho e fixar o valor de venda        
        Passo 4:Após realizar a venda
        Passo 5:voltar ao passo 1
'''
import time
import os
import sys
import threading
from get_account_info import GetAccountInfo
from list_orderbook import ListOrderBook
from place_sell_order import PlaceSellOrder
from place_buy_order import PlaceBuyOrder
from cancel_order import CancelOrder
from list_orders import ListOrders
from datetime import datetime

# Obtém a hora de inicio do bot e cria um arquivo out com base na data.
inicioBot = str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
file = "out-"+str(datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))

# Moeda a ser usada no script futuramente pode ser passado por
# parâmetro na linha de comando.
moeda='BRLXRP'

# Obtém a percentagem do spreed passado por parâmetro na linha de comando.
# Em caso de erro exibe a mensagem e encerra o script.
try:
    spreed=float(sys.argv[1])
except:
    print("É necessário passar um argumento spreed como parâmetro ex: 0.006")
    exit()

# Contador para ordens do inicio do bot
ordensDia=0

# Obtém o menor preço de venda do orderbook
def menorVenda(coin_pair):
    orderBook = ListOrderBook(coin_pair,str(int(time.time())))
    priceSell = float(orderBook.getOrderbookAsksLimitPrice())
    return priceSell

# Realiza uma ordem de compra com base no saldo
# e retorn o order_id da operação.
def buy(coin_pair,saldo):    
    time.sleep(1)
    # Obtém informações do orderbook com base no coin_pair
    orderBook = ListOrderBook(coin_pair,str(int(time.time())))

    # Abre o arquivo e insere as informações nele
    f = open(file,'a')
    print("############ ORDEN DE COMPRA ############\n")
    print("Saldo de Reais: R$"+str(saldo)+"\n")
    f.close()

    # Menor preço de vendo do orderbook
    priceSell = menorVenda(moeda)

    # Preço de compra sugerido
    priceBuy=float("{0:9.5f}".format(priceSell*(1.0-spreed)))            
    
    f = open(file,'a')
    print("Preço de compra: "+str(priceBuy)+"\n")
    f.close()

    # Calcula a quantidade a ser comprada
    quantidade=float("{0:9.8f}".format(saldo/priceBuy))
    f = open(file,'a')
    print("Quantidade da moeda a ser comprada: "+str(quantidade)+"\n")
    f.close()

    # Executa a ordem de compra
    time.sleep(1)  
    buyOrder = PlaceBuyOrder(coin_pair,quantidade,priceBuy,str(int(time.time())))
    buyOrder_id = int(buyOrder.getOrderId())

    return buyOrder_id

# Cancela uma ordem
def cancelOrder(coin_pair, order_id):
    cancelBuyOrder = CancelOrder(coin_pair,order_id,str(int(time.time())))


# Realiza uma orderm de venda com base na moeda o saldo e o último preço
# de compra da moeda
def sell(coin_pair,saldo,lastBuy):
    
    # Insere informações no arquivo out
    f = open(file,'a')
    print("############ ORDEN DE VENDA ############\n")
    f.close()    
    
    # Calcula o preço de venda
    priceSell = float(float(lastBuy)*(1.0+spreed))

    # Exibe no arquivo out o preço de venda e o preço da ultima compra.
    f = open(file,'a')
    print("Preço de venda: "+"{0:9.8f}".format(priceSell)+"\n")
    print("Preço da última compra: R$"+str(lastBuy)+"\n")
    f.close()

    # Calcula o valor em Reais com base no preço de venda e o saldo da moeda.
    reais = float("{0:9.8f}".format((priceSell*saldo)*0.997))

    # Exibe as informações no arquivo out
    # Mostrando o valor em Reais já com a taxa descontada
    f = open(file,'a')
    print("Valor em Reais calculado descontando a taxa: R$"+str(reais)+"\n")
    f.close()

    # Formata o preço de venda para 5 casas decimais
    priceSell = float("{0:9.5f}".format(priceSell))
    
    # Realiza a ordem de venda com base nas informações inseridas e calculadas
    time.sleep(1)
    sellOrder = PlaceSellOrder(coin_pair,saldo,priceSell,str(int(time.time())))
    sellOrder_id = sellOrder.getOrderId()
    
    # Retorna o ID da ordem de venda
    return sellOrder_id 

while True:
    try:
        # Cabeçalho
        f = open(file,'a')
        print("\nBot Iniciado: "+inicioBot+"\n")
        print("Ordens criadas no dia: "+str(ordensDia)+"\n")
        print("Operação Iniciada: "+str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))+"\n")
        f.close()
    
        # Contador para ordens criadas no dia
        ordensDia=ordensDia+1
    
        # Exibe o cabeçalho no arquivo out
        f = open(file, 'a')
        print("Obtendo o valor da última Compra ...\n")
        time.sleep(1)
        l = ListOrders(moeda,str(int(time.time())),4,1)
        ultimaCompra = l.getOrdersLimitPrice()
        print("Valor da última Compra: R$"+str(ultimaCompra)+"\n")
        f.close()
        time.sleep(1)

        AccountInfo = GetAccountInfo(str(int(time.time())))
        saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
        qtdCoin = float(AccountInfo.getBalanceAvailable('xrp'))  

        # Exibe o saldo das moedas
        f = open(file,'a')
        print("Saldo em Reais: R$"+str(saldoBRL)+"\n")
        print("Saldo em Coin: R$"+str(qtdCoin)+"\n")
        f.close()

        if qtdCoin>=0.1:
            # Executa uma ordem de venda, obtém o ID e aguarda 20 segundos
            f = open(file,'a')
            print("\n\nIniciando ordem de venda...\n")        
            sell_id = sell(moeda,qtdCoin,ultimaCompra)
            print("Ordem de venda criada com id: "+str(sell_id)+"\n")
            f.close()
            f = open(file,'a')
            print("Aguardando 1 minuto...\n")
            f.close()
            time.sleep(60)
        
            # Cancela a ordem
            cancelOrder(moeda,sell_id)
            f = open(file,'a')
            print("Ordem de venda cancelada:\n")
            f.close()
    
        elif saldoBRL>=10.0:    
            # Executa uma ordem de compra, obtém o ID e aguarda 20 segundos
            f = open(file,'a')
            print("\n\nIniciando ordem de compra...\n")
            buy_id = buy(moeda,saldoBRL)
            print("Ordem de compra criada com id: "+str(buy_id)+"\n")
            f.close()
            f = open(file,'a')
            print("Aguardando 20 segundos...\n")
            f.close()
            time.sleep(20)
    
            # Cancela a ordem
            cancelOrder(moeda,buy_id)
            f = open(file,'a')
            print("Ordem de compra cancelada:\n")
            f.close()
        else:
            # Verifica se há ordens abertas
            f = open(file,'a')
            print("\nVerificando se há ordens abertas...\n")
            f.close()
            try:
                time.sleep(1)
                l = ListOrders(moeda,str(int(time.time())),2)
                if int(l.getOrdersStatus()) == 2:
                    f = open(file,'a')
                    print("Há ordens abertas com ID: "+str(l.getOrdersId())+"\n")
                    f.close()
                    time.sleep(1)
                    cancelOrder(moeda,l.getOrdersId())
                    f = open(file,'a')
                    print("Ordem Cancelada.\n")
                    f.close()
            except:
                f = open(file,'a')
                print("Não há ordens abertas.\n")
                f.close()
            f=open(file,'a')
            print("Tentando Novamente.\n\n")
            f.close()

    except :        
        f = open(file,'a')
        print("\nOcorreu algum erro!!!\n")
        print("Tentando novamente em 3 segundos!...\n")
        f.close()
        time.sleep(3)
