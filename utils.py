import streamlit as st
import pandas as pd
import streamlit_js_eval as st_js

# Define Colors for Map Dots
color_user_center = "#FFFFFFFF"
color_user_area = "#FFFFFF50"

color_fire_center = "#FF5927FF"
color_fire_area = "#FF592750"

color_disease_center = "#8EB904FF"
color_disease_area = "#8EB90450"

color_crime_center = "#445B82FF"
color_crime_area = "#445B8250"

color_unknown = "#dedede30"

# Get users current location
def getLocation():
    """
    Returns the user's location as a dictionary with keys 'lat' and 'lon'.
    The user will be prompted by their browser to share their location.
    """
    location = st_js.get_geolocation()
    if location:  
        df = pd.DataFrame(
        [{  # SIZE OF USER CENTER
            "latitude": location['coords']["latitude"],
            "longitude": location['coords']["longitude"],
            "accuracy": 5,
            "color": color_user_center,
        },
        {   # SIZE OF USER SURROUNDING CIRCLE
            "latitude": location['coords']["latitude"],
            "longitude": location['coords']["longitude"],
            "accuracy": location['coords']['accuracy'],
            "color": color_user_area,
             
        }])
        return df
    else:
        st.error("Could not retrieve location. Make sure location services are enabled.")
        return None
    
    
