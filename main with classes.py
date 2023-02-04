# %%
import requests 
import json
import API_details
import time
import concurrent.futures
import sys
from data_analyser import sanitisation

list_times = []

def timeit(list_times):
    def wrapper(func):
        def inner(*args, **kwargs):
            start = time.time()
            func(*args, **kwargs)
            end = time.time()
            print(end-start)
            list_times.append(end-start)
            #return list_times
        return inner
    return wrapper

# Returns the token used for making API calls
def get_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    payload=f'client_id={API_details.CLIENT_ID}&client_secret={API_details.CLIENT_SECRET}&grant_type=client_credentials'
    headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    response = json.loads(response.text)
    API_details.ACCESS_TOKEN = response['access_token'] 

# Makes an API call to return a json data about the flights on a specific date from the origin to destination
def get_data(origin, destination,departure, adults, children):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departure}&adults={adults}&children={children}&nonStop=false&max=250&currencyCode=GBP"

    #payload='origin=BHX&destination=IAS&departureDate=2023-05-02&adults=1&nonStop=False'
    payload = {}
    headers = {
  'Authorization': f'Bearer {API_details.ACCESS_TOKEN}',
  'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    
    data = json.loads(response.text)

    try:
        data = data['data']
        return data, departure
    except:
        print(data)
        #return data, departure

# Writes the json data retrieved from the API to a json file
def write_data(filename, data, departure):
    try: 
        with open(filename, 'r') as f:
            file_json = json.load(f)
    except: 
        pass

    with open(filename, 'w') as f:
        try:

            file_json[departure] = data
            print('adding dates to existing file')
        except Exception as err:
            print(err)
            try:
                temp_dict = {departure: data}
                #temp_dict = json.dumps(temp_dict)
                #print(temp_dict)
                file_json = temp_dict
                print('adding the flights for the first date')
            except Exception as err:
                print(err)
        json.dump(file_json, f, indent = 2)


#@timeit(list_times)
def rotate_location_and_date(dict_locations, monthList):
    months_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for origin in dict_locations['listOrigin']:
        for destination in dict_locations['listDestination']:

            filename = f'{origin}_to_{destination}.json'
            if type(monthList) == type([]) :
                monthStart = monthList[0]
                monthEnd = monthList[1]
                
            else:
                monthStart = monthList
                monthEnd = monthList
            for month in range(monthStart, monthEnd+1):
                month_dict={}
                if month< 10:
                    string_month = '0'+str(month)
                else:
                    string_month = month
                for day in range(1, months_list[month-1]+1):
                    if day < 10:
                        string_day = '0'+str(day)
                    else:
                        string_day = day

                    print(f"The date is {string_day}-{string_month}-2023")
                    print(f'THis is for {filename}')
                    print(''']
                    
                    
                    
                    ''')
                    data, departure = get_data(origin, destination, f'2023-{string_month}-{string_day}', '4', '0')
                    #write_data(filename, data, departure)
                    month_dict[departure] = data
                    print(sys.getsizeof(month_dict))
                    return month_dict



def rotate_date(origin, destination, monthList):
    filename = f'{origin}_to_{destination}.json'
    #checking whether the input contains a list of the start and end month or just one singular month to iterate over
    if type(monthList) == type([]) :
        monthStart = monthList[0]
        monthEnd = monthList[1]
        
    else:
        monthStart = monthList
        monthEnd = monthList

    months_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # Iterating over the month
    for month in range(monthStart, monthEnd+1):
        month_dict={}
        if month< 10:
            string_month = '0'+str(month)
        else:
            string_month = month

        #Iterating over each day of the month
        for day in range(1, months_list[month-1]+1):
            if day < 10:
                string_day = '0'+str(day)
            else:
                string_day = day

            print(f"The date is {string_day}-{string_month}-2023")
            print(f'THis is for {filename}')
            print(''']
            
            
            
            ''')
            data, departure = get_data(origin, destination, f'2023-{string_month}-{string_day}', '4', '0')
            #write_data(filename, data, departure)
            sanitisation_2(data)
            month_dict[departure] = data
            print(sys.getsizeof(month_dict))
        return month_dict, filename

# %%
if __name__ == '__main__':
    get_token()
    months = [2, 3, 4, 5, 6]
    dict_locations = {
        'listOrigin':['BHX', 'MAN'],
        'listDestination': ['IAS']
    }
    

    for origin in dict_locations['listOrigin']:
        for destination in dict_locations['listDestination']:


            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                #worker_list = [executor.submit(rotate_date, origin, destination, month) for month in months]
                worker_list = []
                for month in months:
                    worker_list.append(executor.submit(rotate_date, origin, destination, month))
                    time.sleep(0.5)

            
            for future in concurrent.futures.as_completed(worker_list):
                print(future.result())
                data, filename = future.result()
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
        

# %%

# %%
