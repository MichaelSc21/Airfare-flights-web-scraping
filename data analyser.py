# %%
import json
import pandas as pd
import numpy as np



# %%
def sanitisation():
    with open('airfare#1.json', 'r') as f:
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

data = sanitisation()
df = pd.DataFrame.from_dict(data, orient='index')
# %%
type(['price'])
# %%
count = 0
for i, j in df.iterrows():
    print(count)
    count+= 1
    print(type(i))
# %%

def function1(row):

    return row[0]


df['price'] = df.apply(lambda row: np.min(row[2]), axis = 1)
df['currency'] =  df['currency'].apply(lambda row: function1(row))
# %%
df
# %%
