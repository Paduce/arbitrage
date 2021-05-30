import requests
import json
from web3 import Web3, middleware
import defi.defi_tools as dft
import itertools
from secret import  private_key
from web3.gas_strategies.time_based import medium_gas_price_strategy,construct_time_based_gas_price_strategy
import time
import tempfile
import traceback
import pandas as pd
import numpy as np
import networkx as nx
import itertools
import webbrowser, os
import csv
import pickle
import qgrid
import matplotlib.pyplot as plt

w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org:443"))

wbnb = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'
busd = '0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'
cake = '0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82'
bunny = '0xC9849E6fdB743d08fAeE3E34dd2D1bc69EA11a51'
usdc = '0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d'
btcb = '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c'
busdt = '0x55d398326f99059fF775485246999027B3197955'
ethb = '0x2170Ed0880ac9A755fd29B2688956BD959F933F8'
safemoon = '0x8076C74C5e3F5852037F31Ff0093Eeb8c8ADd8D3'
ust = '0x23396cF899Ca06c4472205fC903bDB4de249D6fC'
dai = '0x1AF3F329e8BE154074D8769D1FFa4eE058B1DBc3'
dot = '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402'
ada = '0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47'
xrp = '0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE'
xvs = '0xcF6BB5389c92Bdda8a3747Ddb454cB7a64626C63'
link = '0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD'


tokens = {"W" : [wbnb,busd,usdc,dai,xvs,ust,busdt],
          "P" : [wbnb,busd,usdc,dai,xvs,ust,busdt],
          "A" : [wbnb,busd,usdc,dai,xvs,ust,busdt],
          "B" : [wbnb,busd,usdc,dai,xvs,ust,busdt]}

def open_file(dataFrame):
    tmp = tempfile.NamedTemporaryFile(delete=False)
    path = tmp.name+'.html'
    dataFrame.to_html(path)
    webbrowser.open("file://"+path)

def LPGraph(tokens):
    start_timer = time.time()
    G = {}
    for i in tokens.keys():
        G[i] = nx.Graph()
        tokens[i] = [i + j for j in tokens[i]]
        G[i].add_nodes_from(tokens[i])
        G[i].add_edges_from(list(itertools.combinations(tokens[i],2)))
    G = nx.compose_all([G["W"],G["P"],G["A"],G["B"]])
    for i in range(0,len(G.nodes())):
        for j in range(i+1,len(G.nodes())):
            if list(G.nodes())[i][1::] == list(G.nodes())[j][1::]:
                G.add_edge(list(G.nodes())[i],list(G.nodes())[j])
    print("int1 :", time.time() - start_timer)
    nx.draw_kamada_kawai(G, with_labels=False)
    nx.draw(G)
    node_to_cycles = {}
    start_timer = time.time()
    for source in G.nodes():
        paths = []
        for target in G.neighbors(source):
            paths += [l + [source] for l in list(nx.all_simple_paths(G, source=source, target=target, cutoff=2)) if len(l) > 2]
        node_to_cycles[source] = paths
    print("int2 :", time.time() - start_timer)
    path = []
    paths = node_to_cycles["W" + wbnb]
    start_timer = time.time()
    for k in list(paths):
        path.append(list(map(list,zip(k[:-1], k[1:]))))
    final = []
    print("int3 :", time.time() - start_timer)
    start_timer = time.time()
    for i in range(0,len(path)):
        final.append([])
        for j in range(0,len(path[i])):
            if path[i][j][0][1::] != path[i][j][1][1::]:
                if path[i][j][1][1::] == '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c':
                    final[i].append(path[i][j])
                    break
                else:
                    final[i].append(path[i][j])
    print("int4 :", time.time() - start_timer)
    return final
start = time.time()
path = LPGraph(tokens)
print(time.time() - start)
with open("data.txt", "wb") as file:
    pickle.dump(path, file)

with open("data.txt", "rb") as file:
    lista2 = pickle.load(file)
data = pd.DataFrame(lista2)



