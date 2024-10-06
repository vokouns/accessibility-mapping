import requests
import json
import os
import time
from datetime import date
from console import google_places_api_key  # Importing your API key from console.py

def get_place_details(place_id):
    details_url = "https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,place_id,formatted_address,wheelchair_accessible_entrance,geometry",  # Add any other fields of interest
        "key": google_places_api_key
    }

    response = requests.get(details_url, params=params)
    details = response.json()

    # Check if the request was successful
    if response.status_code == 200 and details.get('status') == 'OK':
        return details.get('result', {})
    else:
        print(f"Error fetching details for Place ID: {place_id}, Status: {details.get('status')}")
        return {}

def fetch_accessibility_info(restaurants):
    detailed_restaurants = []
    place_ids_seen = set()  # Keep track of seen place_ids to avoid duplicates

    for restaurant in restaurants:
        place_id = restaurant['place_id']
        
        # Check if place_id has already been seen
        if place_id in place_ids_seen:
            print(f"Skipping duplicate restaurant: {restaurant['name']} (Place ID: {place_id})")
            continue  # Skip this restaurant if it's a duplicate

        print(f"Fetching details for: {restaurant['name']} (Place ID: {place_id})")

        details = get_place_details(place_id)

        if details:
            detailed_restaurant = {
                "name": details.get('name', 'Unknown'),
                "place_id": details.get('place_id', 'Unknown'),
                "formatted_address": details.get('formatted_address', 'Unknown'),
                "latitude": details.get('geometry', {}).get('location', {}).get('lat', 'Unknown'),
                "longitude": details.get('geometry', {}).get('location', {}).get('lng', 'Unknown'),
                "wheelchair_accessible_entrance": details.get('wheelchair_accessible_entrance', 'Unknown'),
                "wheelchair_accessible_parking": "Unknown",  # Placeholder for future data
                "wheelchair_accessible_restroom": "Unknown",  # Placeholder for future data
                "wheelchair_accessible_seating": "Unknown"  # Placeholder for future data
            }
            detailed_restaurants.append(detailed_restaurant)
            place_ids_seen.add(place_id)  # Add the place_id to the set of seen ids

        # Add a short delay to avoid exceeding API rate limits
        time.sleep(2)

    # Save the detailed data to a JSON file
    data_folder = os.path.join(os.getcwd(), "data")
    file_path = os.path.join(data_folder, f"{date.today()}_accessibility_restaurant_info.json")

    with open(file_path, 'w') as json_file:
        json.dump(detailed_restaurants, json_file, indent=4)

    print(f"Accessible restaurant info saved to {file_path}")
    return detailed_restaurants


# Load the previously saved results (e.g., from your shifted searches)
restaurants_list_path = os.path.join(os.getcwd(), "data", "shifted_restaurants_list.json")
with open(restaurants_list_path, 'r') as file:
    restaurants = json.load(file)

# Fetch detailed info, including accessibility
detailed_info = fetch_accessibility_info(restaurants)
