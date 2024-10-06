import requests
import json
import os
import time
from console import google_places_api_key  # Importing your API key from console.py

# Function to load existing data (if any) and return set of existing place IDs
def load_existing_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        # Extract existing place_ids into a set for fast lookup
        existing_place_ids = {restaurant['place_id'] for restaurant in data}
        return data, existing_place_ids
    return [], set()

# Function to search for restaurants
def search_restaurants(lat, lng, radius, existing_place_ids, place_type="restaurant"):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    new_restaurants = []

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
                place_id = place.get('place_id')
                
                # Skip if this place_id is already in the dataset
                if place_id in existing_place_ids:
                    continue
                
                # Collect only new restaurants
                restaurant = {
                    "name": place.get('name', 'Unknown'),
                    "place_id": place_id,
                    "address": place.get('vicinity', 'Unknown'),
                    "latitude": place['geometry']['location']['lat'],
                    "longitude": place['geometry']['location']['lng']
                }
                new_restaurants.append(restaurant)

                # Add the new place_id to the set
                existing_place_ids.add(place_id)

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

    return new_restaurants

# Shift the search coordinates by a small amount to cover different areas
def shift_coordinates(lat, lng, lat_shift, lng_shift, radius, existing_place_ids, place_type):
    return search_restaurants(lat + lat_shift, lng + lng_shift, radius, existing_place_ids, place_type)

# Main logic to shift coordinates and run multiple searches 45.61608090821104, -122.4477018374083
latitude = 45.61608090821104
longitude = -122.4477018374083
radius = 3000  # 1 mile = 1609 meters

# Define the shifts (latitude and longitude)
lat_shifts = [0, 0.01, -0.01]  # Slightly shift up and down in latitude
lng_shifts = [0, 0.01, -0.01]  # Slightly shift left and right in longitude

# Load existing dataset
data_folder = os.path.join(os.getcwd(), "data")
existing_file_path = os.path.join(data_folder, "shifted_restaurants_list.json")
existing_data, existing_place_ids = load_existing_data(existing_file_path)

# Fetch new data using different coordinate shifts
all_results = existing_data  # Start with the existing data
for lat_shift in lat_shifts:
    for lng_shift in lng_shifts:
        print(f"Searching with shift (lat: {lat_shift}, lng: {lng_shift})")
        results = shift_coordinates(latitude, longitude, lat_shift, lng_shift, radius, existing_place_ids, "restaurant")
        all_results.extend(results)

# Save the updated data to a JSON file
file_path = os.path.join(data_folder, "shifted_restaurants_list.json")
with open(file_path, 'w') as json_file:
    json.dump(all_results, json_file, indent=4)

print(f"Complete list of unique restaurants saved to {file_path}")
