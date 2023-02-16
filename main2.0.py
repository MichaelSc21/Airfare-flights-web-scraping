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

# It gets the data from the API in a JSON format
# The JSON text returned is composed of an object for a date entered--> to multiple lists where each list contains the data for each flight
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

def write_data_2(filename, month_dict):
    try: 
        with open(filename, 'r') as f:
            file_json = json.load(f)
            file_json = file_json | month_dict
    except Exception as e:
        print(e) 
        file_json = month_dict
    with open(filename, 'w') as f:
        json.dump(file_json, f, indent=2, sort_keys=True)

def write_data(filename, data, departure):
	# this is meant to add the data for each individual day to the file
	# this is a task which I/O bound I believe
	# that is the reason I am creating def write_data_in_chunks
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

	json.dump(file_json, f, indent = 2)



def write_data_in_chunks(filename, data):
	# this is meant to write a dictionary that has quite a few elemnts to a file 
	# it writes to the file a dictionary of the data of different dates rather than one singular date like def write_data does
	try: 
		with open(filename, 'r') as f:
			file_json = json.load(f)
	except: 
		pass

	with open(filename, 'w') as f:
		try:
			file_json = file_json|data
		except Exception as err:
			print(err)
			file_json = data
		json.dump(file_json, f, indent = 2)

# this function is meant to be used as a generator for get_data()
# it iterates over each day in a month up to a certain day, this will be called the period
# By default, period will be greater than the number of days in any month because the function will automatically result in using the length of the month as the period


def rotate_date(origin=None, destination=None, month=None, dayResume = 1, period=40):
	month_dict = {}
	months_list = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	filename = f'{origin}_to_{destination}.json'
	if month< 10:
		string_month = '0'+str(month)
	else:
		string_month = month

	dayEnd = dayResume + period
	if dayEnd > months_list[month-1]+1:
		#print('We are using the period, not the limit of the month')
		dayEnd =months_list[month-1] +1

	for day in range(dayResume, dayEnd):
		if day < 10:
			string_day = '0'+str(day)
		else:
			string_day = day

		#print(f"The date is {string_day}-{string_month}-2023")
		#print(f'THis is for {filename}')

		data, departure = get_data(origin, destination, f'2023-{string_month}-{string_day}', '4', '0')
		#print(type(data))
		#write_data(filename, data, departure)
		#sanitised_data =data_analyser.sanitisation_2(data=data)
		# Use this sanitised_data with write_data_2 rather than anything else
		month_dict[departure] = data
		#print(sys.getsizeof(month_dict))
		
	return month_dict, filename, day+1
			



# %%
if __name__ == '__main__':
	get_token()
	months = [3, 4, 5, 6, 7, 8, 9]
	dict_locations = {
		'listOrigin':['BHX'],
		'listDestination': ['IAS']
	}
	

	for origin in dict_locations['listOrigin']:
		for destination in dict_locations['listDestination']:
			period =11

			with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
				dayResume = 1
				
				for _ in range(3):
					print(f"The dayResume is: {dayResume}")
					print("""
				
				
					""")
					worker_list = []
					for month in months:
						worker_list.append(executor.submit(rotate_date, origin=origin, destination=destination, month=month,dayResume=dayResume, period = period))
						time.sleep(0.5)

				
					for future in concurrent.futures.as_completed(worker_list):
						# this is for days 1-11
						month_dict, filename, dayResume = future.result()
						write_data_in_chunks(filename=filename, data=month_dict)
			



## %%

# %%
