from datetime import datetime
import streamlit as st
import pandas as pd
import numpy as np
from utils import *
from db import *
from styling import *
from dotenv import load_dotenv
import os
import google.generativeai as ggi

def main():
    
    # Set the page title and favicon
    st.set_page_config(page_title="The Data Bard", page_icon="📜", layout="wide")
    
    
    # App content
    st.title("Welcome to The Data Bard!")
    
    # Create two columns
    col1, col2, col3, col4, col5 = st.columns(5)
        
    if "name" not in st.session_state:
        st.session_state.name = "USER"
        
    if "show_password" not in st.session_state:
        st.session_state.show_password = False
        
    if "filterMap" not in st.session_state:
        st.session_state.filterMap = []
        
            
    # Report Options
    with col1:
        typeOfEvent = st.pills(
            "What type of event is happening?",
            ("FIRE", "DISEASE", "CRIME"),
        )
    
    # Size Options
    with col2:
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
    
    # Initialize session state if not set
    if "filterMap" not in st.session_state:
        st.session_state.filterMap = []
        
    # Mapping of icons to filter names
    icon_to_label = {
        ":material/local_fire_department:": "FIRE",
        ":material/coronavirus:": "DISEASE",
        ":material/local_police:": "CRIME",
    }

    # Display pills with icons
    selected_icons = st.pills(
        "Filter the Map",
        list(icon_to_label.keys()),  # Use icons as options
        selection_mode="multi"
    )

    # Convert selected icons to their corresponding labels
    st.session_state.filterMap = [icon_to_label[icon] for icon in selected_icons]
    
    
    
    df_user = pd.DataFrame(getLocation());
    df_reports = filteredReport(st.session_state.filterMap);
    
    
    if st.session_state.name == "USER":
        if not df_user.empty:
            latitude = df_user.loc[0, "latitude"]
            longitude = df_user.loc[0, "longitude"]
            with col3:
                st.button("Report", on_click=lambda: addReport(typeOfEvent, st.session_state.name, latitude, longitude, sizeOfEvent, now, False, False))

    
    df_center_reports = df_reports.copy(deep=True)
    df_area_reports = df_reports.copy(deep=True)
    df_center_reports['accuracy'] = 5
    df_center_reports["color"] = df_center_reports["type"].map(color_center_mapping).fillna(color_unknown)
    df_area_reports["color"] = df_area_reports["type"].map(color_area_mapping).fillna(color_unknown)
    
    df_points = pd.concat([df_user, df_center_reports], join='inner')
    df_points = pd.concat([df_points, df_area_reports], join='inner')
    
           
    # Draw the map
    st.map(df_points, latitude="latitude", longitude="longitude", size="accuracy", color="color")
    
    # Start the Gemini Chat Bot
    load_dotenv(".env")

    fetcheed_api_key = os.getenv("API_KEY")
    ggi.configure(api_key = fetcheed_api_key)

    model = ggi.GenerativeModel("gemini-2.0-flash") 
    chat = model.start_chat()

    def LLM_Response(question):
        response = chat.send_message(question,stream=True)
        return response

    st.header("Seek wisdom in the data’s tale—ask for guidance!")
    
    user_quest = st.text_input("Ask a question:")
    btn = st.button("Ask")
    
    preamble = """
                  You are a chat assistant for people in the 1300s. 
                  You provide insights on coordinate data linked to incidents including fires, disease breakouts, and crime reports.
                  Users can ask you questions about this data and it is your sole job to help them understand it.
                  Make sure to keep your responses simple and in the frame of someone from the 1300s.
                  You are not to have conversations about anything other interpreting data provided.
                  Please do not provide direct coordinates to the user, use the coordinates to link to modern day maps and give specific landmarks neardby.
                  Do not provide generate landmarks like "town square" or "highway", etc. please only provide real life places incidents take place near, if asked.
                  If you are providing landmarks of where incidents are happening, get them to be as close to the coordinates as possible. Preferably with an accuracy of 500 meters.
                  The data that you will be referencing is stores as a CSV file and is below, please use it all when providing help:
                  
                  """
                  
    epilogue = "\nHere is the question the user has: "
                  
    file_path = "data.csv"
    with open(file_path, "r", encoding="utf-8") as file:
        data_text = file.read()

    if btn and user_quest:
        result = LLM_Response(preamble + data_text + epilogue + user_quest)
        st.subheader("Response : ")
        for word in result:
            output = "".join(word.text for word in result)
        st.text(output)
    
    
if __name__ == "__main__":
    main()