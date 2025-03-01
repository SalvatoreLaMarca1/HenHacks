import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

def main():
    st.button("Report")
    st.write("Button clicked!") 
    
    # Center coordinates
    lat_center = 34.15060042487772
    lon_center = -118.47614745730962

    # Number of random points
    num_points = 50

    # Generate small random offsets (using a normal distribution)
    lat_offsets = np.random.normal(loc=0, scale=0.01, size=num_points)
    lon_offsets = np.random.normal(loc=0, scale=0.01, size=num_points)

    # Calculate new coordinates
    lats = lat_center + lat_offsets
    lons = lon_center + lon_offsets

    # Create DataFrame
    data = pd.DataFrame({
        'lat': lats,
        'lon': lons
    })

    
    st.map(data)

    
    
if __name__ == "__main__":
    main()