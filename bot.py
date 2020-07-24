'''
    Passos para operação do bot
        Passo 1:Obter o saldo na conta em Reais
        Passo 2:Obter o maior preço de compra da moeda
        Passo 3:Obter o spreed para ver se compensa a operação
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
from cancel_order import CancelOrder

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
        