# Accessibility Mapping Project

## Project Overview

This project aims to create an accessibility mapping tool that focuses on gathering, displaying, and analyzing accessibility-related data for various businesses, starting with restaurants. The goal is to create a comprehensive and community-driven resource that provides information such as wheelchair-accessible entrances, restrooms, seating, and parking.

In its current state, the project pulls data from the Google Places API and processes accessibility information for restaurants, including wheelchair-accessible entrances. Future iterations will include crowdsourcing data from users to gather more granular accessibility information, such as accessible restrooms, seating, and parking.

## Features

### What We've Done So Far
- **Data Collection**: We’ve used the Google Places API to gather information about restaurants in specific geographic locations. For now, we’ve pulled information such as restaurant names, addresses, place IDs, latitude/longitude, and whether the business has a wheelchair-accessible entrance.
- **Data Processing**: The data has been structured into a pandas DataFrame and exported to JSON format for further use in mapping tools.
- **Manual Expansion**: Placeholders for additional accessibility data (wheelchair-accessible restrooms, parking, seating) have been added to the dataset. These fields are currently set to `"Unknown"`, to be updated manually or through future crowdsourcing.
- **APIs Utilized**: Data has been sourced via the Google Places API, with plans for future integration of crowdsourced input to enrich the dataset further.

### Future Plans
- **Mapping**: The next major step involves mapping the collected data using **Leaflet.js** and **D3.js** to visualize the locations and accessibility details on a dynamic map.
- **Crowdsourcing**: Future phases will include enabling users to contribute additional accessibility information. This will allow the community to provide real-time updates for missing data (such as accessible restrooms, seating, and parking).
- **Machine Learning**: The project may eventually leverage machine learning to analyze user-submitted photos or reviews to automatically classify accessibility features like ramps, accessible restrooms, or parking.
- **Expansion to More Cities**: Initially focused on Vancouver, WA, and its surrounding areas, the project will expand to other regions over time.

## Tools and Technologies

### APIs
- **Google Places API**: Used to fetch business information such as name, address, place ID, and wheelchair-accessible entrance data.

### Python Libraries/Dependencies
- **pandas**: For data manipulation and creating DataFrames from JSON data.
- **requests**: For making HTTP requests to the Google Places API.
- **os**: For handling file paths and directory creation.
- **json**: For working with JSON data formats.
- **datetime**: Used to generate filenames with the current date.

### Mapping Libraries
- **Leaflet.js**: Planned for mapping the data and displaying it visually on a web-based map.
- **D3.js**: Planned for future data visualizations and user interaction on the map.

## File Structure
- **`console.py`**: Contains API keys (ignored in version control for security).
- **`datasets/`**: Folder where all pulled data is stored in JSON format.
- **`static/`**: Contains subdirectories for `CSS` and `JS` files related to web mapping.
- **`README.md`**: Documentation and project overview.
- **`.gitignore`**: Specifies files that should not be tracked by Git, including API keys.

## Next Steps
When the project resumes, the primary focus will be on visualizing the collected data on a map using **Leaflet.js**. From there, we'll enhance the dataset by integrating crowdsourcing methods for collecting additional accessibility information and expanding to mobile platforms.

### Request for Collaboration: Mobile App Development
In the future, we aim to expand the accessibility mapping tool into a mobile app available on both **Android** and **iPhone** platforms. The app will allow users to contribute accessibility data directly from their devices, submit reviews, and access real-time maps showing wheelchair-friendly businesses.

We are currently seeking:
- **Developers** interested in creating native or cross-platform apps for Android and iOS.
- **UX/UI designers** to help ensure the app is intuitive and easy to use for all types of users.
- **Contributors** with experience in crowdsourcing platforms and community-driven applications.

If you’re interested in collaborating on the development of the mobile app or have expertise in these areas, please reach out.
