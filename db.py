import pandas as pd
import os

filepath = "./data.csv"

def addReport(type, reported_by, latitude, longitude, accuracy, time, resolved, verified):
    df = pd.DataFrame(openCSV(filepath))
    
    # Create a new row as a dictionary
    new_row = pd.DataFrame([{
        "type": type,
        "reported_by": reported_by,
        "latitude": latitude,
        "longitude": longitude,  # Remove negation unless it's intentional
        "accuracy": accuracy,
        "time": time,
        "resolved": resolved,
        "verified": verified
    }])
    
    # Append the new row to the DataFrame
    df = pd.concat([df, new_row], ignore_index=True)    
    # Write the updated DataFrame to CSV with headers
    df.to_csv(filepath, index=False)
    return df

def filteredReport(filterMap):
    
    # Load CSV into a DataFrame
    df = pd.read_csv(filepath)

    # Ensure the 'type' column exists
    # if "type" not in df.columns:
    #     return pd.DataFrame()  # Return empty DataFrame if 'type' is missing

    # Filter rows based on selected letters
    if filterMap:
        df = df[df["type"].isin(filterMap)]
        
    
        
    return df  # Return the filtered DataFrame
    

def getReports():
    df = pd.DataFrame(openCSV(filepath))
    return df

def openCSV(filepath):
    # Check if file exists and is not empty
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        df = pd.read_csv(filepath)
    else:
        # Create a new DataFrame with proper headers
        df = pd.DataFrame(columns=["type", "reported_by", "latitude", "longitude", "time", "resolved", "verified"])
    return df

