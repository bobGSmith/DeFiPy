#!/bin/python3
'''Terminal Token Chart 

Display token price charts in terminal 

Run as script:
python3 -m DeFiPy.chart TOKEN DENOMINATE_IN N_DAYS

Where TOKEN is the token you want to chart, DENOMINATE is what you want it priced in (e.g. USD), 
and N_DAYS is the number of days you want the chart to cover. 
'''

import requests 
import sys
import termplotlib as tpl
from datetime import datetime
import time
import os 


try: 
	t = sys.argv[1] 
	d = sys.argv[2] 
	days = int(sys.argv[3])

	url = f'https://api.coingecko.com/api/v3/coins/{t}/market_chart?vs_currency={d}&days={days}&interval=hourly'

	data = (requests.get(url, headers = {"accept":"application/json"})).json()

	prices = []
	times = []
	xlabs = []
	for i, price in enumerate(data["prices"]):
	    xlabs.append(i)
	    times.append(price[0])
	    prices.append(price[1])
	 
	width = int(os.get_terminal_size().lines * 3)

	start = datetime.fromtimestamp(time.time() - (days * 86400))
	t_now = datetime.fromtimestamp(time.time())
	print(f"Terminal Token Chart ({t}/{d})")
	print(f"Range: {start} - {t_now} ({days} days)")
	print(f"Current Price: {round(data['prices'][-1][1],4)} {d}")
	fig = tpl.figure()
	fig.plot(xlabs,prices,width=width,height=(width//3)-4)
	fig.show()
	
except Exception as e: 
	print(f"Error: {e}")
	print("See Docs below\n") 
	print(__doc__)
