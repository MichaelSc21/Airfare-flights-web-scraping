# %%
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit


# %%
def filename_getter(dict_locations) : # --> list
    list_filenames = []
    for origin in dict_locations['listOrigin']:
            for destination in dict_locations['listDestination']:
                filename = f'{origin}_to_{destination}.json'
                list_filenames.append(filename)
    return list_filenames

def sanitisation_2(filename=None, data=None):
    if data==None:
        return None
    sanitised_data={
                'no_trips':[],
                'currency':[],
                'price':[]
         }
    for i in range(len(data)):
        sanitised_data['no_trips'].append(len(data[i]["itineraries"][0]['segments']))
        sanitised_data['currency'].append(data[i]['price']['currency'])
        sanitised_data['price'].append(data[i]['price']['total'])

    #sanitised_data['price'] = np.array(sanitised_data['price'], dtype = np.float32)
        

    #print(sanitised_data['price'])
    return sanitised_data

def file_rotator(list_filenames, dict_dfs ={}):
    def wrapper(func):
        def creating_dfs(*args, **kwargs):
            for filename in list_filenames:
                data = func(filename)
                df = pd.DataFrame.from_dict(data, orient='index')
                df.index = pd.to_datetime(df.index)
                dict_dfs[filename[:-5]] = df
                try:
                    df['price'] = df.apply(lambda row: np.min(row[2]), axis = 1)
                    df['currency'] =  df['currency'].apply(lambda row: function1(row))
                except Exception as err:
                    print(err)
                    df['price'] = np.nan
            return dict_dfs
        return creating_dfs()
    return wrapper

def sanitisation(filename=None, data=None):
    if filename != None:
        with open(filename, 'r') as f:
            data = json.load(f)
        sanitised_data = {}

    for date in data:
        sanitised_data[date]={
                'no_trips':[],
                'currency':[],
                'price':np.empty(0).astype(np.float32)
         }
        if data[date] != None:
            for i in range(len(date)):
                no_trips = len(data[date][i]["itineraries"][0]['segments'])
                currency = data[date][i]['price']['currency']
                price = np.float32(data[date][i]['price']['total'])

                sanitised_data[date]['no_trips'].append(no_trips)
                sanitised_data[date]['currency'].append(currency)
                sanitised_data[date]['price'] = np.append(sanitised_data[date]['price'], price)
        else:
            sanitised_data[date]['no_trips'] = np.nan
            sanitised_data[date]['currency'] = np.nan
            sanitised_data[date]['price'] = np.nan

    return sanitised_data



def sort_out_currency_and_trips(row):
    try:
        return row[0]
    except:
        return np.nan

def sort_out_price(row):
    try:
        return np.min(row)
    except Exception as err:
        print(err)
        print(row)

def creating_dfs(list_filenames, data):
    for filename in list_filenames:
        df = pd.DataFrame.from_dict(data, orient='index')
        df.index = pd.to_datetime(df.index)
        dict_dfs[filename[:-5]] = df
        try:
            df['currency'] =  df['currency'].apply(lambda row: sort_out_currency_and_trips(row))
            df['no_trips'] =  df['no_trips'].apply(lambda row: sort_out_currency_and_trips(row))
        except Exception as err:
            print(err)
        try:
            df['price'] = df['price'].apply(lambda row: sort_out_price(row))
        except Exception as err:
            df['price'] = np.nan
            print(err)
        
            
    return dict_dfs



def model_f(x, a, b, c, d, e):
    return  a*x**2 + b*x + c

    
def plot_graph(x, y):
    mask1 = ~x.isnull()
    mask2 = ~y.isnull()
    x = x[mask2 & mask1]
    y = y[mask1 & mask2]
    # I use this for curve fitting becuase the curve fit doesn't take in data in the format of dates as a parameter
    # therefore, I use the number of seconds since 1970 on my x axis for my curve fitting
    x_numerical = (x - pd.Timestamp("1970-01-01")) // pd.Timedelta('1s')
    print(x_numerical)
    popt, pcov = curve_fit(model_f, x_numerical, y)
    y_data = model_f(x_numerical, *popt)

    print(popt)

    #a, b = np.polyfit(x_numerical, y, 1)

    fig, ax = plt.subplots(figsize = (12, 6))
   
    ax.plot(x, y_data, color='red')
    ax.scatter(x, y, marker='o')
    ax.legend(['Total price of a flight from BHX to IAS for 4 people'])


# %% 
if __name__ == '__main__':
    dict_locations={
    'listOrigin':['BHX'],
    'listDestination': ['IAS']
}
    list_filenames = filename_getter(dict_locations)
    data = sanitisation(list_filenames[0])

    dict_dfs = creating_dfs(list_filenames, data)

    fig, ax = plt.subplots(figsize = (12, 6))

    #ax.plot(dict_dfs['MAN_to_IAS'].index,dict_dfs['MAN_to_IAS']['price'])
    plot_graph(dict_dfs['BHX_to_IAS'].index, dict_dfs['BHX_to_IAS']['price'])
    ax.scatter(dict_dfs['BHX_to_IAS'].index,dict_dfs['BHX_to_IAS']['price'])

# %%

# %%
print(sys.getsizeof(dict_dfs['BHX_to_IAS']))
dict_dfs['BHX_to_IAS']

# %%
