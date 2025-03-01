import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from db import *

def main():
    
    # Define a mapping from type to hex color
    color_mapping = {
    "FIRE": color_fire_center,
    "DISEASE": color_disease_center,
    "CRIME": color_disease_center
    }
    
    st.button("Report")
    st.write("Button clicked!")
    
    df_user = getLocation();
    df_reports = getReports();
    df_reports["color"] = df_reports["type"].map(color_mapping).fillna(color_unknown)
    
    df_points = pd.concat([df_user, df_reports], join='inner')
    print(df_points)
       
    # current only shows the user
    st.map(df_points, latitude="latitude", longitude="longitude", size="accuracy", color="color")

    
    
if __name__ == "__main__":
    main()