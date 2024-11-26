import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from io import StringIO
import pytz  # For timezone handling

# Function to generate dynamic start and end dates
def generate_dates():
    today = datetime.now()
    start_date = today.strftime('%Y-%m-%d')
    end_date = (today + timedelta(days=14)).strftime('%Y-%m-%d')
    return start_date, end_date

# Function to convert datetime to the operational timezone
def create_datetime(date, hour, timezone):
    dt = pd.to_datetime(f"{date} {hour:02d}:00:00")
    return dt.tz_localize('UTC').tz_convert(timezone)

# Function to process the API response into separate DataFrames
def all_data_to_csv(df, timezone, timestamp):
    forecast_timestamp_utc = pd.to_datetime(timestamp)
    forecast_timestamp_opr = forecast_timestamp_utc.tz_localize('UTC').tz_convert(timezone)

    # Initialize DataFrames for solar, wind, and load
    solar = pd.DataFrame(columns=['published_at', 'utc_datetime', 'opr_datetime', 'opr_date', 'opr_hour', 'region_zone', 'solar_mw'])
    wind = pd.DataFrame(columns=['published_at', 'utc_datetime', 'opr_datetime', 'opr_date', 'opr_hour', 'region_zone', 'wind_mw'])
    load = pd.DataFrame(columns=['published_at', 'utc_datetime', 'opr_datetime', 'opr_date', 'opr_hour', 'region_zone', 'load_mw'])

    # Iterate over rows of the input DataFrame and process each one
    for _, row in df.iterrows():
        opr_datetime = create_datetime(row['date'], row['hour'] - 1, timezone) + timedelta(hours=1)
        utc_datetime = opr_datetime.tz_convert('UTC')
        opr_date = opr_datetime.date()
        opr_hour = opr_datetime.hour

        # Process each column and append to the appropriate DataFrame
        for col in df.columns:
            region_zone = col.split()[0]
            if 'AMP Solar Forecast' in col:
                new_data = {
                    'published_at': forecast_timestamp_opr,
                    'utc_datetime': utc_datetime,
                    'opr_datetime': opr_datetime,
                    'opr_date': opr_date,
                    'opr_hour': opr_hour,
                    'region_zone': region_zone,
                    'solar_mw': row[col]
                }
                solar = pd.concat([solar, pd.DataFrame([new_data])], ignore_index=True)
            elif 'AMP Wind Forecast' in col:
                new_data = {
                    'published_at': forecast_timestamp_opr,
                    'utc_datetime': utc_datetime,
                    'opr_datetime': opr_datetime,
                    'opr_date': opr_date,
                    'opr_hour': opr_hour,
                    'region_zone': region_zone,
                    'wind_mw': row[col]
                }
                wind = pd.concat([wind, pd.DataFrame([new_data])], ignore_index=True)
            elif 'AMP Forecast' in col:
                new_data = {
                    'published_at': forecast_timestamp_opr,
                    'utc_datetime': utc_datetime,
                    'opr_datetime': opr_datetime,
                    'opr_date': opr_date,
                    'opr_hour': opr_hour,
                    'region_zone': region_zone,
                    'load_mw': row[col]
                }
                load = pd.concat([load, pd.DataFrame([new_data])], ignore_index=True)

    return solar, wind, load

# Main function to handle the API calls and data processing
def main():
    opr_timezone = 'US/Eastern'  # Set the operational timezone
    all_data = pd.DataFrame()  # Initialize an empty DataFrame for all the data

    # Infinite loop to call the endpoint every 15 minutes
    while True:
        try:
            # Generate dynamic start and end dates
            start_date, end_date = generate_dates()

            # Prepare parameters for the API request
            params = {
                'startDate': start_date,
                'endDate': end_date,
                'zoneId': 'ALL',
            }

            # Make the API call
            resp = requests.get(
                'https://platform.amperon.co/export/iso/pjm/short-term/net-demand',
                params=params,
                auth=requests.auth.HTTPBasicAuth('UDePfCeIlA2lYJYR87V7jU7IoxbW0HyC', 'wn1V4TtuR0FjQsdaWi719D7erNpg8di0mBh4F24J2muvWv4lU7OxJ9TNrzgPkxnr'),
            )

            if resp.status_code == 200:
                try:
                    # Read the CSV response into a pandas DataFrame
                    all_data = pd.read_csv(StringIO(resp.text))
                    all_data.to_csv("pjm-parse.csv", index=False)

                    # Now, process the data using the all_data_to_csv function
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    solar, wind, load = all_data_to_csv(all_data, opr_timezone, timestamp)

                    solar.to_csv('solar_data.csv', index=False)
                    wind.to_csv('wind_data.csv', index=False)
                    load.to_csv('load_data.csv', index=False)

                    # Print results for verification
                    print("Solar Data:")
                    print(solar)
                    print("Wind Data:")
                    print(wind)
                    print("Load Data:")
                    print(load)

                except Exception as e:
                    print(f"Error parsing response: {e}")
            else:
                print(f"API call failed with status {resp.status_code}: {resp.text}")

        except Exception as e:
            print(f"An error occurred: {e}")

        # Wait for 15 minutes before making the next API call
        time.sleep(900)


# Run the main function if this script is executed directly
if __name__ == "__main__":
    main()
