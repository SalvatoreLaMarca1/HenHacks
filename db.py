import pandas as pd
import os

file_path = "./data.csv"

# Check if file exists and is not empty
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    df = pd.read_csv(file_path)
else:
    # Create a new DataFrame with proper headers
    df = pd.DataFrame(columns=["type", "reported_by", "latitude", "longitude", "time", "resolved", "verified"])

def addReport(df, type, reported_by, latitude, longitude, accuracy, time, resolved, verified):
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
    df.to_csv(file_path, index=False)
    return df

def getReports():
    return df

#df = addReport(df, "FIRE", "KINGDOM", 39.3, 38.2, "2024-22-08", True, True)
