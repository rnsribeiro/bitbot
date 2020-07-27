# coding: latin1
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

print("\tObtendo o valor da última Compra ...")
l = ListOrders('BRLXRP',str(int(time.time())),4,1)
ultimaCompra = l.getOrdersLimitPrice()
print("\tValor da última Compra: R$"+str(ultimaCompra))   

ordensDia=0

cont=0
#time.sleep(1)
#listOrders = ListOrders("BRLXRP",str(int(time.time())))



while True:
    try:
        #os.system("clear")
        # Cabeçalho e alteração de cor para amarelo
        print("\t"+"\033[33m"+"Bot Iniciado: "+inicioBot)
        print("\tOperação Iniciada: "+str(datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')))
        print("\tOrdens criadas no dia: "+str(ordensDia)+"\033[0;0m")

        ordensDia=ordensDia+1

        time.sleep(1)
        #try:
        AccountInfo = GetAccountInfo(str(int(time.time())))
        saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
        quantidadeXRP = float(AccountInfo.getBalanceAvailable('xrp'))    

        if saldoBRL>=10.0:
            time.sleep(1)
            orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
            print("\t"+'\033[32m'+"############ ORDEN DE COMPRA ############"+'\033[0;0m')
            print("\tValor da última Compra: R$"+str(ultimaCompra))   
            print("\tSaldo de Reais: R$"+str(saldoBRL))
            maiorCompra = float(orderBook.getOrderbookBidsLimitPrice())
            print("\tMaior preço de compra do orderbook: "+str(maiorCompra))
            compraSugerida=float("{0:9.5f}".format(maiorCompra+0.00001))            
            compraSugerida=1.1008
            print("\tPreço de compra sugerido: "+str(compraSugerida))
            quantidadeXRP=float("{0:9.8f}".format(saldoBRL/compraSugerida)) 
            print("\tQuantidade de XRP calculado sem taxa: "+str(quantidadeXRP)) 
            time.sleep(1)  
            buyOrder = PlaceBuyOrder('BRLXRP',quantidadeXRP,compraSugerida,str(int(time.time())))
            buyOrder_id = int(buyOrder.getOrderId())
            print("\tOrdem de compra criado: "+str(buyOrder_id))
            print("\tAguardando 60 segundos .")
            time.sleep(20)
            print("\tAguardando 40 segundos ..")
            time.sleep(20)
            print("\tAguardando 20 segundos ...")
            time.sleep(20)
            ultimaCompra=compraSugerida
            cancelBuyOrder = CancelOrder("BRLXRP",buyOrder_id,str(int(time.time())))
            print("\tOrdem de compra cancelada:")
            print("\n\n")

        elif quantidadeXRP>=0.1:
            time.sleep(1)
            orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
            print("\t"+'\033[31m'+"############ ORDEN DE VENDA ############"+'\033[0;0m')
            menorVenda = float(orderBook.getOrderbookAsksLimitPrice())
            print("\tMenor preço de venda do orderbook: "+str(menorVenda))
            vendaSugerida = float(float(ultimaCompra)*1.008)
            cont=0
            while cont<20:
                menorVenda = float(orderBook.getOrderbookAsksLimitPrice(cont))
                print("\tMenor venda com indice: {0} R${1:9.5f}".format(cont,menorVenda))
                if vendaSugerida<menorVenda:
                    vendaSugerida=menorVenda-0.00001
                    break
                cont=cont+1
            print("\tPreço de venda sugerido: "+"{0:9.8f}".format(vendaSugerida))
            print("\n\tUltimo preço de compra: R$"+str(ultimaCompra))
            reais = float("{0:9.8f}".format(vendaSugerida*quantidadeXRP))
            print("\tValor em Reais calculado sem taxa: R$"+str(reais))
            #vendaSugerida = float("{0:9.5f}".format(vendaSugerida))
            vendaSugerida = 1.12
            time.sleep(1)
            sellOrder = PlaceSellOrder("BRLXRP",quantidadeXRP,vendaSugerida,str(int(time.time())))
            sellOrder_id = sellOrder.getOrderId()
            print("\tOrdem de venda criada: "+str(sellOrder_id))
            print("\tAguardando 60 segundos .")
            time.sleep(20)
            print("\tAguardando 40 segundos ..")
            time.sleep(20)
            print("\tAguardando 20 segundos ...")
            time.sleep(20)
            cancelar = CancelOrder("BRLXRP",sellOrder_id,str(int(time.time())))
            print("\tOrdem de venda cancelada:")
            print("\n\n")
        else:
            print("\tVerificando se há ordens abertas...")
            l = ListOrders('BRLXRP',str(int(time.time())),2)
            if int(l.getOrdersStatus()) == 2:
                print("\tHá ordens abertas com ID: "+str(l.getOrdersId()))
                time.sleep(1)
                cancelar = CancelOrder("BRLXRP",l.getOrdersId(),str(int(time.time())))
                print("\tOrdem Cancelada.\n\tTentar Novamente.")
                print("\n\n")


    except :        
        print("\tOcorreu algum erro!!!")
        print("\tAguardará 10 segundos para tentar novamente!")
        print("\n\n")
        time.sleep(10)

