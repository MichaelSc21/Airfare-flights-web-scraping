# %%
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# %%
def sanitisation(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    sanitised_data = {}

    for date in data:
        sanitised_data[date]={
                'no_trips':[],
                'currency':[],
                'price':[]
         }
        for i in range(len(date)):


            
            sanitised_data[date]['no_trips'].append(len(data[date][i]["itineraries"][0]['segments']))
            sanitised_data[date]['currency'].append(data[date][i]['price']['currency'])

            sanitised_data[date]['price'].append(data[date][i]['price']['total'])

        
        sanitised_data[date]['price'] = np.array(sanitised_data[date]['price'], dtype = np.float32)
        

        print(sanitised_data[date]['price'])
        """sanitised_data = {
                'date': data[date][i]["itineraries"][0]['segments'][0]['departure']['at'],
                'no_trips': len(data[date][i]["itineraries"][0]['segments']),
                'curreny': data[date][i]['price']['currency'],
                'price': data[date][i]['price']['total'],

        }"""
    return sanitised_data

def function1(row):

    return row[0]


# %%
dict_dfs={}
if __name__ == '__main__':
    listOrigin = ['BHX', 'MAN']
    listDestination = ['IAS']
    dict_dfs={}
    for origin in listOrigin:
        for destination in listDestination:
            filename = f'{origin}_to_{destination}.json'
            data = sanitisation(filename)
            df = pd.DataFrame.from_dict(data, orient='index')
            df.index = pd.to_datetime(df.index)
            dict_dfs[filename[:-5]] = df
            df['price'] = df.apply(lambda row: np.min(row[2]), axis = 1)
            df['currency'] =  df['currency'].apply(lambda row: function1(row))
# %%
print(dict_dfs)
fix, ax = plt.subplots(figsize= (12, 6))
for df in dict_dfs.values():
    print(df)
    ax.plot(df.index, df['price'])

