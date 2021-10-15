# --------------------------------------------------------------
# API & Data Cleaning library
# --------------------------------------------------------------

# Import libaries needed for functions

import requests
import hmac
import hashlib
import time
import cbpro
import pickle
import json

import pandas as pd
import matplotlib.pyplot as plt

from requests.auth import AuthBase

# --------------------------------------------------------------

def historic_data(coin_country):
    
    public_client = cbpro.PublicClient()
    
    history = pd.DataFrame(data = public_client.get_product_historic_rates(coin_country),
                            columns = ['time', 'low', 'high', 'open', 'close', 'volume' ])
    
    pickle_out = open(f'coin_history/{coin_country}.csv', 'wb')
    
    pickle.dump(history, pickle_out)
    
    return None

# --------------------------------------------------------------

def save_all_historic_coin_data(coins_dataframe):
    
    for ids in coins_dataframe['id']:
        
        try:
            
            historic_data(ids)
        
        except:
            
            print(f'{ids} error')
    
    return 'Coin History Completed'

# --------------------------------------------------------------

def load_history(coin):
    
    pickle_in = open(f"coin_history/{coin}.csv","rb")
    
    coin_history = pickle.load(pickle_in)
    
    return coin_history

# --------------------------------------------------------------

def get_keys(path):
    
    with open(path) as f:
        
        return json.load(f)
    
# --------------------------------------------------------------

def plot_coin_over_time(coin):
    
    history = load_history(coin)
    
    fig, ax = plt.subplots()
    
    ax.plot(history['time'], history['high'], color = 'green', label='high')
    
    ax.plot(history['time'], history['low'], color = 'red', label='low')
    
    plt.legend()
    
    plt.title(coin)
    
    plt.show()
    
    return None

# --------------------------------------------------------------
