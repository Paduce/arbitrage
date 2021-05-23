import requests
import json
from web3 import Web3
import time
profits = [0]

while -1>0:
    try:
        url_bnb_busd =requests.get('https://api.1inch.exchange/v3.0/56/quote?fromTokenAddress=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&toTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&amount=500000000000000000').json()
        url_busd_bnb = requests.get(f'https://api.1inch.exchange/v3.0/56/quote?fromTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&toTokenAddress=0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c&amount={url_bnb_busd["toTokenAmount"]}').json()
        print(int(url_busd_bnb['toTokenAmount']))
        if int(url_busd_bnb['toTokenAmount'])-10*int(url_busd_bnb['estimatedGas'])-10*int(url_bnb_busd['estimatedGas']) > 500000000000000000:
            profit = (int(url_busd_bnb['toTokenAmount'])-5*int(url_busd_bnb['estimatedGas'])-5*int(url_bnb_busd['estimatedGas']))*10**-18-0.5
            if profits[-1] != profit:
                profits.append(profits[-1] + profit)
            print(f'Found 1inch arbitrage opportunitie: {profit}BNB')
            print(f'Pofits so far {profits[-1]}')
        time.sleep(6)
    except:
        continue