def TestLP(dict):
    Contract = {'W': ['0xB42E3FE71b7E0673335b3331B3e1053BD9822570','[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'],
                'A': ['0x0841BD0B734E4F5853f0dD8d7Ea041c241fb0Da6','[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'],
                'P': ['0xBCfCcbde45cE874adCB698cC183deBcF17952812','[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[],"name":"INIT_CODE_PAIR_HASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'],
                'B': ['0x01bF7C66c6BD861915CdaaE475042d3c4BaE16A7','[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]']
                }
    LP_Test = {}
    for i in dict.keys():
        contract = w3.eth.contract(address=Contract[i][0], abi=Contract[i][1])
        LP_Test[i] = list(map(lambda x:contract.functions.getPair(str(x[0][1::]), str(x[1][1::])).call(),dict[i]))
    return LP_Test

def DataCleaning(path,tokens):
    combinations = {i : list(itertools.combinations(tokens[i],2)) for i in tokens.keys()}
    address = TestLP(combinations)
    df = pd.DataFrame()
    df["Pair"] = [i for sublist in combinations.values() for i in sublist]
    df["LP"] = [i for sublist in address.values() for i in sublist]
    df1 = df[df.LP != "0x0000000000000000000000000000000000000000"]
    valid = df1.iloc[:, 0]
    valid = list(map(list, valid))
    valid_reversed = list(map(list, map(reversed, valid)))
    df2 = pd.DataFrame()
    df2["Pair"] = valid_reversed
    df2["LP"] = df1.iloc[:, 1].to_list()
    pair_dict = pd.concat([df1, df2], ignore_index=True)
    pair_dict = dict(zip(map(tuple, pair_dict.iloc[:, 0].to_list()), pair_dict.iloc[:, 1].to_list()))
    path = path.fillna("This was a NA")
    valid.append("This was a NA")
    print(path.shape)
    path = path[path.applymap(lambda x: np.logical_or(x in valid, x in valid_reversed))].dropna()
    path = path.replace("This was a NA",np.nan)
    open_file(path)
    print(path.shape)
    return (path, valid,pair_dict)


start = time.time()
data_cleaned = DataCleaning(data,tokens)
print(time.time() - start)

pair_dict = data_cleaned[2]
data_cleaned[0].to_csv("out_cleaned_test.csv",index=False)
data_cleaned = pd.DataFrame(pd.read_csv("out_cleaned_test.csv"))


def LP_addreses(path,pair_dict):
    pair_abi = '[{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount0In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1In","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount0Out","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount1Out","type":"uint256"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"Swap","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint112","name":"reserve0","type":"uint112"},{"indexed":false,"internalType":"uint112","name":"reserve1","type":"uint112"}],"name":"Sync","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MINIMUM_LIQUIDITY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"burn","outputs":[{"internalType":"uint256","name":"amount0","type":"uint256"},{"internalType":"uint256","name":"amount1","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_token0","type":"address"},{"internalType":"address","name":"_token1","type":"address"}],"name":"initialize","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"mint","outputs":[{"internalType":"uint256","name":"liquidity","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"price0CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"price1CumulativeLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"}],"name":"skim","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"uint256","name":"amount0Out","type":"uint256"},{"internalType":"uint256","name":"amount1Out","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"swap","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"sync","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
    while 1>0:
        tests = 0
        for i in range(0,path.shape[0]):
             amounts = [10**18]
             tests += 1
             try:
                for j in range(0,len(path.iloc[i,:].dropna())):
                    LP_contract = w3.eth.contract(address=pair_dict[(str(path.iloc[i,j][2:45]),str(path.iloc[i,j][49:92]))], abi=pair_abi)
                    LP = LP_contract.functions.getReserves().call()
                    token0 = LP_contract.functions.token0().call()
                    token1 = LP_contract.functions.token1().call()
                    reserves = {token0:LP[0],token1:LP[1]}
                    numerator = amounts[j]*0.998*reserves[str(path.iloc[i,j][50:92])]
                    denominator = reserves[str(path.iloc[i,j][3:45])] + amounts[j]*0.998
                    amounts.append(numerator / denominator)
                if amounts[-1] > 10**18:
                    print(amounts[-1],"arbitrage found")

             except:
                 print("failed")
                 traceback.print_exc()
                 continue

LP_addreses(data_cleaned,pair_dict)