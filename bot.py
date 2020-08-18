# -*- coding: utf-8 -*-
'''
Created on 13 de agosto de 2020

@author: Rodrigo Nunes

Version: v0.002

    Esse bot será baseado na observação do gráfico:
        Passo 1:Analisar o gráfico e observar qual os
                valores de mínimo e máximo de uma determinada faixa do gráfico.
        Passo 2:Definir um valor de compra da moeda
        Passo 3:Definir um stoploss para o valor de compra
        Passo 4:Definir um valor de venda da moeda
        Passo 5:Definir um valor de resistência para a faixa do gráfico.
                Se romper a resistência iniciar o procedimento de compra da moeda.
'''
import time
import os
import sys
import threading
import configparser
from get_account_info import GetAccountInfo
from list_orderbook import ListOrderBook
from place_sell_order import PlaceSellOrder
from place_buy_order import PlaceBuyOrder
from cancel_order import CancelOrder
from list_orders import ListOrders
from datetime import datetime
from trades import Trades

# Obtém a hora de inicio do bot e cria um arquivo out com base na data.
inicioBot = str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))

# Obtém as informações de configuração do bot
cfg = configparser.ConfigParser()


while True:        
        cfg.read('config')

        active = cfg.getint('conf', 'active')
        priceBuy = cfg.getfloat('conf','buy')
        priceSell = cfg.getfloat('conf','sell')
        stoploss = cfg.getfloat('conf','stoploss')
        res = cfg.getfloat('conf','resistence')
        stopmovel = cfg.getint('conf','stopmovel')
        coin = cfg.get('conf','coin')
        coinpair = cfg.get('conf','coinpair')

        # Obtendo o valor da última negociação
        td = Trades()
        currentPrice = float(td.getPrice())
        # Obtém informações da conta
        AccountInfo = GetAccountInfo(str(int(time.time())))
        saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
        qtdCoin = float(AccountInfo.getBalanceAvailable(coin)) 
        # se o preço atual estiver entre o stoploss e a resistência
        if currentPrice>stoploss and currentPrice<res and active==1:
                if qtdCoin>=0.1:
                        sellOrder = PlaceSellOrder(coinpair,qtdCoin,priceSell,str(int(time.time())))
                if saldoBRL>=10.0:
                        qtd=float("{0:9.8f}".format(saldoBRL/priceBuy))
                        buyOrder = PlaceBuyOrder(coinpair,qtd,priceBuy,str(int(time.time())))
        # se o preço atual estiver abaixo do stoploss
        if currentPrice<=stoploss and active==1:                        
                # Verificar se há ordens abertas e cancela
                time.sleep(1)
                # lista ordens de vendas abertas
                l = ListOrders(coinpair,str(int(time.time())),2,1)                        
                # enquanto tiver ordens abertas
                if int(l.getOrdersStatus()) == 2:
                        print("Ordens abertas com ID: "+str(l.getOrdersId())+"\n")
                        time.sleep(1)
                        cancelOrder = CancelOrder(coinpair,l.getOrdersId(),str(int(time.time())))
                        print("Ordem Cancelada.\n")                                
                # se a quantidade de moedas for maior do que o mínimo                                
                if qtdCoin>=0.1:
                        # criar as ordens de venda
                        time.sleep(1)
                        orderBook = ListOrderBook(coinpair,str(int(time.time())))
                        priceSell = float(orderBook.getOrderbookBidsLimitPrice(5))
                        sellOrder = PlaceSellOrder(coinpair,qtdCoin,priceSell,str(int(time.time())))
                # tornar o bot inativo
                replaceStringFile('active=1','active=0')
                                         
        # se o preço atual estiver acima da resistência
        if currentPrice>=res and active==1:
                stopPrice=float("{0:9.8f}".format(res*(1-(stopmovel/100))))
                if saldoBRL>=10.0:
                        orderBook = ListOrderBook(coinpair,str(int(time.time())))
                        price = float(orderBook.getOrderbookAsksLimitPrice(5))
                        # Calcula a quantidade a ser comprada
                        qtd=float("{0:9.8f}".format(saldoBRL/price))
                        buyOrder = PlaceBuyOrder(coinpair,qtd,price,str(int(time.time())))
                        stopPrice=float("{0:9.8f}".format(price*(1-(stopmovel/100))))
                
                tempPrice=stopPrice                        
                # enquanto o currentPrice>stopPrice
                while currentPrice>stopPrice:
                        tempPrice=float("{0:9.8f}".format(currentPrice*(1-(stopmovel/100))))
                        if tempPrice>stopPrice:
                                stopPrice=tempPrice
                        # aguarda 5 segundos para verificar o preço novamente
                        time.sleep(5)
                        # Obtendo o valor da última negociação
                        td = Trades()
                        currentPrice = float(td.getPrice())
                # após sair do loop executa a ordem de venda
                # Obtém informações da conta
                time.sleep(1)
                AccountInfo = GetAccountInfo(str(int(time.time())))
                qtdCoin = float(AccountInfo.getBalanceAvailable(coin))

                # criar a orden de venda
                time.sleep(1)
                orderBook = ListOrderBook(coinpair,str(int(time.time())))
                priceSell = float(orderBook.getOrderbookBidsLimitPrice(5))
                sellOrder = PlaceSellOrder(coinpair,qtdCoin,priceSell,str(int(time.time())))  

                # tornar o bot inativo
                replaceStringFile('active=1','active=0')

# altera o arquivo
def replaceStringFile(str1='',str2=''):
        file = open('config','r')
        string = file.read()
        file.close()        
        file = open('config','w')
        file.write(string.replace(str1,str2))
        file.close()