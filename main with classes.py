# %%
import requests 
import json
import API_details
from importlib import reload
reload(API_details)
print(API_details.ACCESS_TOKEN)

def get_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    payload=f'client_id={API_details.CLIENT_ID}&client_secret={API_details.CLIENT_SECRET}&grant_type=client_credentials'
    headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)




def get_data(origin, destination,departure, adults, children):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departure}&adults={adults}&children={children}&nonStop=false&max=250"

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
    with open('airfare#1.json', 'w+') as f:
        
        data = data['data']
        print(data)
        print(type(data))
        try:
            
            #file_json = json.load(f)
            try:
                file_json[departure].append(data)
                print('appended new flights to existing date')
            except Exception as err:
                print('adding flights to a new date')
                print(err)
                file_json[departure] = data
                print('done')
        except Exception as e:
            print(e)
            print('creating a file in the first place')
            del data[0]
            file_json = {departure: data}
        json.dump(file_json, f, indent = 2)
    return data

data = get_data('BHX', 'IAS', '2023-05-05', '4', '0')
# %%
get_token()
# %%
print(data)
# %%
