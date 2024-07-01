import json
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import itertools


geolocator = Nominatim(user_agent="job_recommendation_system")

def get_coordinates(city_name):
    print(f"Attempting to fetch coordinates for {city_name}")
    time.sleep(1)  #this is to respect API usage policy
    location = geolocator.geocode(city_name)
    if location:
        print(f"Coordinates for {city_name}: (Lat: {location.latitude}, Long: {location.longitude})")
        return (location.latitude, location.longitude)
    else:
        print(f"No coordinates found for {city_name}")
        return (None, None)

def compute_distances(cities):
    city_coordinates = {}
    print("Initializing geocoding of cities...")
    for city in cities:
        city_coordinates[city] = get_coordinates(city)

    distances = {}
    print("Initializing distance calculations between cities...")
    for (city1, coordinate1), (city2, coordinate2) in itertools.combinations(city_coordinates.items(), 2):
        if None not in (coordinate1, coordinate2):
            distance = geodesic(coordinate1, coordinate2).miles
            key1 = f"{city1.lower().replace(' ', '_')}_{city2.lower().replace(' ', '_')}"
            key2 = f"{city2.lower().replace(' ', '_')}_{city1.lower().replace(' ', '_')}"
            distances[key1] = distance
            distances[key2] = distance
            print(f"Distance between {city1} and {city2}: {distance} miles")
    return distances

cities = [
    "Montgomery, AL", "Birmingham, AL", "Huntsville, AL",
    "Anchorage, AK", "Fairbanks, AK", "Juneau, AK",
    "Phoenix, AZ", "Tucson, AZ", "Mesa, AZ",
    "Little Rock, AR", "Fayetteville, AR", "Fort Smith, AR",
    "Los Angeles, CA", "San Francisco, CA", "San Diego, CA",
    "Denver, CO", "Colorado Springs, CO", "Aurora, CO",
    "Hartford, CT", "New Haven, CT", "Stamford, CT",
    "Dover, DE", "Wilmington, DE", "Newark, DE",
    "Tallahassee, FL", "Miami, FL", "Orlando, FL",
    "Atlanta, GA", "Savannah, GA", "Augusta, GA",
    "Honolulu, HI", "Hilo, HI", "Kailua, HI",
    "Boise, ID", "Idaho Falls, ID", "Nampa, ID",
    "Chicago, IL", "Springfield, IL", "Peoria, IL",
    "Indianapolis, IN", "Fort Wayne, IN", "Evansville, IN",
    "Des Moines, IA", "Cedar Rapids, IA", "Davenport, IA",
    "Topeka, KS", "Wichita, KS", "Overland Park, KS",
    "Frankfort, KY", "Louisville, KY", "Lexington, KY",
    "Baton Rouge, LA", "New Orleans, LA", "Shreveport, LA",
    "Augusta, ME", "Portland, ME", "Lewiston, ME",
    "Annapolis, MD", "Baltimore, MD", "Rockville, MD",
    "Boston, MA", "Worcester, MA", "Springfield, MA",
    "Lansing, MI", "Detroit, MI", "Grand Rapids, MI",
    "Saint Paul, MN", "Minneapolis, MN", "Rochester, MN",
    "Jackson, MS", "Gulfport, MS", "Biloxi, MS",
    "Jefferson City, MO", "Kansas City, MO", "Saint Louis, MO",
    "Helena, MT", "Billings, MT", "Missoula, MT",
    "Lincoln, NE", "Omaha, NE", "Bellevue, NE",
    "Carson City, NV", "Las Vegas, NV", "Reno, NV",
    "Concord, NH", "Manchester, NH", "Nashua, NH",
    "Trenton, NJ", "Newark, NJ", "Jersey City, NJ",
    "Santa Fe, NM", "Albuquerque, NM", "Las Cruces, NM",
    "Albany, NY", "New York, NY", "Buffalo, NY",
    "Raleigh, NC", "Charlotte, NC", "Greensboro, NC",
    "Bismarck, ND", "Fargo, ND", "Grand Forks, ND",
    "Columbus, OH", "Cleveland, OH", "Cincinnati, OH",
    "Oklahoma City, OK", "Tulsa, OK", "Norman, OK",
    "Salem, OR", "Portland, OR", "Eugene, OR",
    "Harrisburg, PA", "Philadelphia, PA", "Pittsburgh, PA",
    "Providence, RI", "Warwick, RI", "Cranston, RI",
    "Columbia, SC", "Charleston, SC", "Greenville, SC",
    "Pierre, SD", "Sioux Falls, SD", "Rapid City, SD",
    "Nashville, TN", "Memphis, TN", "Knoxville, TN",
    "Austin, TX", "Houston, TX", "Dallas, TX",
    "Salt Lake City, UT", "Provo, UT", "West Valley City, UT",
    "Montpelier, VT", "Burlington, VT", "Rutland, VT",
    "Richmond, VA", "Virginia Beach, VA", "Norfolk, VA",
    "Olympia, WA", "Seattle, WA", "Spokane, WA",
    "Charleston, WV", "Huntington, WV", "Morgantown, WV",
    "Madison, WI", "Milwaukee, WI", "Green Bay, WI",
    "Cheyenne, WY", "Casper, WY", "Laramie, WY"
]

#The distances are computed
saved_distances = compute_distances(cities)

# Saved in JSON format for re use
with open('geocoding_values.json', 'w') as f:
    json.dump(saved_distances, f)

print("All distances between cities have been cached in the current directory successfully.")
