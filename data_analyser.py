# %%
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# %%
def filename_getter(dict_locations) : # --> list
    list_filenames = []
    for origin in dict_locations['listOrigin']:
            for destination in dict_locations['listDestination']:
                filename = f'{origin}_to_{destination}.json'
                list_filenames.append(filename)
    return list_filenames


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
                except:
                    pass
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
                'price':[]
         }
        if data[date] != None:
            for i in range(len(date)):
                sanitised_data[date]['no_trips'].append(len(data[date][i]["itineraries"][0]['segments']))
                sanitised_data[date]['currency'].append(data[date][i]['price']['currency'])

                sanitised_data[date]['price'].append(data[date][i]['price']['total'])

        sanitised_data[date]['price'] = np.array(sanitised_data[date]['price'], dtype = np.float32)
        

        print(sanitised_data[date]['price'])
    return sanitised_data


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


def function1(row):

    return row[0]



# %% 
if __name__ == '__main__':
    dict_locations={
    'listOrigin':['BHX'],
    'listDestination': ['IAS']
}
    list_filenames = filename_getter(dict_locations)
    #df = sanitisation(list_filenames[0])
    #print(df)
    dict_dfs = file_rotator(list_filenames)(sanitisation_2)
    print(dict_dfs['BHX_to_IAS'])

    fig, ax = plt.subplots(figsize = (12, 6))

    #ax.plot(dict_dfs['MAN_to_IAS'].index,dict_dfs['MAN_to_IAS']['price'])
    ax.plot(dict_dfs['BHX_to_IAS'].index,dict_dfs['BHX_to_IAS']['price'])


# %%

# %%
