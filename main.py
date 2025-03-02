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
    
    
    # Start the Gemini Chat Bot
    load_dotenv(".env")

    fetcheed_api_key = os.getenv("API_KEY")
    ggi.configure(api_key = fetcheed_api_key)

    model = ggi.GenerativeModel("gemini-2.0-flash") 
    chat = model.start_chat()

    def LLM_Response(question):
        response = chat.send_message(question,stream=True)
        return response

    st.title("Ask for help with understanding the data!")

    user_quest = st.text_input("Ask a question:")
    btn = st.button("Ask")
    
    preamble = """
                  Your first task is to 
    
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
                  
    epilogue = "\nHere is the question the user has:"
                  
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