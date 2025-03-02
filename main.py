from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from db import *

def main():
    
    if "name" not in st.session_state:
        st.session_state.name = "USER"
    if "show_password" not in st.session_state:
        st.session_state.show_password = False
        
    def toggle_state():
        if st.session_state.name == "USER":
            st.session_state.name = "KINGDOM"
            st.session_state.show_password = True
        else:
            st.session_state.name = "USER"
            st.session_state.show_password = False
    
    st.button(st.session_state.name, on_click=toggle_state)

    placeholder = st.empty()
    
    if st.session_state.show_password:
        password = placeholder.text_input("Password")
        
        
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
    
    
    if st.session_state.name == "USER":
        if not df_user.empty:
            latitude = df_user.loc[0, "latitude"]
            longitude = df_user.loc[0, "longitude"]
            st.button("Report", on_click=lambda: addReport(typeOfEvent, st.session_state.name, latitude, longitude, sizeOfEvent, now, False, False))
    
    if st.session_state.name == "KINGDOM" and password == "password":
        placeholder.empty()
        if not df_user.empty:
            latitude = df_user.loc[0, "latitude"]
            longitude = df_user.loc[0, "longitude"]
            st.button("Report", on_click=lambda: addReport(typeOfEvent, st.session_state.name, latitude, longitude, sizeOfEvent, now, False, False))
        
        else:
            # Handle the case where the DataFrame is empty (e.g., set default values or wait)
            latitude = None
            longitude = None
            print("Data is still loading, default values set.")
    

    
    # Check if the DataFrame is not empty before accessing the data
    # if not df_user.empty:
    #     latitude = df_user.loc[0, "latitude"]
    #     longitude = df_user.loc[0, "longitude"]
    #     st.button("Report", on_click=lambda: addReport(typeOfEvent, st.session_state.name, latitude, longitude, sizeOfEvent, now, False, False))
        
    # else:
    #     # Handle the case where the DataFrame is empty (e.g., set default values or wait)
    #     latitude = None
    #     longitude = None
    #     print("Data is still loading, default values set.")

    
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