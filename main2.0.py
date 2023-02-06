# %%
import requests 
import json
import API_details
import time
import concurrent.futures
import sys
import importlib

import data_analyser
importlib.reload(data_analyser)


def get_token():
        url = "https://test.api.amadeus.com/v1/security/oauth2/token"

        payload=f'client_id={API_details.CLIENT_ID}&client_secret={API_details.CLIENT_SECRET}&grant_type=client_credentials'
        headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response = json.loads(response.text)
        API_details.ACCESS_TOKEN = response['access_token'] 


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
                print(data['errors'][0]['title'])
                return None, departure

def write_data(filename, data, departure=None):
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
                file_json = temp_dict
                print('adding the flights for the first date')
            except Exception as err:
                print(err)
        if departure==None:
            file_json = file_json|data
        json.dump(file_json, f, indent = 2)


def rotate_date(future = None, origin=None, destination=None, month=None, dayResume = 1):
        months_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        filename = f'{origin}_to_{destination}.json'
        if month< 10:
                string_month = '0'+str(month)
        else:
                string_month = month
        month_dict = {}
        dayEnd = dayResume + 11
        if dayEnd < months_list[month-1]+1:
                months_list[month-1] = dayEnd

        for day in range(dayResume, months_list[month-1]+1):
                if day < 10:
                        string_day = '0'+str(day)
                else:
                        string_day = day

                print(f"The date is {string_day}-{string_month}-2023")
                print(f'THis is for {filename}')
                print(''']
                
                
                
                ''')
                data, departure = get_data(origin, destination, f'2023-{string_month}-{string_day}', '4', '0')
                print(type(data))
                #write_data(filename, data, departure)
                #sanitised_data =data_analyser.sanitisation_2(data=data)
                month_dict[departure] = data
                print(sys.getsizeof(month_dict))
                
    
        return month_dict, filename, day+1
                        



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
                                worker_list = []
                                for month in months:
                                        worker_list.append(executor.submit(rotate_date, origin=origin, destination=destination, month=month))
                                        time.sleep(0.5)

                        
                        for future in concurrent.futures.as_completed(worker_list):
                                print(future.result())
                                # this is for days 1-11
                                month_dict, filename, dayResume = future.result()
                                write_data(filename=filename, data=month_dict)
                                # for days 12-23
                                future.add_done_callback(rotate_date(origin = origin, destination = destination, month = month, dayResume = dayResume))
                                write_data(filename=filename, month_dict=month_dict)
                                # for days 24- to end of month
                                write_data(filename=filename, month_dict=month_dict)
                                future.add_done_callback(rotate_date(origin = origin, destination = destination, month = month, dayResume = dayResume))
                




# %%
