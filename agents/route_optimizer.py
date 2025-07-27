import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_ors_api_key(state: dict = None) -> str:
    # Priority: passed via state > .env > streamlit secrets
    return (
        (state or {}).get("ors_api_key") or
        os.getenv("ORS_API_KEY") or
        st.secrets.get("ORS_API_KEY", "")
    )

def geocode_location(location: str, ors_api_key: str):
    if not ors_api_key:
        raise ValueError("OpenRouteService API key is missing.")

    url = "https://api.openrouteservice.org/geocode/search"
    params = {
        "api_key": ors_api_key,
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
    ors_api_key = get_ors_api_key(state)

    if not to_location:
        return {
            "route": "❌ Destination missing in parsed order.",
            "distance_km": 0.0,
            "duration_minutes": 0.0,
            "route_coords": []
        }

    from_coords = geocode_location(from_location, ors_api_key)
    to_coords = geocode_location(to_location, ors_api_key)

    if not from_coords or not to_coords:
        return {
            "route": f"❌ Could not geocode location: {to_location}",
            "distance_km": 0.0,
            "duration_minutes": 0.0,
            "route_coords": []
        }

    headers = {
        "Authorization": ors_api_key,
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
