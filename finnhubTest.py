import numpy as np
from numpy import random
import talib
from talib import MA_Type

close = random.random(100)

output = talib.SMA(close, timeperiod = 5)
output1 = talib.MA(close, timeperiod = 5)
print(output)
print(output1)