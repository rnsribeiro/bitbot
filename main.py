#from cancel_order import CancelOrder
#from place_sell_order import PlaceSellOrder
from list_orderbook import ListOrderBook
import time

#sell = PlaceSellOrder("BRLXRP",0.1,1.081)
#time.sleep(10)
#
#print(sell.getOrderId())
#cancel = CancelOrder("BRLXRP",sell.getOrderId(),str(int(time.time())))

listOrderBook = ListOrderBook("BRLXRP",str(int(time.time())))
print(listOrderBook.getOrderbookAsksID())

