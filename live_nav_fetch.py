import requests
import pandas as pd

def fetch_nav_data(scheme_code):
    """Fetches live NAV data from mfapi.in for a given scheme code."""
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Connecting to API: {url}...")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        print("Connection successful. Parsing JSON...")
        data = response.json()
        
        # Extract metadata
        meta = data.get("meta", {})
        print("-" * 40)
        print(f"Fund Name:  {meta.get('scheme_name')}")
        print(f"Fund House: {meta.get('fund_house')}")
        print(f"Category:   {meta.get('scheme_category')}")
        print("-" * 40)
        
        # Convert the historical data list into a Pandas DataFrame
        nav_data = data.get("data", [])
        df = pd.DataFrame(nav_data)
        
        print(f"\nTotal records retrieved: {df.shape[0]}")
        print("\nFirst 5 rows of NAV history:")
        print(df.head())
        
        # NEW CODE: Save the dataframe to a physical file
        output_path = f"data/raw/{scheme_code}_nav_history.csv"
        df.to_csv(output_path, index=False)
        print(f"\nSUCCESS: Data permanently saved to {output_path}")
        
        return df
    else:
        print(f"Error: Failed to fetch data. HTTP Status Code: {response.status_code}")
        return None

# Execute the function using the 5 target IDs from your task sheet
if __name__ == "__main__":
    key_schemes = ["119551", "120503", "118632", "120465", "120841"]
    
    for scheme in key_schemes:
        print(f"\nProcessing Scheme: {scheme}")
        fetch_nav_data(scheme)