from place_sell_order import PlaceSellOrder
from cancel_order import CancelOrder
import time

sell = PlaceSellOrder('BRLXRP',0.1,1.081,)
time.sleep(30)
cancelarOrdem = CancelOrder('XRPBRL',sell.getOrderId())

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


