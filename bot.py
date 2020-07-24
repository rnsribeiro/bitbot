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

ultimaCompra=0

cont=0
while True:    
    time.sleep(1)
    listOrders = ListOrders("BRLXRP",str(int(time.time())))
    if int(listOrders.getOrdersOrderType(cont))==1:
        ultimaCompra=float(listOrders.getOrdersLimitPrice(cont))
        break
    cont=cont+1

while True:
    os.system("clear")

    time.sleep(1)
    AccountInfo = GetAccountInfo(str(int(time.time())))
    saldoBRL = float(AccountInfo.getBalanceAvailable('brl'))
    quantidadeXRP = float(AccountInfo.getBalanceAvailable('xrp'))
    

    if saldoBRL>=10.0:
        time.sleep(1)
        orderBook = ListOrderBook('BRLXRP',str(int(time.time())))
        print("############ ORDEN DE COMPRA ############")
        print("Saldo de Reais: R$"+str(saldoBRL))
        maiorCompra = float(orderBook.getOrderbookBidsLimitPrice())
        print("Maior preço de compra do orderbook: "+str(maiorCompra))
        compraSugerida=float(maiorCompra+0.0001)
        print("Preço de compra sugerido: "+str(compraSugerida))
        quantidadeXRP=float("{0:9.8f}".format(saldoBRL/compraSugerida)) 
        print("Quantidade de XRP calculado sem taxa: "+str(quantidadeXRP)) 
        time.sleep(1)  
        buyOrder = PlaceBuyOrder('BRLXRP',quantidadeXRP,compraSugerida,str(int(time.time())))
        buyOrder_id = int(buyOrder.getOrderId())
        print("Ordem de compra criado: "+str(buyOrder_id))
        print("Aguardando 30 segundos .")
        time.sleep(10)
        print("Aguardando 20 segundos ..")
        time.sleep(10)
        print("Aguardando 10 segundos ...")
        time.sleep(10)
        ultimaCompra=compraSugerida
        cancelBuyOrder = CancelOrder("BRLXRP",buyOrder_id,str(int(time.time())))
        print("Ordem de compra cancelada:")
        print("\n\n")

    elif quantidadeXRP>=0.1:
        time.sleep(1)
        orderBook = ListOrderBook('BRLXRP',str(int(time.time())))

        print("############ ORDEN DE VENDA ############")
        menorVenda = float(orderBook.getOrderbookAsksLimitPrice())
        print("Menor preço de venda do orderbook: "+str(menorVenda))

        vendaSugerida = float(ultimaCompra*1.01)

        cont=0
        while cont<15:
            menorVenda = float(orderBook.getOrderbookAsksLimitPrice(cont))
            if vendaSugerida<menorVenda:
                vendaSugerida=menorVenda-0.0001
                break
            cont=cont+1

        print("Preço de venda sugerido: "+str(vendaSugerida))

        reais = float("{0:9.8f}".format(vendaSugerida*quantidadeXRP))
        print("Valor em Reais calculado sem taxa: R$"+str(reais))
        vendaSugerida = float("{0:9.5f}".format(vendaSugerida))

        time.sleep(1)
        sellOrder = PlaceSellOrder("BRLXRP",quantidadeXRP,vendaSugerida,str(int(time.time())))
        sellOrder_id = sellOrder.getOrderId()
        print("Ordem de venda criada: "+str(sellOrder_id))
        print("Aguardando 30 segundos .")
        time.sleep(10)
        print("Aguardando 20 segundos ..")
        time.sleep(10)
        print("Aguardando 10 segundos ...")
        time.sleep(10)
        cancelar = CancelOrder("BRLXRP",sellOrder_id,str(int(time.time())))
        print("Ordem de venda cancelada:")
        print("\n\n")
    
    else:
        print("Saldo Insuficiente!!")
        break
        


'''
while True:
    os.system("clear")
    time.sleep(1)
    print('#############################################')
    AccountInfo = GetAccountInfo(str(int(time.time())))
    print("Obtendo informações da conta:")
    time.sleep(1)
    OrderBook = ListOrderBook('BRLXRP',str(int(time.time())))
    print("Obtendo informações do orderbook:")

    # Obtém o saldo em xrp 
    # Obs: coin em letras minúsculas Ex:xrp
    quantidadeXRP = float(AccountInfo.getBalanceAvailable('xrp'))
    print("Saldo em XRP: "+str(quantidadeXRP))

    if quantidadeXRP>=0.1 :

        menorVenda = float(OrderBook.getOrderbookAsksLimitPrice())
        print("Menor preço de venda do orderbook: "+str(menorVenda))
        priceVenda = float(menorVenda-0.0001)
        print("Preço de venda sugerido: "+str(priceVenda))

        reais = float("{0:9.8f}".format(priceVenda*quantidadeXRP))
        print("Valor em Reais calculado sem taxa: R$"+str(reais))

        time.sleep(1)
        sellOrder = PlaceSellOrder("BRLXRP",quantidadeXRP,priceVenda,str(int(time.time())))
        order_id = sellOrder.getOrderId()
        print("Ordem de venda criada: "+str(order_id))
        print("Aguardando 30 segundos .")
        time.sleep(10)
        print("Aguardando 20 segundos ..")
        time.sleep(10)
        print("Aguardando 10 segundos ...")
        time.sleep(10)
        cancelar = CancelOrder("BRLXRP",order_id,str(int(time.time())))
        print("Ordem de venda cancelada:")
        print("\n\n")
    else:
        print("Quantidade de XRP menor que o necessário para criar ordem.")
        break
'''