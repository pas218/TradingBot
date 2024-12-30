#Imports
from lib2to3.main import diff_texts

import ibapi
import talib
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
#Vars
orderId = 1
# Letters in alphabet
globalBarrier = 1


#Class for Interactive Brokers Connection
class IBApi(EWrapper,EClient):
    orderNumber = 15000
    closingValues = np.zeros(720)
    smaValues = np.zeros(720)
    closingValuesIndex = 0
    dates = np.empty(720, dtype=object)
    def __init__(self):
        EClient.__init__(self, self)
    def nextValidId(self, nextorderId):
        global orderId
        orderId = nextorderId

    def realtimeBar(self, reqId, time: int, open: float, high: float, low: float, close: float,
                    volume, wap, count: int):
        super().realtimeBar(reqId, time, open, high, low, close, volume, wap, count)
        try:
            print("TickerId:", reqId, "close:", close, "open:", open, "high:", high, "low:", low, "volume:", volume, "wap:", wap)

            #if close < globalBarrier:
            #    contract = Contract()
            #    contract.symbol = globalSymbol
            #    contract.secType = "OPT"
            #    contract.exchange = "SMART"
            #   contract.primaryExchange = "ISLAND"
            #   contract.currency = "USD"
            #    orderTest = Order()
            #    # parent.orderId = parentOrderId
            #    orderTest.orderType = "MKT"
            #    orderTest.action = "BUY"
            #    orderTest.totalQuantity = 1
            #    self.placeOrder(orderId, contract, orderTest)
            #    #f.write("Buy " + globalSymbol + " at " + str(close))
            #else:
            #    contract = Contract()
            #    contract.symbol = globalSymbol
            #    contract.secType = "OPT"
            #    contract.exchange = "SMART"
            #    contract.primaryExchange = "ISLAND"
            #    contract.currency = "USD"
            #    orderTest = Order()
                # parent.orderId = parentOrderId
            #    orderTest.orderType = "MKT"
            #    orderTest.action = "SELL"
            #    orderTest.totalQuantity = 1
            #    self.placeOrder(orderId, contract, orderTest)
            #print("Order number", orderId)
            #print("Ticker", globalSymbol)
            #print("Barrier", globalBarrier)
            #self.reqIds(-1)
            self.shiftArrayLeftOne(720)
            self.closingValues[719] = close
            self.smaValues[719] = self.findSMA(720)
            print(self.closingValues)
            print(self.smaValues)
            #print(self.sma)
        except Exception as e:
            print(e)

    def headTimestamp(self, reqId, headTimestamp):
        #print("got in")
        print(reqId, headTimestamp)

    def historicalData(self, reqId: int, bar):
        self.closingValues[self.closingValuesIndex] = bar.close
        self.dates[self.closingValuesIndex] = bar.date
        self.closingValuesIndex += 1
    def shiftArrayLeftOne(self, length):
        for i in range(0, length):
            if i == (length - 1):
                self.closingValues[i] = 0.0
                self.smaValues[i] = 0.0
            else:
                self.closingValues[i] = self.closingValues[i+1]
                self.smaValues[i] = self.smaValues[i+1]

    def findSMA(self, length):
        returnValue = 0.0
        for i in range(0, length):
            returnValue += self.closingValues[i]
        returnValue /= length
        return returnValue

    def error(self, id, errorCode, errorMsg, advancedOrderRejection=""):
        print(errorCode)
        print(errorMsg)
#Bar Object
class Bar:
    open = 0
    low = 0
    high = 0
    close = 0
    volume = 0
    date = datetime.now()
    def __init__(self):
        self.open = 0
        self.low = 0
        self.high = 0
        self.close = 0
        self.volume = 0
        self.date = datetime.now()
