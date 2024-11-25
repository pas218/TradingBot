# Imports
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
#
from ibapi.contract import Contract
from ibapi.order import *
import threading
import time
#Vars

#Class for Interactive Brokers Connection
class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    # Listen for real time bars
    def realtimeBar(self, reqId, time, open, high, low, close, volume, wap, count):
        super().realtimeBar(self, reqId, time, open, high, low, close, volume, wap)
        try:
            bot.on_bar_update(reqId, time, open, high, low, close, volume, wap, count)
        except Exception as e:
            print(e)
    def error(self, id, errorCode, errorMsg, advancedOrderRejectJson):
        print(errorCode)
        print(errorMsg)
#Bot logic
class Bot:
    ib = None
    def __init__(self):
        # Connect to IB on innit
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7496, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        # Get symbol info
        symbol = input("Enter the symbol you want to trade: ")
        # Create our ID Contract Object
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Request Market Data
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])

        # Create Order Object
        order = Order()
        order.orderType = "MKT"  # or LMT ETC...
        order.action = "SELL" # or SELL ETC ...
        quantity = 1
        order.totalQuantity = quantity
        # Create Contract Object
        contract = Contract()
        contract.symbol = symbol
        contract.secType = "STK" # or FUT ETC ...
        contract.exchange = "SMART"
        contract.primaryExchange = "ISLAND"
        contract.currency = "USD"
        # Place the order
        self.ib.placeOrder(6, contract, order)
    # Listen to socket in separate thread
    def run_loop(self):
            self.ib.run()
    # Pass realtime bar data back to our bot object
    def on_bar_update(self, reaId, time, open, high, low, close, volume, wap, count):
        print(close)
#Start Bot
bot = Bot()