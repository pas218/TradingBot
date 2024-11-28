# Imports
import ibapi
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *
import ta
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
import threading
import time
orderId = 6
#Vars

#Class for Interactive Brokers Connection
class IBApi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, False)
        except Exception as e:
            print(e)
    # On Realtime Var after historical data finished
    def historicalDataUpdate(self, reqId, bar):
        try:
            bot.on_bar_update(reqId, bar, True)
        except Exception as e:
            print(e)
    # On Historical Data End
    def historicalDataEnd(self, reqId, start, end):
        print(reqId)
    # Get next order ID we can use
    def nextValidId(self, nextorderId):
        global orderId = nextorderId
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

# Bar Object
class Bar:
    open = 0
    low = 0
    high = 0
    close = 0
    volume = 0
    date = ''
    def __init__(self):
        self.open = 0
        self.low = 0
        self.high = 0
        self.close = 0
        self.volume = 0
        self.date = ''

#Bot logic
class Bot:
    ib = None
    barsize = 1
    currentBar = Bar()
    reqId = 1
    global orderId
    smaPeriod = 50
    symbol = ""
    initialbartime = datetime.now().astimezone(pytz.timezone('America/New_York'))
    def __init__(self):
        # Connect to IB on innit
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7496, 1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        currentBar = Bar()
        # Get symbol info
        self.symbol = input("Enter the symbol you want to trade: ")
        # Get bar size
        self.barsize = input("Enter the barsize you want to trade in minutes: ")
        mintext = " min"
        if (int(self.barsize) > 1):
            mintext = " mins"
        queryTime = (datetime.now().astimezone(pytz.timezone('America/New_York'))-timedelta(days-1)).replace(hour=16, minute=0, second=0, microsecond=0).strftime("%Y%m%d %H:%M:%S")
        self.ib.reqHistoricalData(self.reqId, contract, "", "2 D", str(self.barsize)+mintext, "TRADES", 1, 1, True, [])
        # Create our ID Contract Object
        contract = Contract()
        contract.symbol = symbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Request Market Data
        self.ib.reqRealTimeBars(0, contract, 5, "TRADES", 1, [])

        # Create Order Object
        #order = Order()
        #order.orderType = "MKT"  # or LMT ETC...
        #order.action = "SELL" # or SELL ETC ...
        #quantity = 1
        #order.totalQuantity = quantity
        # Place the order
        #self.ib.placeOrder(6, contract, order)
    # Listen to socket in separate thread
    def run_loop(self):
            self.ib.run()
    # Pass realtime bar data back to our bot object
    def on_bar_update(self, reaId, bar, realTime):
        # Historical data to catch up
        if (realTime == False):
            self.bars.
#Start Bot
bot = Bot()