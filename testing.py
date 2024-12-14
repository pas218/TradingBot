import ta
import numpy as np
import pandas as pd
import pytz
import math
from datetime import datetime, timedelta
import threading
import time

print(datetime.now())
print(datetime.now().astimezone(pytz.timezone("America/New_York")))
print(datetime.now().astimezone(pytz.timezone("America/Chicago")))
print(timedelta(days=1, hours=3))
print(datetime.now().astimezone(pytz.timezone("America/New_York"))-timedelta(days=1))
print((datetime.now().astimezone(pytz.timezone("America/New_York"))-timedelta(days=1)).replace(hour=16,minute=0,second=0,microsecond=0))
print((datetime.now().astimezone(pytz.timezone("America/New_York"))-timedelta(days=1)).replace(hour=16,minute=0,second=0,microsecond=0).strftime("%Y%m%d %H:%M:%S"))