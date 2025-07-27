# import os
# import requests
# import json


# def optimize_route(state: dict) -> dict:
#     from_location = "Mumbai"
#     to_location = state["parsed_order"]["destination"]

#     # Dummy coordinates (replace with real geocoding in production)
#     city_coords = {
#         "Mumbai": [72.8777, 19.0760],
#         "Hyderabad": [78.4867, 17.3850]
#     }

#     from_coords = city_coords.get(from_location)
#     to_coords = city_coords.get(to_location)

#     if not from_coords or not to_coords:
#         return {"route": "Location not found.", "distance_km": 0.0, "duration_minutes": 0.0}

#     headers = {
#         "Authorization": os.environ.get("ORS_API_KEY"),
#         "Content-Type": "application/json"
#     }

#     url = "https://api.openrouteservice.org/v2/directions/driving-car"
#     body = {
#         "coordinates": [from_coords, to_coords]
#     }

#     response = requests.post(url, json=body, headers=headers)
#     data = response.json()

#     if "routes" in data:
#         route_info = data["routes"][0]
#         summary = route_info.get("summary", {})
#         distance_km = summary.get("distance", 0) / 1000  # meters to km
#         duration_minutes = summary.get("duration", 0) / 60  # seconds to minutes

#         return {
#             "route": "Route optimized successfully.",
#             "distance_km": distance_km,
#             "duration_minutes": duration_minutes
#         }
#     else:
#         return {
#             "route": "Route optimization failed.",
#             "distance_km": 0.0,
#             "duration_minutes": 0.0
#         }


# import os
# import requests

# def geocode_location(location: str):
#     url = "https://api.openrouteservice.org/geocode/search"
#     params = {
#         "api_key": os.environ.get("ORS_API_KEY"),
#         "text": location,
#         "size": 1
#     }
#     response = requests.get(url, params=params)
#     data = response.json()

#     if data.get("features"):
#         return data["features"][0]["geometry"]["coordinates"]
#     return None

# def optimize_route(state: dict) -> dict:
#     from_location = "Mumbai"
#     to_location = state["parsed_order"]["destination"]

#     from_coords = geocode_location(from_location)
#     to_coords = geocode_location(to_location)

#     if not from_coords or not to_coords:
#         return {"route": "Location not found.", "distance_km": 0.0, "duration_minutes": 0.0}

#     headers = {
#         "Authorization": os.environ.get("ORS_API_KEY"),
#         "Content-Type": "application/json"
#     }

#     url = "https://api.openrouteservice.org/v2/directions/driving-car"
#     body = {
#         "coordinates": [from_coords, to_coords]
#     }

#     response = requests.post(url, json=body, headers=headers)
#     data = response.json()

#     if "routes" in data:
#         summary = data["routes"][0].get("summary", {})
#         distance_km = summary.get("distance", 0) / 1000
#         duration_minutes = summary.get("duration", 0) / 60

#         return {
#             "route": f"Optimized route from {from_location} to {to_location}.",
#             "distance_km": round(distance_km, 2),
#             "duration_minutes": round(duration_minutes, 2)
#         }
#     else:
#         return {
#             "route": "Route optimization failed.",
#             "distance_km": 0.0,
#             "duration_minutes": 0.0
#         }


# import os
# import requests
# import streamlit as st
# # Load OpenRouteService API Key from environment or Streamlit secrets
# from dotenv import load_dotenv
# load_dotenv()


# ORS_API_KEY = os.getenv("ORS_API_KEY", st.secrets.get("ORS_API_KEY", ""))

# def geocode_location(location: str):
#     url = "https://api.openrouteservice.org/geocode/search"
#     params = {
#         "api_key": ORS_API_KEY,
#         "text": location,
#         "size": 1
#     }
#     response = requests.get(url, params=params)
#     data = response.json()

#     if data.get("features"):
#         return data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
#     return None

# def optimize_route(state: dict) -> dict:
#     from_location = "Mumbai"
#     to_location = state["parsed_order"]["destination"]

#     from_coords = geocode_location(from_location)
#     to_coords = geocode_location(to_location)

#     if not from_coords or not to_coords:
#         return {
#             "route": "Location not found.",
#             "distance_km": 0.0,
#             "duration_minutes": 0.0,
#             "route_coords": []
#         }

#     headers = {
#         "Authorization": ORS_API_KEY,
#         "Content-Type": "application/json"
#     }

#     url = "https://api.openrouteservice.org/v2/directions/driving-car"
#     body = {
#         "coordinates": [from_coords, to_coords]
#     }

#     response = requests.post(url, json=body, headers=headers)
#     data = response.json()

#     if "routes" in data:
#         summary = data["routes"][0].get("summary", {})
#         geometry = data["routes"][0].get("geometry", {})

#         distance_km = summary.get("distance", 0) / 1000
#         duration_minutes = summary.get("duration", 0) / 60

#         # Optional: decode full path (but we'll use start-end only for now)
#         route_coords = [
#             {"lon": from_coords[0], "lat": from_coords[1]},
#             {"lon": to_coords[0], "lat": to_coords[1]}
#         ]

#         return {
#             "route": f"Optimized route from {from_location} to {to_location}.",
#             "distance_km": round(distance_km, 2),
#             "duration_minutes": round(duration_minutes, 2),
#             "route_coords": route_coords
#         }
#     else:
#         return {
#             "route": "Route optimization failed.",
#             "distance_km": 0.0,
#             "duration_minutes": 0.0,
#             "route_coords": []
#         }


import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Load OpenRouteService API Key securely
ORS_API_KEY = os.getenv("ORS_API_KEY", st.secrets.get("ORS_API_KEY", ""))

def geocode_location(location: str):
    if not ORS_API_KEY:
        raise ValueError("OpenRouteService API key is missing. Set it in .env or Streamlit secrets.")

    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ORS_API_KEY,
        "text": location,
        "size": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("features"):
            return data["features"][0]["geometry"]["coordinates"]  # [lon, lat]

    except Exception as e:
        print(f"❌ Geocoding failed for location '{location}': {e}")

    return None

def optimize_route(state: dict) -> dict:
    from_location = "Mumbai"
    to_location = state.get("parsed_order", {}).get("destination", "")

    if not to_location:
        return {
            "route": "❌ Destination missing in parsed order.",
            "distance_km": 0.0,
            "duration_minutes": 0.0,
            "route_coords": []
        }

    from_coords = geocode_location(from_location)
    to_coords = geocode_location(to_location)

    if not from_coords or not to_coords:
        return {
            "route": f"❌ Could not geocode location: {to_location}",
            "distance_km": 0.0,
            "duration_minutes": 0.0,
            "route_coords": []
        }

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json"
    }

    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    body = {
        "coordinates": [from_coords, to_coords]
    }

    try:
        response = requests.post(url, json=body, headers=headers, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "routes" in data:
            summary = data["routes"][0].get("summary", {})
            distance_km = summary.get("distance", 0) / 1000
            duration_minutes = summary.get("duration", 0) / 60

            route_coords = [
                {"lon": from_coords[0], "lat": from_coords[1]},
                {"lon": to_coords[0], "lat": to_coords[1]}
            ]

            return {
                "route": f"Optimized route from {from_location} to {to_location}.",
                "distance_km": round(distance_km, 2),
                "duration_minutes": round(duration_minutes, 2),
                "route_coords": route_coords
            }

    except Exception as e:
        print(f"❌ Route optimization failed for {to_location}: {e}")

    return {
        "route": "❌ Route optimization failed due to API or input error.",
        "distance_km": 0.0,
        "duration_minutes": 0.0,
        "route_coords": []
    }
