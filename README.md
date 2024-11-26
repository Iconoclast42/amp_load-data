# 
Here's a sample README.md for your Python program, which processes load, solar, and wind data into a structured format. This README will describe the purpose, functionality, installation instructions, and usage of the program.

Data Processing for Load, Solar, and Wind Forecast
This Python program fetches forecast data from the Amperon API for PJM's short-term net demand. The program processes and organizes the data into three categories: Load, Solar, and Wind forecasts. It then saves the processed data to a CSV file and prints it to the console.

Features
Fetches data every 15 minutes using the Amperon API.
Processes forecast data for Solar, Wind, and Load (net demand) in PJM (or other ISO regions if modified).
Converts the data into a pandas DataFrame for easier analysis and storage.
Saves the processed data to a CSV file (pjm-parse.csv).
Includes functions to handle date and time localization for different time zones (Eastern Time).
Requirements
Python 3.6+ is recommended.
The following Python libraries are required:
requests
pandas
time
datetime
You can install these dependencies using pip:

bash
Copy code
pip install requests pandas
How It Works
Data Fetching: The script makes an API call to the Amperon endpoint, using dynamically generated dates (today and 14 days ahead) to pull short-term net demand data.

Data Processing: The fetched data is processed to extract forecast values for Solar, Wind, and Load. The data is then organized into separate DataFrames for each category.

Time Localization: The script handles the time conversion from the ISO time zone to the operating region's time zone (US/Eastern by default), converting to UTC time for consistency.

Saving Data: Once the data is processed, it is saved as a CSV file (pjm-parse.csv) and printed to the terminal for viewing.

Continuous Execution: The program is designed to run indefinitely, fetching and processing data every 15 minutes.

Usage
Clone the repository to your local machine or copy the Python script to your working directory.

Run the Python script using the following command:

bash
Copy code
python <your_script_name>.py
The script will start fetching data and processing it every 15 minutes.

The processed data will be saved to a file named pjm-parse.csv in the current directory, and printed to the terminal.

Example Output:
csv
Copy code
published_at,utc_datetime,opr_datetime,opr_date,opr_hour,region_zone,solar_mw
2024-11-26 12:00:00,2024-11-26 17:00:00,2024-11-26 12:00:00,2024-11-26,12,PJM,75.3
...
Data Structure
The output CSV will contain the following columns:

published_at: The timestamp when the forecast was published.
utc_datetime: The UTC time equivalent of the forecasted time.
opr_datetime: The operating time in the specified timezone (US/Eastern).
opr_date: The date of the forecast in the operating timezone.
opr_hour: The hour of the forecast in the operating timezone.
region_zone: The region (e.g., PJM).
solar_mw: The forecasted solar generation in MW (for solar data).
wind_mw: The forecasted wind generation in MW (for wind data).
load_mw: The forecasted load (net demand) in MW (for load data).
Notes
The script relies on the Amperon API, which requires API keys for authentication. You need valid credentials to use the API.
The script processes data from the AMP Solar Forecast, AMP Wind Forecast, and AMP Forecast columns in the API response.
The script runs in an infinite loop, fetching data every 15 minutes. You can stop it at any time by pressing Ctrl+C.
Example of Data Processing:
The script will handle the following columns (example):

Solar: Extract values from columns like AMP Solar Forecast PJM and save them under the solar_mw column.
Wind: Extract values from columns like AMP Wind Forecast PJM and save them under the wind_mw column.
Load: Extract values from columns like AMP Forecast PJM and save them under the load_mw column.
Example Data for a Region:
plaintext
Copy code
published_at       utc_datetime            opr_datetime        opr_date   opr_hour   region_zone   solar_mw   wind_mw   load_mw
2024-11-26 12:00   2024-11-26 17:00:00     2024-11-26 12:00    2024-11-26 12   PJM         75.3       5.6        1300
2024-11-26 12:00   2024-11-26 17:00:00     2024-11-26 12:00    2024-11-26 13   PJM         74.5       6.0        1320
License
This project is licensed under the MIT License - see the LICENSE file for details.

This README.md provides a basic description of your Python program and explains how it works and how to use it. Let me know if you need further adjustments or more details!
