#!/bin/python3
'''Terminal Token Chart 

Display token price charts in terminal 

Run as script:
python3 -m DeFiPy.chart TOKEN DENOMINATE_IN N_DAYS MPL_TPL 

Where TOKEN is the token you want to chart, DENOMINATE is what you want it priced in (e.g. USD), 
and N_DAYS is the number of days you want the chart to cover. 
MPL_TPL is a string either "mpl" or "tpl". "tpl" will produce a plot in terminal, "mpl" will pop up a matplotlib plot.
'''

import requests 
import sys
from datetime import datetime
import time
import os 

try: 
	t = sys.argv[1] 
	d = sys.argv[2] 
	days = int(sys.argv[3])

	url = f'https://api.coingecko.com/api/v3/coins/{t}/market_chart?vs_currency={d}&days={days}'#&interval=hourly'

	data = (requests.get(url, headers = {"accept":"application/json"})).json()


	prices = []
	times = []
	xlabs = []
	for i, price in enumerate(data["prices"]):
		xlabs.append(i)
		times.append(datetime.fromtimestamp(int(price[0])/1000))
		prices.append(price[1])
	 
	

	start = datetime.fromtimestamp(time.time() - (days * 86400))
	t_now = datetime.fromtimestamp(time.time())
	print(f"Terminal Token Chart ({t}/{d})")
	print(f"Range: {start} - {t_now} ({days} days)")
	print(f"Current Price: {round(data['prices'][-1][1],4)} {d}")
 	
	if sys.argv[4].lower() == "tpl": 
		import plotext as plt 
		width = int(os.get_terminal_size().lines * 3)
		plt.plot(xlabs,prices)
		plt.title(f"{t} price: {days} days")
		plt.xlabel("days")
		plt.ylabel(f"Price ({d})")
		plt.theme("matrix")
		plt.show()
	else: 
		import matplotlib.pyplot as plt 
		plt.plot(times,prices)
		plt.title(f"{t}/{d}: {round(data['prices'][-1][1],4)}")
		plt.xticks(rotation=45)
		plt.ylabel(f"price ({d})")
		plt.tight_layout()
		plt.show()	    
except Exception as e: 
	print(f"Error {e}")
	print("See Docs below\n") 
	print(__doc__)
