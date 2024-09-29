import requests
import json
from console import google_places_api_key  # Importing your API key from console.py
import os
import time

def search_restaurants(lat, lng, radius):
    base_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    all_restaurants = []

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "restaurant",  # Searching specifically for restaurants
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
                    "address": place.get('vicinity', 'Unknown')
                }
                all_restaurants.append(restaurant)

                # Print each restaurant's name to verify progress
                print(f"Pulled data for: {restaurant['name']}")

            # Check if there's another page of results
            next_page_token = data.get('next_page_token')

            if next_page_token:
                # Ensure proper handling of the next page token
                time.sleep(6)  # Google imposes a small delay before retrieving the next page
                params = {
                    "pagetoken": next_page_token,
                    "key": google_places_api_key
                }
            else:
                break
        elif data['status'] == 'INVALID_REQUEST' and 'next_page_token' in data:
            # Retry after a delay in case the next_page_token is not immediately ready
            time.sleep(5)
            continue
        else:
            print(f"Error fetching places: {data['status']}")
            break

    # Save the list to a JSON file
    data_folder = os.path.join(os.getcwd(), "data")
    file_path = os.path.join(data_folder, "all_restaurants_list.json")

    with open(file_path, 'w') as json_file:
        json.dump(all_restaurants, json_file, indent=4)

    print(f"Complete list of restaurants saved to {file_path}")
    return all_restaurants

# Example usage
latitude = 45.689981
longitude = -122.569775
radius = 16093  # 10 miles in meters

all_restaurants_list = search_restaurants(latitude, longitude, radius)
