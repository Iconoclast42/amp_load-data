# Load, Solar, and Wind Data Processing

This Python program fetches short-term net demand forecast data for the PJM ISO (Independent System Operator) from the Amperon API. The data includes **load**, **solar**, and **wind** forecasts. The program processes the data and exports it into CSV files for further analysis.

---

## Features

- **Dynamic Date Range**: Automatically generates today's date and a date 14 days later to fetch data.
- **Scheduled API Calls**: Makes API calls every 15 minutes to retrieve updated forecasts.
- **CSV Export**: Saves the processed data into structured CSV files.
- **Data Categories**:
  - **Load Forecast**: Energy load predictions by region and hour.
  - **Solar Forecast**: Solar power generation predictions by region and hour.
  - **Wind Forecast**: Wind power generation predictions by region and hour.

---

## Prerequisites

To run this program, you need the following:

1. Python 3.8 or higher
2. Required Python libraries:
   - `pandas`
   - `requests`
   - `time`
   - `datetime`
   - `io`
3. Access to the Amperon API with valid credentials:
   - API username: `ID`
   - API password: `secret`

---

## Installation

1. Clone the repository to your local machine:
   ```bash
   git clone [https://github.com/your-username/your-repo.git](https://github.com/Iconoclast42/amp_load-data.git)
   cd your-repo
