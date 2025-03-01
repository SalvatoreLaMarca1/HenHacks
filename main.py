import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from db import *

def main():
    
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
    
    st.button("Report")
    st.write("Button clicked!")
    
    df_user = getLocation();
    df_reports = getReports();
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

    
    
if __name__ == "__main__":
    main()