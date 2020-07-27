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
file = "out-"+str(datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S'))

#os.system("rm -f out")

f = open(file, 'a')
f.write("Obtendo o valor da última Compra ...\n")
l = ListOrders('BRLXRP',str(int(time.time())),4,1)
ultimaCompra = l.getOrdersLimitPrice()
f.write("Valor da última Compra: R$"+str(ultimaCompra)+"\n")
f.close()

ordensDia=0

cont=0
#time.sleep(1)
#listOrders = ListOrders("BRLXRP",str(int(time.time())))



while True:
    try:
        #os.system("clear")
        # Cabeçalho e alteração de cor para amarelo
        f = open(file,'a')
        f.write("\nBot Iniciado: "+inicioBot+"\n")
        f.write("Ordens criadas no dia: "+str(ordensDia)+"\n")
        f.write("Operação Iniciada: "+str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))+"\n")
        f.close()

        ordensDia=ordensDia+1

        time.sleep(1)
        #try:
        AccountInfo = GetAccountInfo(str(int(time.time())))
        saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
        quantidadeXRP = float(AccountInfo.getBalanceAvailable('xrp'))    

        if saldoBRL>=10.0:
            time.sleep(1)
            orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
            f = open(file,'a')
            f.write("\n############ ORDEN DE COMPRA ############\n")
            f.write("Valor da última Compra: R$"+str(ultimaCompra)+"\n")   
            f.write("Saldo de Reais: R$"+str(saldoBRL)+"\n")
            f.close()
            maiorCompra = float(orderBook.getOrderbookBidsLimitPrice())
            f = open(file,'a')
            f.write("Maior preço de compra do orderbook: "+str(maiorCompra)+"\n")
            f.close()
            compraSugerida=float("{0:9.5f}".format(maiorCompra+0.00001))            
            #compraSugerida=1.12001
            f = open(file,'a')
            f.write("Preço de compra sugerido: "+str(compraSugerida)+"\n")
            f.close()
            quantidadeXRP=float("{0:9.8f}".format(saldoBRL/compraSugerida))
            f = open(file,'a')
            f.write("Quantidade de XRP calculado sem taxa: "+str(quantidadeXRP)+"\n")
            f.close()
            time.sleep(1)  
            buyOrder = PlaceBuyOrder('BRLXRP',quantidadeXRP,compraSugerida,str(int(time.time())))
            buyOrder_id = int(buyOrder.getOrderId())
            f = open(file,'a')
            f.write("Ordem de compra criado: "+str(buyOrder_id)+"\n")
            f.write("Aguardando 60 segundos .\n")
            f.close()
            time.sleep(20)
            f = open(file,'a')
            f.write("Aguardando 40 segundos ..\n")
            f.close()
            time.sleep(20)
            f = open(file,'a')
            f.write("Aguardando 20 segundos ...\n")
            f.close()
            time.sleep(20)
            ultimaCompra=compraSugerida
            cancelBuyOrder = CancelOrder("BRLXRP",buyOrder_id,str(int(time.time())))
            f = open(file,'a')
            f.write("Ordem de compra cancelada:\n")
            f.close()

        elif quantidadeXRP>=0.1:
            time.sleep(1)
            orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
            f = open(file,'a')
            f.write("\n############ ORDEN DE VENDA ############\n")
            f.close()
            menorVenda = float(orderBook.getOrderbookAsksLimitPrice())
            f = open(file,'a')
            f.write("Menor preço de venda do orderbook: "+str(menorVenda)+"\n")
            f.close()
            vendaSugerida = float(float(ultimaCompra)*1.01)
            cont=0
            while cont<20:
                menorVenda = float(orderBook.getOrderbookAsksLimitPrice(cont))
                f = open(file,'a')
                f.write("Menor venda com indice: {0} R${1:9.5f}".format(cont,menorVenda)+"\n")
                f.close()
                if vendaSugerida<menorVenda:
                    vendaSugerida=menorVenda-0.00001
                    break
                cont=cont+1
            f = open(file,'a')
            f.write("Preço de venda sugerido: "+"{0:9.8f}".format(vendaSugerida)+"\n")
            f.write("Ultimo preço de compra: R$"+str(ultimaCompra)+"\n")
            f.close()
            reais = float("{0:9.8f}".format(vendaSugerida*quantidadeXRP))
            f = open(file,'a')
            f.write("Valor em Reais calculado sem taxa: R$"+str(reais)+"\n")
            f.close()
            vendaSugerida = float("{0:9.5f}".format(vendaSugerida))
            #vendaSugerida = 1.12
            time.sleep(1)
            sellOrder = PlaceSellOrder("BRLXRP",quantidadeXRP,vendaSugerida,str(int(time.time())))
            sellOrder_id = sellOrder.getOrderId()
            f = open(file,'a')
            f.write("Ordem de venda criada: "+str(sellOrder_id)+"\n")
            f.write("Aguardando 60 segundos .\n")
            f.close()
            time.sleep(20)
            f = open(file,'a')
            f.write("Aguardando 40 segundos ..\n")
            f.close()
            time.sleep(20)
            f = open(file,'a')
            f.write("Aguardando 20 segundos ...\n")
            f.close()
            time.sleep(20)
            cancelar = CancelOrder("BRLXRP",sellOrder_id,str(int(time.time())))
            f = open(file,'a')
            f.write("Ordem de venda cancelada:"+sellOrder_id+"\n\n")
            f.close()            
        else:
            f = open(file,'a')
            f.write("\nVerificando se há ordens abertas...\n")
            f.close()
            l = ListOrders('BRLXRP',str(int(time.time())),2)
            if int(l.getOrdersStatus()) == 2:
                f = open(file,'a')
                f.write("Há ordens abertas com ID: "+str(l.getOrdersId())+"\n")
                f.close()
                time.sleep(1)
                cancelar = CancelOrder("BRLXRP",l.getOrdersId(),str(int(time.time())))
                f = open(file,'a')
                f.write("Ordem Cancelada.\nTentando Novamente.\n\n")
                f.close()                


    except :        
        f = open(file,'a')
        f.write("\nOcorreu algum erro!!!\n")
        f.write("Tentando novamente em 5 segundos!...\n")
        f.close()
        time.sleep(5)

