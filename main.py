from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from db import *

def main():
    
    user = ""
    
    typeOfEvent = st.pills(
        "What type of event is happening?",
        ("FIRE", "DISEASE", "CRIME"),
    )
    
    sizeOfEvent = st.pills(
        "What is the size of the event?",
        ("SMALL", "MEDIUM", "LARGE")
    )
    
    st.write("Type:", typeOfEvent)
    st.write("Size: ", sizeOfEvent)
    
    now = datetime.now()
    
    st.write(now)
    
    
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
    
    df_user = getLocation();
    df_reports = getReports();
    
    #st.button("Report", on_click=addReport(getReports(), typeOfEvent, user, df_user[0]["latitude"], df_user[0]["longitude"], sizeOfEvent, now, False, False))
    
    
    st.write("Button clicked!")
    
    df_center_reports = df_reports.copy(deep=True)
    df_area_reports = df_reports.copy(deep=True)
    df_center_reports['accuracy'] = 5
    df_center_reports["color"] = df_center_reports["type"].map(color_center_mapping).fillna(color_unknown)
    df_area_reports["color"] = df_area_reports["type"].map(color_area_mapping).fillna(color_unknown)
    
    df_points = pd.concat([df_user, df_center_reports], join='inner')
    df_points = pd.concat([df_points, df_area_reports], join='inner')
    
    print(df_points)
       
    # current only shows the user
    st.map(df_points, latitude="latitude", longitude="longitude", size="accuracy", color="color")
    
    # Add theming
    #def local_css(file_name):
    #    with open(file_name) as f:
    #        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    # local_css("medievel-theme.css")


    
    
    
if __name__ == "__main__":
    main()