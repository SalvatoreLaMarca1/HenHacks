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
    color_mapping = {
        "FIRE": color_fire_center,
        "DISEASE": color_disease_center,
        "CRIME": color_disease_center
    }
    
    df_user = getLocation();
    df_reports = getReports();
    
    #st.button("Report", on_click=addReport(getReports(), typeOfEvent, user, df_user[0]["latitude"], df_user[0]["longitude"], sizeOfEvent, now, False, False))
    
    
    st.write("Button clicked!")
    
    
    df_reports["color"] = df_reports["type"].map(color_mapping).fillna(color_unknown)
    
    df_points = pd.concat([df_user, df_reports], join='inner')
    print(df_points)
       
    # current only shows the user
    st.map(df_points, latitude="latitude", longitude="longitude", size="accuracy", color="color")


    
    
    
if __name__ == "__main__":
    main()