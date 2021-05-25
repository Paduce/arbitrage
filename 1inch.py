import requests
import json
from web3 import Web3, middleware
from secret import  private_key
from web3.gas_strategies.time_based import medium_gas_price_strategy,construct_time_based_gas_price_strategy
import time
import traceback
w3 = Web3(Web3.HTTPProvider("https://bsc-dataseed1.binance.org:443"))


def Buy(amount):
    print("Called")
    while 1 > 0:
        try:
            trade = requests.get(f'https://api.1inch.exchange/v3.0/56/swap?fromTokenAddress=0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c&toTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&amount={amount}&fromAddress=0xCd531e3904FE9e393e97E6f316008dA8e1516145&slippage=1&gasPrice=6&partialFillEnabled=false&gasLimit=800000').json()
            url_busd_bnb = requests.get(f'https://api.1inch.exchange/v3.0/56/quote?fromTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&toTokenAddress=0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c&amount={trade["toTokenAmount"]}&slippage=1&gasPrice=6&partialFillEnabled=false&gasLimit=800000').json()
            if int(url_busd_bnb['toTokenAmount']) - 6000000000 * int(trade["tx"]['gas']) - 6000000000 * int(url_busd_bnb['estimatedGas']) > 500000000000000000:
                nonce = w3.eth.get_transaction_count("0xCd531e3904FE9e393e97E6f316008dA8e1516145")
                gas = int(trade["tx"]['gas'])
                trade["tx"]["nonce"]=nonce
                trade["tx"]["to"] = "0x11111112542D85B3EF69AE05771c2dCCff4fAa26"
                trade["tx"]["gasPrice"] = Web3.toWei(trade["tx"]["gasPrice"],'gwei')
                trade["tx"]["value"] = Web3.toWei(trade["tx"]["value"], 'gwei')
                signed_txn = w3.eth.account.sign_transaction(trade["tx"], private_key=private_key)
                w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print(f'Swapped {trade["fromTokenAmount"]}BNB for {trade["toTokenAmount"]} BUSD')
                time.sleep(35)
                print("gas:", gas)
                Sell(trade["toTokenAmount"],gas)
            else:
                continue
        except:
            print("Bad Request")
            traceback.print_exc()
            continue


def Sell(amount,gas):
    print("Called")
    print("entered values:" , amount,gas)
    while 1 > 0:
            try:
                trade = requests.get(f'https://api.1inch.exchange/v3.0/56/swap?fromTokenAddress=0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56&toTokenAddress=0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c&amount={amount}&fromAddress=0xCd531e3904FE9e393e97E6f316008dA8e1516145&slippage=1&gasPrice=6&partialFillEnabled=false&gasLimit=800000').json()
                nonce = w3.eth.get_transaction_count("0xCd531e3904FE9e393e97E6f316008dA8e1516145")
                if int(trade['toTokenAmount']) - 6000000000 * int(trade["tx"]['gas']) - 6000000000*gas>500000000000000000:
                    trade["tx"]["nonce"] = nonce
                    trade["tx"]["gasPrice"] = Web3.toWei(trade["tx"]["gasPrice"], 'gwei')
                    trade["tx"]["value"] = Web3.toWei(trade["tx"]["value"], 'gwei')
                    trade["tx"]["to"] = "0x11111112542D85B3EF69AE05771c2dCCff4fAa26"
                    signed_txn = w3.eth.account.sign_transaction(trade["tx"], private_key=private_key)
                    tx = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    print(f'Swapped {trade["fromTokenAmount"]}BUSD for {trade["toTokenAmount"]} BNB, making a profit of {int(trade["toTokenAmount"])-500000000000000000}')
                    time.sleep(35)
                    Buy(500000000000000000)
                else:
                    continue
            except:
                print("Bad Request")
                traceback.print_exc()
                continue


Buy(500000000000000000)