import requests
import json
import os
import time
from console import google_places_api_key  # Importing your API key from console.py

def search_restaurants(lat, lng, radius, place_type="restaurant"):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    all_restaurants = []

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,  # Allowing the place type to be passed as an argument
        "key": google_places_api_key
    }

    while True:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data['status'] == 'OK':
            places = data.get('results', [])
            for place in places:
                restaurant = {
                    "name": place.get('name', 'Unknown'),
                    "place_id": place.get('place_id'),
                    "address": place.get('vicinity', 'Unknown'),
                    "latitude": place['geometry']['location']['lat'],
                    "longitude": place['geometry']['location']['lng']
                }
                all_restaurants.append(restaurant)

                # Print progress
                print(f"Pulled data for: {restaurant['name']}")

            # Check if there's another page of results
            next_page_token = data.get('next_page_token')

            if next_page_token:
                # Delay before fetching the next page to avoid API limits
                time.sleep(2)
                params = {
                    "pagetoken": next_page_token,
                    "key": google_places_api_key
                }
            else:
                break
        else:
            print(f"Error fetching places: {data['status']}")
            break

    return all_restaurants

# Shift the search coordinates by a small amount to cover different areas
def shift_coordinates(lat, lng, lat_shift, lng_shift, radius, place_type):
    return search_restaurants(lat + lat_shift, lng + lng_shift, radius, place_type)

# Main logic to shift coordinates and run multiple searches
latitude = 45.6346
longitude = -122.6731
radius = 1600  # 1 mile = 1609 meters

# Define the shifts (latitude and longitude)
lat_shifts = [0, 0.01, -0.01]  # Slightly shift up and down in latitude
lng_shifts = [0, 0.01, -0.01]  # Slightly shift left and right in longitude

# Fetch data using different coordinate shifts
all_results = []
for lat_shift in lat_shifts:
    for lng_shift in lng_shifts:
        print(f"Searching with shift (lat: {lat_shift}, lng: {lng_shift})")
        results = shift_coordinates(latitude, longitude, lat_shift, lng_shift, radius, "restaurant")
        all_results.extend(results)

# Remove duplicates by 'place_id'
unique_restaurants = {restaurant['place_id']: restaurant for restaurant in all_results}
unique_results = list(unique_restaurants.values())

# Save the results to a JSON file
data_folder = os.path.join(os.getcwd(), "data")
file_path = os.path.join(data_folder, "shifted_restaurants_list.json")

with open(file_path, 'w') as json_file:
    json.dump(unique_results, json_file, indent=4)

print(f"Complete list of unique restaurants saved to {file_path}")
