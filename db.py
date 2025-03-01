import pandas as pd

# Read CSV without headers

df = pd.read_csv("./data.csv")  # Use header=None instead of header=""

print(df.columns)

def addReport(df, type, reported_by, lat, lon, time, resolved, verified):
    new_row = {"type": type, "reported_by": reported_by, "lat": lat, "lon":-lon, "time": time,"resolved": resolved, "verified": verified}
    
    new_row_df = pd.DataFrame([new_row])
    
    df = pd.concat([df, new_row_df])
    
    
    df.to_csv("./data.csv")

df = addReport(df, "FIRE", "KINGDOM", 39.3, 38.2, "2024-22-08", True, True)