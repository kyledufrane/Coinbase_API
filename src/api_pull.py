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

from lazypredict.Supervised import LazyRegressor

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

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

def get_models(coins_dataframe):
    
    model_results=	{
    'HuberRegressor':0,
    'RANSACRegressor':0,
    'OrthogonalMatchingPursuitCV':0,
    'Lasso LassoLarsCV':0,
    'LarsCV':0,
    'LassoCV':0,
    'PoissonRegressor':0,
    'TransformedTargetRegressor':0,
    'Lars':0,
    'LinearRegression':0,
    'BayesianRidge':0,
    'Ridge':0,
    'LassoLarsIC':0,
    'PassiveAggressiveRegressor':0,
    'RidgeCV':0,
    'ExtraTreesRegressor':0,
    'LassoLars':0,
    'SGDRegressor':0,
    'GradientBoostingRegressor':0,
    'RandomForestRegressor':0,
    'BaggingRegressor':0,
    'KNeighborsRegressor':0,
    'LGBMRegressor':0,
    'HistGradientBoostingRegressor':0,
    'ElasticNetCV':0,
    'XGBRegressor':0,
    'DecisionTreeRegressor':0,
    'ElasticNet':0,
    'ExtraTreeRegressor':0,
    'AdaBoostRegressor':0,
    'OrthogonalMatchingPursuit':0,
    'TweedieRegressor':0,
    'GammaRegressor':0,
    'SVR':0,
    'NuSVR':0,
    'QuantileRegressor':0,
    'DummyRegressor':0,
    'GaussianProcessRegressor':0,
    'LinearSVR':0,
    'MLPRegressor':0,
    'KernelRidge':0}
    
    coins_models = {}
    
    for ids in coins_dataframe['id']:
        
        try:
    
            coin_data=load_history(ids)

            X = coin_data.drop('high', axis=1)
            y = coin_data['high']

            X_train, X_test, y_train, y_test = train_test_split(X,y, random_state=42)

            scaler = StandardScaler()

            X_train_scaled = scaler.fit_transform(X_train)

            X_test_scaled = scaler.transform(X_test)

            base_models = LazyRegressor()

            base_model = base_models.fit(X_train_scaled, X_test_scaled, y_train, y_test)

            coins_models[ids] = base_model[0].index

            for model in model_results.keys():

                if model == str(base_model[0].index):

                    model_results[model] += 1
        
        except:
            
            print(f'{ids} error')
            
            
    return model_results, coins_models

# --------------------------------------------------------------