#Bot Logic
class Bot:
    ib = None
    barsize = 1
    currentBar = Bar()
    bars = []
    reqId = 1
    smaPeriod = 50
    identify = 2200
    symbol = ""
    close = []
    def __init__(self):
        #Connect to IB on init
        self.ib = IBApi()
        self.ib.connect("127.0.0.1", 7497,1)
        ib_thread = threading.Thread(target=self.run_loop, daemon=True)
        ib_thread.start()
        time.sleep(1)
        currentBar = Bar()
        #Get symbol info
        global globalSymbol
        global globalBarrier
        global orderId
        globalSymbol = input("Enter the symbol you want to trade : ")
        #Get bar size
        globalBarrier = float(input("Enter the value about which you would like to trade : "))
        #orderId = int(input("Enter the order id you want to start trading from : "))
        #print("original ticker", globalSymbol)
        #print("original barrier", globalBarrier)
        #print("original orderId", orderId)
        mintext = " min"
        if (int(self.barsize) > 1):
            mintext = " mins"
        #self.identify = self.ib.reqIds(-1)
        contract = Contract()
        contract.symbol = globalSymbol.upper()
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        #orderTest = Order()
        # parent.orderId = parentOrderId
        #orderTest.orderType = "MKT"
        #orderTest.action = "BUY"
        #orderTest.totalQuantity = 1
        #self.ib.placeOrder(orderId, contract, orderTest)
        self.ib.reqIds(-1)
        #print(orderId)
        #self.ib.reqRealTimeBars(self.identify, contract, 5, "MIDPOINT", 0, [])
        #self.ib.reqHeadTimeStamp(1, contract , "ASK", 1, 2)
        self.ib.reqHistoricalData(4102, contract, "", "3600 S", "5 secs", "TRADES", 1, 1, True, [])
        time.sleep(2)
        #print(self.ib.closingValues)
        self.ib.sma = talib.SMA(self.ib.closingValues, timeperiod=720)
        print(self.ib.closingValues)
        print(self.ib.dates)
        print(self.ib.smaValues)
        print(self.ib.closingValues.size)
        print(self.ib.dates.size)
        print(self.ib.smaValues.size)
        self.ib.reqRealTimeBars(3001, contract, 5, "TRADES", 0, [])


    #Listen to socket in seperate thread
    def run_loop(self):
        self.ib.run()
    #Bracet Order Setup
    def bracketOrder(self, parentOrderId, action, quantity, profitTarget, stopLoss):
        #Initial Entry
        #Create our IB Contract Object
        contract = Contract()
        contract.symbol = self.symbol.upper()
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Create Parent Order / Initial Entry
        parent = Order()
        parent.orderId = parentOrderId
        parent.orderType = "MKT"
        parent.action = action
        parent.totalQuantity = quantity
        parent.transmit = False
        # Profit Target
        profitTargetOrder = Order()
        profitTargetOrder.orderId = parent.orderId+1
        profitTargetOrder.orderType = "LMT"
        profitTargetOrder.action = "SELL"
        profitTargetOrder.totalQuantity = quantity
        profitTargetOrder.lmtPrice = round(profitTarget,2)
        profitTargetOrder.parentId = parentOrderId
        profitTargetOrder.transmit = False
        # Stop Loss
        stopLossOrder = Order()
        stopLossOrder.orderId = parent.orderId+2
        stopLossOrder.orderType = "STP"
        stopLossOrder.action = "SELL"
        stopLossOrder.totalQuantity = quantity
        stopLossOrder.parentId = parentOrderId
        stopLossOrder.auxPrice = round(stopLoss,2)
        stopLossOrder.transmit = True

        bracketOrders = [parent, profitTargetOrder, stopLossOrder]
        return bracketOrders

    # Bracket Order Setup
    def bracketOrderOne(self, parentOrderId, action, quantity):
        # Initial Entry
        # Create our IB Contract Object
        contract = Contract()
        contract.symbol = self.symbol.upper()
        contract.secType = "OPT"
        contract.exchange = "SMART"
        contract.currency = "USD"
        # Create Parent Order / Initial Entry
        parent = Order()
        #parent.orderId = parentOrderId
        parent.orderType = "MKT"
        parent.action = action
        parent.totalQuantity = quantity
        parent.transmit = False

        bracketOrder = parent
        return

    #Pass realtime bar data back to our bot object
    def on_bar_update(self, reqId, close,realtime):
        #print("test")
        global orderId
        #Historical Data to catch up
        if (realtime == False):
            #print("test realtime false")
            #self.bars.append(close)
            print("false")
        else:
            print(close)
            print("in on bar update")

            # Check Criteria
            quantity = 1
            contract = Contract()
            contract.symbol = self.symbol
            contract.secType = "OPT"
            contract.exchange = "SMART"
            contract.primaryExchange = "ISLAND"
            contract.currency = "USD"
            orderTest = Order()
            # parent.orderId = parentOrderId
            orderTest.orderType = "MKT"
            orderTest.action = "BUY"
            orderTest.totalQuantity = 1
            self.currentBar.close = bar.close
            print("New bar!")
            self.bars.append(self.currentBar)
            self.currentBar = Bar()
            self.currentBar.open = bar.open




print("Before bot")

#Start Bot
bot = Bot()

print("after bot")

