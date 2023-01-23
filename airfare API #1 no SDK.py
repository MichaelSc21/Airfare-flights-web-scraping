
# %% 
import requests
import json
for i in range(3, 10):
    url = f"https://test.api.amadeus.com/v2/shopping/flight-offers?originLocationCode=BHX&destinationLocationCode=IAS&departureDate=2023-05-0{i}&adults=2&children=2&nonStop=false&max=250"

    payload='origin=BHX&destination=IAS&departureDate=2023-05-02&adults=1&nonStop=False'
    headers = {
  'Authorization': 'Bearer ',
  'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)


    data = json.loads(response.text)
    data = data['data']

    for flight in data:
        if float(flight['price']['total']) < 2000:
            print(flight['price']['total'])

    with open('airfare#1.json', 'a') as f:
        json.dump(data, f)


# %%
with open('airfare#1.json', 'r') as f:
    data = json.load(f)
# %%
