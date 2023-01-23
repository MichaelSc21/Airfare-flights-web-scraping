# %%
import requests 
import json
from API_details import ACCESS_TOKEN, API_SECRET, API_KEY

def get_data(origin, destination,departure, adults, children):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode={origin}&destinationLocationCode={destination}&departureDate={departure}&adults={adults}&children={children}&nonStop=false&max=250"

    #payload='origin=BHX&destination=IAS&departureDate=2023-05-02&adults=1&nonStop=False'
    headers = {
  'Authorization': f'Bearer {ACCESS_TOKEN}',
  'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


    data = json.loads(response.text)

    with open('airfare#1.json', 'a') as f:
        json.dump(data, f)


get_data('BHX', 'IAS', '2023-05-02', '2', '2')