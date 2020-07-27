# -*- coding: utf-8 -*-
'''
    Passos para operação do bot
        Passo 1:Obter o saldo na conta em Reais
        Passo 2:Obter o maior preço de compra da moeda
        Passo 3:Somar 0.0001 ao maior valor de compra
        Passo 4:Realizar uma ordem de compra
        Passo 5:Embutir o percentual da taxa de compra e venda + o 
        Passo 6:    percentual de ganho e estabelecer o preço de venda
        Passo 7:Realizar uma ordem de venda
        Passo 8:voltar ao passo 1
'''
import time
import os
from get_account_info import GetAccountInfo
from list_orderbook import ListOrderBook
from place_sell_order import PlaceSellOrder
from place_buy_order import PlaceBuyOrder
from cancel_order import CancelOrder
from list_orders import ListOrders
from datetime import datetime

inicioBot = str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))

os.system("rm -f out")

file = open('out', 'a')
file.write("Obtendo o valor da última Compra ...\n")
l = ListOrders('BRLXRP',str(int(time.time())),4,1)
ultimaCompra = l.getOrdersLimitPrice()
file.write("Valor da última Compra: R$"+str(ultimaCompra)+"\n")
file.close()

ordensDia=0

cont=0
#time.sleep(1)
#listOrders = ListOrders("BRLXRP",str(int(time.time())))



while True:
    try:
        #os.system("clear")
        # Cabeçalho e alteração de cor para amarelo
        file = open('out','a')
        file.write("\nBot Iniciado: "+inicioBot+"\n")
        file.write("Ordens criadas no dia: "+str(ordensDia)+"\n")
        file.write("Operação Iniciada: "+str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))+"\n")
        file.close()

        ordensDia=ordensDia+1

        time.sleep(1)
        #try:
        AccountInfo = GetAccountInfo(str(int(time.time())))
        saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
        quantidadeXRP = float(AccountInfo.getBalanceAvailable('xrp'))    

        if saldoBRL>=10.0:
            time.sleep(1)
            orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
            file = open('out','a')
            file.write("\n############ ORDEN DE COMPRA ############\n")
            file.write("Valor da última Compra: R$"+str(ultimaCompra)+"\n")   
            file.write("Saldo de Reais: R$"+str(saldoBRL)+"\n")
            file.close()
            maiorCompra = float(orderBook.getOrderbookBidsLimitPrice())
            file = open('out','a')
            file.write("Maior preço de compra do orderbook: "+str(maiorCompra)+"\n")
            file.close()
            compraSugerida=float("{0:9.5f}".format(maiorCompra+0.00001))            
            #compraSugerida=1.12001
            file = open('out','a')
            file.write("Preço de compra sugerido: "+str(compraSugerida)+"\n")
            file.close()
            quantidadeXRP=float("{0:9.8f}".format(saldoBRL/compraSugerida))
            file = open('out','a')
            file.write("Quantidade de XRP calculado sem taxa: "+str(quantidadeXRP)+"\n")
            file.close()
            time.sleep(1)  
            buyOrder = PlaceBuyOrder('BRLXRP',quantidadeXRP,compraSugerida,str(int(time.time())))
            buyOrder_id = int(buyOrder.getOrderId())
            file = open('out','a')
            file.write("Ordem de compra criado: "+str(buyOrder_id)+"\n")
            file.write("Aguardando 60 segundos .\n")
            file.close()
            time.sleep(20)
            file = open('out','a')
            file.write("Aguardando 40 segundos ..\n")
            file.close()
            time.sleep(20)
            file = open('out','a')
            file.write("Aguardando 20 segundos ...\n")
            file.close()
            time.sleep(20)
            ultimaCompra=compraSugerida
            cancelBuyOrder = CancelOrder("BRLXRP",buyOrder_id,str(int(time.time())))
            file = open('out','a')
            file.write("Ordem de compra cancelada:\n")
            file.close()

        elif quantidadeXRP>=0.1:
            time.sleep(1)
            orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
            file = open('out','a')
            file.write("\n############ ORDEN DE VENDA ############\n")
            file.close()
            menorVenda = float(orderBook.getOrderbookAsksLimitPrice())
            file = open('out','a')
            file.write("Menor preço de venda do orderbook: "+str(menorVenda)+"\n")
            file.close()
            vendaSugerida = float(float(ultimaCompra)*1.01)
            cont=0
            while cont<20:
                menorVenda = float(orderBook.getOrderbookAsksLimitPrice(cont))
                file = open('out','a')
                file.write("Menor venda com indice: {0} R${1:9.5f}".format(cont,menorVenda)+"\n")
                file.close()
                if vendaSugerida<menorVenda:
                    vendaSugerida=menorVenda-0.00001
                    break
                cont=cont+1
            file = open('out','a')
            file.write("Preço de venda sugerido: "+"{0:9.8f}".format(vendaSugerida)+"\n")
            file.write("Ultimo preço de compra: R$"+str(ultimaCompra)+"\n")
            file.close()
            reais = float("{0:9.8f}".format(vendaSugerida*quantidadeXRP))
            file = open('out','a')
            file.write("Valor em Reais calculado sem taxa: R$"+str(reais)+"\n")
            file.close()
            vendaSugerida = float("{0:9.5f}".format(vendaSugerida))
            #vendaSugerida = 1.12
            time.sleep(1)
            sellOrder = PlaceSellOrder("BRLXRP",quantidadeXRP,vendaSugerida,str(int(time.time())))
            sellOrder_id = sellOrder.getOrderId()
            file = open('out','a')
            file.write("Ordem de venda criada: "+str(sellOrder_id)+"\n")
            file.write("Aguardando 60 segundos .\n")
            file.close()
            time.sleep(20)
            file = open('out','a')
            file.write("Aguardando 40 segundos ..\n")
            file.close()
            time.sleep(20)
            file = open('out','a')
            file.write("Aguardando 20 segundos ...\n")
            file.close()
            time.sleep(20)
            cancelar = CancelOrder("BRLXRP",sellOrder_id,str(int(time.time())))
            file = open('out','a')
            file.write("Ordem de venda cancelada:"+sellOrder_id+"\n\n")
            file.close()            
        else:
            file = open('out','a')
            file.write("\nVerificando se há ordens abertas...\n")
            file.close()
            l = ListOrders('BRLXRP',str(int(time.time())),2)
            if int(l.getOrdersStatus()) == 2:
                file = open('out','a')
                file.write("Há ordens abertas com ID: "+str(l.getOrdersId())+"\n")
                file.close()
                time.sleep(1)
                cancelar = CancelOrder("BRLXRP",l.getOrdersId(),str(int(time.time())))
                file = open('out','a')
                file.write("Ordem Cancelada.\nTentando Novamente.\n\n")
                file.close()                


    except :        
        file = open('out','a')
        file.write("\nOcorreu algum erro!!!\n")
        file.write("Tentando novamente em 5 segundos!...\n")
        file.close()
        time.sleep(5)

