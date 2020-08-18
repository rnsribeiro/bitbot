# -*- coding: utf-8 -*-
'''
Created on 13 de agosto de 2020

@author: Rodrigo Nunes

Version: v0.002

    Esse bot será baseado na observação do gráfico:
        Todas esses valores devem ser verificados no arquivo config
        Passo 1:Analisar o gráfico e observar qual os
                valores de mínimo e máximo de uma determinada faixa do gráfico.
        Passo 2:Definir um valor de compra da moeda
        Passo 3:Definir um stoploss para o valor de compra
                3.1 Se o valor atual for menor ou igual ao stoploss executar
                uma ordem de venda imediatamente
        Passo 4:Definir um valor de venda da moeda
        Passo 5:Definir um valor de resistência para a faixa do gráfico.
                5.1 Se romper a resistência iniciar o procedimento de compra da moeda.
                5.2 Se conseguir comprar verificar frequentemente o valor atual e
                definir um valor de stop price movel
                        5.2.1 se o valor atual for menor ou igual ao stop price, executar
                        uma ordem de venda imediatamente.

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

# altera o arquivo config
def replaceStringFile(str1='',str2=''):
        file = open('config','r')
        string = file.read()
        file.close()        
        file = open('config','w')
        file.write(string.replace(str1,str2))
        file.close()

# Obtém a hora de inicio do bot e cria um nome de arquivo out com base na data e hora.
inicioBot = str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
file = "out-"+str(datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M%S'))

# Conta quantos ciclos de execução
ciclo=0 

# Obtém as informações de configuração do bot
cfg = configparser.ConfigParser()

while True:
        ciclo=ciclo+1

        f = open(file,'a')
        f.write("\n----------------------------------------------------------\n")
        f.write("################# CICLO: "+str(ciclo)+" ##################\n")
        f.write("######### Bot iniciado em: "+inicioBot+"\n")
        f.write("######### Hora Atual: "+str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))+"\n")
        f.write("######### Lendo o arquivo de configuração.\n")
        f.close()

        cfg.read('config')

        active = cfg.getint('conf', 'active')
        priceBuy = cfg.getfloat('conf','buy')
        priceSell = cfg.getfloat('conf','sell')
        stoploss = cfg.getfloat('conf','stoploss')
        res = cfg.getfloat('conf','resistence')
        stopmovel = cfg.getfloat('conf','stopmovel')
        coin = cfg.get('conf','coin')
        coinpair = cfg.get('conf','coinpair')

        f = open(file,'a')
        f.write("\tAtivo: "+str(active)+"\n")
        f.write("\tPreço de Compra: R$"+str(priceBuy)+"\n")
        f.write("\tPreço de Venda: R$"+str(priceSell)+"\n")
        f.write("\tStop Loss: R$"+str(stoploss)+"\n")
        f.write("\tResistência: R$"+str(res)+"\n")
        f.write("\tStop Movel: "+str(stopmovel)+"%\n")

        # Obtendo o valor da última negociação
        try:
                td = Trades()
                currentPrice = float(td.getPrice())
        except:
                f.write("############## ERRO ##############\n")
                f.write("\tErro ao tentar obter o preço atual.\n")
                f.write("\tNa linha 91 e 92 do arquivo.\n")
        f.write("\tPreço atual: R$"+str(currentPrice)+"\n")
        f.close()


        # Obtém informações da conta
        time.sleep(1)
        try:
                AccountInfo = GetAccountInfo(str(int(time.time())))
                saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
                qtdCoin = float(AccountInfo.getBalanceAvailable(coin))
        except:
                f = open(file,'a')
                f.write("############## ERRO ##############\n")
                f.write("\tErro ao tentar obter informações da conta.\n")
                f.write("\tNa linha 104-106 do arquivo.\n")
                f.close()


        f = open(file,'a')
        f.write("\n\tSaldo em Reais: R$"+str(saldoBRL)+"\n")
        f.write("\tSaldo em "+coin.upper()+": "+str(qtdCoin)+"\n")
        f.close()

        # se o preço atual estiver entre o stoploss e a resistência
        if currentPrice>stoploss and currentPrice<res and active==1:
                f = open(file,'a')
                f.write("\n################ EXECUÇÃO NORMAL #################\n")
                f.write("# O preço atual está entre o stoploss e a resistência.\n")
                f.write("\tResistência: R$"+str(res)+"\n")
                f.write("\tPreço de Venda: R$"+str(priceSell)+"\n")
                f.write("\tPreço atual: R$"+str(currentPrice)+"\n")
                f.write("\tPreço de Compra: R$"+str(priceBuy)+"\n")
                f.write("\tStop Loss: R$"+str(stoploss)+"\n")
                f.close()
                if qtdCoin>=0.1:
                        time.sleep(1)
                        f = open(file,'a')
                        try:
                                sellOrder = PlaceSellOrder(coinpair,qtdCoin,priceSell,str(int(time.time())))                        
                                f.write("\tOrdem de venda criada.\n")
                        except:
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar criar ordem de venda.\n")
                                f.write("\tNa linha 133 e 134 do arquivo.\n")
                        f.close()
                if saldoBRL>=10.0:
                        qtd=float("{0:9.8f}".format(saldoBRL/priceBuy))
                        time.sleep(1)
                        f = open(file,'a')
                        try:
                                buyOrder = PlaceBuyOrder(coinpair,qtd,priceBuy,str(int(time.time())))
                                f.write("\tOrdem de compra criada.\n")
                        except:
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar criar ordem de compra.\n")
                                f.write("\tNa linha 145 do arquivo.\n")                        
                        f.close()
                # Aguarda 10 segundos para verificar o preço novamente
                time.sleep(10)
        # se o preço atual estiver abaixo do stoploss
        if currentPrice<=stoploss and active==1:
                f = open(file,'a')
                f.write("\n##################### STOPLOSS ###################\n")
                f.write("##### O preço atual está abaixo do stoploss. #####\n")
                f.write("\tStop Loss: R$"+str(stoploss)+"\n")
                f.write("\tPreço atual: R$"+str(currentPrice)+"\n")
                f.write("\tVerificando se há ordens abertas.\n")
                f.close()

                # Verificar se há ordens abertas e cancela
                time.sleep(1)
                f = open(file,'a')
                try:
                        # lista ordens de vendas abertas
                        l = ListOrders(coinpair,str(int(time.time())),2)                        
                        # enquanto tiver ordens abertas
                        if int(l.getOrdersStatus()) == 2:
                                f.write("\tOrdens abertas com ID: "+str(l.getOrdersId())+"\n")
                                time.sleep(1)
                                try:
                                        cancelOrder = CancelOrder(coinpair,l.getOrdersId(),str(int(time.time())))
                                        f.write("\tOrdem Cancelada.\n")
                                except:
                                        f.write("############## ERRO ##############\n")
                                        f.write("\tErro ao tentar cancelar a ordem.\n")
                                        f.write("\tNa linha 175 do arquivo.\n") 
                except:
                        f.write("############## ERRO ##############\n")
                        f.write("\tErro ao tentar listar as ordens.\n")
                        f.write("\tNa linha 168-171 do arquivo.\n")
                f.close()
                # se a quantidade de moedas for maior do que o mínimo                                
                if qtdCoin>=0.1:
                        f = open(file,'a')
                        f.write("\tExecutando ordem de venda de emergência.\n")
                        f.close()
                        # criar as ordens de venda
                        time.sleep(1)
                        try:
                                orderBook = ListOrderBook(coinpair,str(int(time.time())))
                                priceSell = float(orderBook.getOrderbookBidsLimitPrice(5))
                        except:
                                f = open(file,'a')
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar obter o preço de venda do orderbook.\n")
                                f.write("\tNa linha 194-195 do arquivo.\n")
                                f.close()
                        time.sleep(1)
                        try:
                                f = open(file,'a')
                                sellOrder = PlaceSellOrder(coinpair,qtdCoin,priceSell,str(int(time.time())))                                
                                f.write("\tOrdem de venda executada.\n")
                                f.close()
                        except:
                                f = open(file,'a')
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar criar uma ordem de venda.\n")
                                f.write("\tNa linha 205 do arquivo.\n")
                                f.close()
                        
                # tornar o bot inativo
                f = open(file,'a')
                f.write("\tDesativando o bot\n")
                replaceStringFile('active=1','active=0')
                f.write("\tBot inativo e aguardando novas ordens.\n")
                f.close()
                                         
        # se o preço atual estiver acima da resistência
        if currentPrice>=res and active==1:
                f = open(file,'a')
                f.write("\n################## RESISTÊNCIA ###################\n")
                f.write("##### Preço atual está acima da resistência. #####\n")
                f.write("\tPreço atual: R$"+str(currentPrice)+"\n")
                stopPrice=float("{0:9.8f}".format(res*(1-(stopmovel/100))))
                f.write("\tStop Price: R$"+str(stopPrice)+"\n")
                f.close()

                if saldoBRL>=10.0:
                        time.sleep(1)
                        try:
                                orderBook = ListOrderBook(coinpair,str(int(time.time())))
                                price = float(orderBook.getOrderbookAsksLimitPrice(5))
                                 # Calcula a quantidade a ser comprada
                                qtd=float("{0:9.8f}".format(saldoBRL/price))
                        except:
                                f = open(file,'a')
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar listar as ordens do orderbook.\n")
                                f.write("\tNa linha 237 e 238 do arquivo.\n")
                                f.close()
                       
                        f = open(file,'a')
                        time.sleep(1)
                        try:
                                buyOrder = PlaceBuyOrder(coinpair,qtd,price,str(int(time.time())))
                                f.write("\tExecutando ordem de compra.\n")
                        except:
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar criar uma ordem de compra.\n")
                                f.write("\tNa linha 251 do arquivo.\n")
                        f.close()

                tempPrice=stopPrice                        
                # enquanto o currentPrice>stopPrice
                while currentPrice>stopPrice:
                        tempPrice=float("{0:9.8f}".format(currentPrice*(1-(stopmovel/100))))
                        if tempPrice>stopPrice:
                                stopPrice=tempPrice
                        # aguarda 5 segundos para verificar o preço novamente
                        time.sleep(5)
                        f = open(file,'a')
                        try:
                                # Obtendo o valor da última negociação
                                td = Trades()
                                currentPrice = float(td.getPrice())
                        except:
                                f.write("############## ERRO ##############\n")
                                f.write("\tErro ao tentar obter o valor do preço atual.\n")
                                f.write("\tNa linha 269 e 270 do arquivo.\n")
                        
                        f.write("\n################## RESISTÊNCIA ###################\n")
                        f.write("###### Preço atual está acima do Stop Price. #####\n")
                        f.write("\tPreço atual: R$"+str(currentPrice)+"\n")
                        f.write("\tStop Price: R$"+str(stopPrice)+"\n")
                        f.close()
                # após sair do loop executa a ordem de venda
                f = open(file,'a')
                f.write("\n############## EXECUTANDO STOP PRICE #############\n")
                f.write("#### O preço atual está abaixo do stop price. ####\n")
                f.write("\tStop Price: R$"+str(stopPrice)+"\n")
                f.write("\tPreço atual: R$"+str(currentPrice)+"\n")
                
                # Obtém informações da conta
                f.write("\tObtendo informações da conta.\n")
                f.close()
                time.sleep(1)
                f = open(file,'a')
                try:
                        AccountInfo = GetAccountInfo(str(int(time.time())))
                        qtdCoin = float(AccountInfo.getBalanceAvailable(coin))
                        f.write("\tQuantidade de "+coin.upper()+": "+str(qtdCoin)+"\n")
                except:
                        f.write("############## ERRO ##############\n")
                        f.write("\tErro ao tentar obter informações da conta.\n")
                        f.write("\tNa linha 294 e 295 do arquivo.\n")                
                f.close()

                # criar a orden de venda
                time.sleep(1)
                f = open(file,'a')
                try:
                        orderBook = ListOrderBook(coinpair,str(int(time.time())))                
                        priceSell = float(orderBook.getOrderbookBidsLimitPrice(5))
                        f.write("\tPreço a ser vendido: R$"+str(priceSell)+"\n")
                except:
                        f.write("############## ERRO ##############\n")
                        f.write("\tErro ao tentar obter o preço de venda do orderbook.\n")
                        f.write("\tNa linha 307-309 do arquivo.\n")

                time.sleep(1)
                try:
                        f.write("\tExecutando ordem de venda.\n")
                        sellOrder = PlaceSellOrder(coinpair,qtdCoin,priceSell,str(int(time.time())))
                except:
                        f.write("############## ERRO ##############\n")
                        f.write("\tErro ao tentar executar uma ordem de venda.\n")
                        f.write("\tNa linha 320 do arquivo.\n")
                f.close()


                # tornar o bot inativo
                f = open(file,'a')
                f.write("\tDesativando o Bot.\n")
                replaceStringFile('active=1','active=0')
                f.write("\tAguardando novas ordens.\n")
                f.close()
        if active==0:
                time.sleep(1)
                f = open(file,'a')
                try:
                        # lista ordens de vendas abertas
                        l = ListOrders(coinpair,str(int(time.time())),2)                        
                        # enquanto tiver ordens abertas
                        if int(l.getOrdersStatus()) == 2:
                                f.write("\tOrdens abertas com ID: "+str(l.getOrdersId())+"\n")
                                time.sleep(1)
                                try:
                                        cancelOrder = CancelOrder(coinpair,l.getOrdersId(),str(int(time.time())))
                                        f.write("\tOrdem Cancelada.\n")
                                except:
                                        f.write("############## ERRO ##############\n")
                                        f.write("\tErro ao tentar cancelar a ordem.\n")
                                        f.write("\tNa linha 342 do arquivo.\n") 
                except:
                        f.write("\n############### AVISO ###############\n")
                        f.write("\tNão há ordens abertas.\n")

                f.write("\n############### BOT DESATIVADO ###############\n")
                f.write("\tAguardando novas ordens.\n")
                f.write("##############################################\n")
                f.close()
                time.sleep(10)