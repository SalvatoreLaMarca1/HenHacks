import streamlit as st
import pandas as pd
import numpy as np
from utils import *

def main():
    st.button("Report")
    st.write("Button clicked!") 
    
    df_user = getLocation();
    
    # current only shows the user
    st.map(df_user, latitude="latitude", longitude="longitude", size="size", color="color")

    
    
if __name__ == "__main__":
    main()