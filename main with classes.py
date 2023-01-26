# %%
import requests 
import json
import API_details
import time

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
    print(data)
    
    with open('airfare#1.json', 'r') as f:
        try:
            file_json = json.load(f)
        except: 
            pass

    with open('airfare#1.json', 'w') as f:
        
        data = data['data']
        try:

            file_json[departure] = data
            print('file is empty')
        except Exception as err:
            print(err)
            try:
                temp_dict = {departure: data}
                #temp_dict = json.dumps(temp_dict)
                print(temp_dict)
                file_json = temp_dict
                print('adding the flights for the first date')
            except Exception as err:
                print(err)


        json.dump(file_json, f, indent = 2)
    print(file_json)

@timeit(list_times)
def iterate_date(listOrigin, listDestination):
    for origin in listOrigin:
        for destination in listDestination:
            for i in range(1, 30):
                if i < 10:
                    i = '0'+str(i)
                print(i)
                get_data(origin, destination, f'2023-05-{i}', '4', '0')


# %%
if __name__ == '__main__':

    #get_token()
    listOrigin = ['BHX', 'MAN']
    listDestination = ['IAS']
    
    iterate_date(listOrigin, listDestination)
# %%
