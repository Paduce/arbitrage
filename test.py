import requests
import json
from web3 import Web3, middleware
import defi.defi_tools as dft
import itertools
from secret import  private_key
from web3.gas_strategies.time_based import medium_gas_price_strategy,construct_time_based_gas_price_strategy
import time
import traceback
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import csv
import pickle
import matplotlib.pyplot as plt

pd.set_option("display.max_colwidth",500)
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org:443"))
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 5000)


wbnb = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
busd = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
cake = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'
bunny = '0xC9849E6fdB743d08fAeE3E34dd2D1bc69EA11a51'
usdc = '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'
btcb = '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c'
ethb = '0x2170Ed0880ac9A755fd29B2688956BD959F933F8'
safemoon = '0x8076C74C5e3F5852037F31Ff0093Eeb8c8ADd8D3'
ust = '0x23396cF899Ca06c4472205fC903bDB4de249D6fC'
dai = '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3'
dot = '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402'
ada = '0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47'
xrp = '0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE'
link = '0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD'


factory_address = '0xBCfCcbde45cE874adCB698cC183deBcF17952812'
factory_abi = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
pair_abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

contract = w3.eth.contract(address=factory_address,abi=factory_abi)

wbnb_busd_LP = w3.eth.contract(address = contract.functions.getPair(wbnb,busd).call(), abi=pair_abi)
busd_usdc_LP = w3.eth.contract(address = contract.functions.getPair(cake,busd).call(), abi=pair_abi)
usdc_wbnb_LP = w3.eth.contract(address = contract.functions.getPair(cake,wbnb).call(), abi=pair_abi)
wbnb_cake_LP = w3.eth.contract(address = contract.functions.getPair(wbnb,cake).call(), abi=pair_abi)


def LPGraph(nodes):
    start = time.time()
    G = nx.Graph()
    G.add_nodes_from(nodes)
    for i in range(0,len(nodes)):
        lista = []
        for j in range(i+1,len(nodes)):
            lista.append([nodes[i],nodes[j]])
        G.add_edges_from(lista)
        G.add_edge("0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",nodes[i])
    paths = nx.all_simple_paths(G, source='0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
                                target='0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',cutoff=4)
    path = []
    for k in list(paths):
        path.append(list(map(list,zip(k[:-1], k[1:]))))
    for i in range(0,len(path)):
        path[i][-1][1] = wbnb
    print("graph done")
    return(path)
tokens = [wbnb,busd,cake,bunny,usdc,btcb,ethb,safemoon,ust,dai,dot,ada,xrp,link]
path = LPGraph(tokens)

'''with open("out.csv","w",newline="") as f:
    wr = csv.writer(f)
    wr.writerows(path)'''
with open("data.txt", "wb") as file:
    pickle.dump(path, file)

with open("data.txt", "rb") as file:
    lista2 = pickle.load(file)

print(len(lista2[0]))
data = pd.DataFrame(lista2)

new_df = data[np.logical_and(data.iloc[:,0].astype(str) != str(data.iloc[1,1]),data.iloc[:,0].astype(str) != str(reversed(data.iloc[1,1])))]

while -1>0:
    LP_values = wbnb_busd_LP.functions.getReserves().call()
    a = LP_values[1]
    b = LP_values[0]
    c = b-(a*b)/(a+10**18*0.997)

    LP_values2 = busd_usdc_LP.functions.getReserves().call()
    a_ = LP_values2[1]
    b_ = LP_values2[1]
    c_ = b_-(a_*b_)/(a_+c*0.997)

    LP_values3 = usdc_wbnb_LP.functions.getReserves().call()
    a__ = LP_values3[1]
    b__ = LP_values3[0]
    c__ = b__-(a__*b__)/(a__+c_*0.997)
    if c__ > 1.0015 *10**18 :
        print("arbitrage opportunitie found")
        print(c)

def DataCleaning(path,tokens):
    combinations = list(itertools.combinations(tokens,2))
    address = list(map(lambda x:contract.functions.getPair(str(x[0]), str(x[1])).call(),combinations))
    df = pd.DataFrame()
    df["Pair"] = combinations
    df["LP"] = address
    valid = df[df.LP != "0x0000000000000000000000000000000000000000"].iloc[:,0]
    valid = list(map(list,valid))
    pair_dict_1 = dict(zip(combinations,address))
    pair_dict_2 = dict(zip(list(map(reversed,combinations)),address))
    pair_dict = {}
    pair_dict.update(pair_dict_1)
    pair_dict.update(pair_dict_2)
    print(valid.unique())
    print(pair_dict)
    valid_reversed = list(map(list,map(reversed,valid)))
    path = path[path.applymap(lambda x: np.logical_or(x in valid , x in valid_reversed))].dropna()
    print(path.shape)
    return (path, valid,pair_dict)
start = time.time()
data_cleaned = DataCleaning(data,tokens)
print(time.time() - start)

pair_dict = data_cleaned[2]
print(pair_dict)
data_cleaned[0].to_csv("out_cleaned_test.csv",index=False)
data_cleaned = pd.DataFrame(pd.read_csv("out_cleaned_test.csv"))
#print(pair_dict[tuple(path[i,j])])
def LP_addreses(path,pair_dict):
    tests = 0
    for i in range(0,path.shape[0]):
         amounts = [10**18]
         tests += 1
         try:
            for j in range(0,len(path.iloc[i,:].dropna())-1):
                LP_contract = w3.eth.contract(address=pair_dict[(str(path.iloc[i,j][2:44]),str(path.iloc[i,j][48:90]))], abi=pair_abi)
                LP = LP_contract.functions.getReserves().call()
                token0 = LP_contract.functions.token0().call()
                token1 = LP_contract.functions.token1().call()
                reserves = {token0:LP[0],token1:LP[1]}
                amounts.append(reserves[str(path.iloc[i,j][48:90])] - (reserves[str(path.iloc[i,j][2:44])] * reserves[str(path.iloc[i,j][48:90])]) / (reserves[str(path.iloc[i,j][2:44])] + amounts[j] * 0.997))
            if 1.2*10**18> amounts[-1] > 10**18:
                print(amounts[-1],"arbitrage found")

         except:
             print("failed")
             traceback.print_exc()
             continue
    return tests
start = time.time()
#print(LP_addreses(data_cleaned,pair_dict))
print(time.time() - start)
def LP_Reserves(LP_addresses,path):
    LP_Reserves = {}
    for i in range(0,len(LP_addresses),3):
        LP_Reserves[path[i]] = LP_addresses[i].functions.getReserves().call()
        LP_Reserves[path[i+1]] = LP_addresses[i+1].functions.getReserves().call()
        LP_Reserves[path[i+2]] = LP_addresses[i+2].functions.getReserves().call()
    return(LP_Reserves)





