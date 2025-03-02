from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from db import *

def main():
    
    # Report Options
    typeOfEvent = st.pills(
        "What type of event is happening?",
        ("FIRE", "DISEASE", "CRIME"),
    )
    
    # Size Options
    sizeOfEvent = st.pills(
        "What is the size of the event?",
        ("SMALL", "MEDIUM", "LARGE")
    )
    
    # Switch to number values
    match sizeOfEvent:
        case "SMALL":
            sizeOfEvent = 20
        case "MEDIUM":
            sizeOfEvent = 50
        case "LARGE":
            sizeOfEvent = 80
    
    user = "USER"
    now = datetime.now()
    
    
    # Define a mapping from type to hex color
    color_center_mapping = {
    "FIRE": color_fire_center,
    "DISEASE": color_disease_center,
    "CRIME": color_crime_center
    }
    
    color_area_mapping = {
    "FIRE": color_fire_area,
    "DISEASE": color_disease_area,
    "CRIME": color_crime_area
    }
    
    df_user = pd.DataFrame(getLocation());
    df_reports = getReports();
    

    
    # Check if the DataFrame is not empty before accessing the data
    if not df_user.empty:
        latitude = df_user.loc[0, "latitude"]
        longitude = df_user.loc[0, "longitude"]
        st.button("Report", on_click=lambda: addReport(typeOfEvent, user, latitude, longitude, sizeOfEvent, now, False, False))
        
    else:
        # Handle the case where the DataFrame is empty (e.g., set default values or wait)
        latitude = None
        longitude = None
        print("Data is still loading, default values set.")

    
    df_center_reports = df_reports.copy(deep=True)
    df_area_reports = df_reports.copy(deep=True)
    df_center_reports['accuracy'] = 5
    df_center_reports["color"] = df_center_reports["type"].map(color_center_mapping).fillna(color_unknown)
    df_area_reports["color"] = df_area_reports["type"].map(color_area_mapping).fillna(color_unknown)
    
    df_points = pd.concat([df_user, df_center_reports], join='inner')
    df_points = pd.concat([df_points, df_area_reports], join='inner')
           
    # current only shows the user
    st.map(df_points, latitude="latitude", longitude="longitude", size="accuracy", color="color")
    
    # Add theming
    #def local_css(file_name):
    #    with open(file_name) as f:
    #        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # local_css("medievel-theme.css")


    
    
    
if __name__ == "__main__":
    main()