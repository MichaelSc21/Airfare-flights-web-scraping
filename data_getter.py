# %%
import requests 
import json
import API_details
import time
import concurrent.futures
import sys
import importlib

import data_analyser
importlib.reload(API_details)

# %%

class api_caller_one_way_tickets(object):
    def __init__(self, origin=None, destination=None, adults=0, children=0, months=None):
        # Maybe add a timer to check when it was the last time the token had been fetched from the server

        url = "https://test.api.amadeus.com/v1/security/oauth2/token"

        payload=f'client_id={API_details.CLIENT_ID}&client_secret={API_details.CLIENT_SECRET}&grant_type=client_credentials'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        response = json.loads(response.text)
        self.ACCESS_TOKEN = response['access_token'] 
        print(self.ACCESS_TOKEN)
        self.origin = origin
        self.destination = destination
        self.adults = adults
        self.children = children
        self.months = months
        self.filename = f'{self.origin}_to_{self.destination}.json'

    # this is meant to write a dictionary that has quite a few elemnts to a file 
    # it writes to the file a dictionary of the data of different dates rather than one singular date like def write_data does

    def write_data_in_chunks(self, data):

        try: 
            with open(self.filename, 'r') as f:
                file_json = json.load(f)
        except: 
            pass

        with open(self.filename, 'w') as f:
            try:
                file_json = file_json|data
            except Exception as err:
                print(err)
                file_json = data
            json.dump(file_json, f, indent = 2)


    def using_threads(self,max_workers = 3, period=11, loop_over=3):
        with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
            self.dayResume = 1
            
            for _ in range(loop_over):
                print(f"The dayResume is: {self.dayResume}")
                print("""
            
            
                """)
                worker_list = []
                class_list = []
                for month in range(len(self.months)):
                    #creating instances of a class
                    class_list.append(each_month(self.ACCESS_TOKEN))
                    #using the methods of the instances of the class
                    worker_list.append(executor.submit(class_list[month].
                    rotate_date, origin=self.origin, destination=self.destination, month=self.months[month],dayResume=self.dayResume, period = period))
                    time.sleep(0.5)

            
                for future in concurrent.futures.as_completed(worker_list):
                    # this is for days 1-11
                    month_dict, self.dayResume = future.result()
                    self.write_data_in_chunks(data=month_dict)
        

class each_month():
    def __init__(self, ACCESS_TOKEN):
        self.ACCESS_TOKEN = ACCESS_TOKEN

    def get_data(self, origin, destination, departure, adults, children):
        url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departure}&adults={adults}&children={children}&nonStop=false&max=250&currencyCode=GBP"

        #payload='origin=BHX&destination=IAS&departureDate=2023-05-02&adults=1&nonStop=False'
        payload = {}
        headers = {
        'Authorization': f'Bearer {self.ACCESS_TOKEN}',
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


    # this function is meant to be used as a generator for get_data()
    # it iterates over each day in a month up to a certain day, this will be called the period
    # By default, period will be greater than the number of days in any month because the function will automatically result in using the length of the month as the period
    def rotate_date(self, origin=None, destination=None, month=None, dayResume = 1, period=40):
        # Make sure you add a weak referrence here for the month_dict


        # afsag
        # make sure you use an official library for the date and month
        month_dict = {}
        months_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        if month< 10:
            string_month = '0'+str(month)
        else:
            string_month = month

        dayEnd = dayResume + period
        if dayEnd > months_list[month-1]+1:
            dayEnd =months_list[month-1] +1
        print(f'The month is {month}')
        for day in range(dayResume, dayEnd):
            if day < 10:
                string_day = '0'+str(day)
            else:
                string_day = day

            print(f"The date is {string_day}-{string_month}-2023")
            #print(f'THis is for {filename}')

            data, departure = self.get_data(origin, destination, f'2023-{string_month}-{string_day}', '4', '0')
            #sanitised_data =data_analyser.sanitisation_2(data=data)
            # Use this sanitised_data with write_data_2 rather than anything else
            month_dict[departure] = data
            
        return month_dict, day+1



# %%
if __name__ == '__main__':
    months = [3, 4, 5, 6, 7, 8, 9]
    max_workers = 3
    period = 11
    loop_over = 3
    object1 = api_caller_one_way_tickets('MAN', 'IAS', adults =4, children = 0, months = months)
    object1.using_threads(max_workers, period, loop_over)


# %%
