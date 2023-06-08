################################################################################
# make these imports into a set of requirements (see above)
################################################################################

import requests
import pandas as pd
import pytz
import json
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup

################################################################################
# set and create some variables
################################################################################

# Coordinates for [location]: 
latitude = '55.951009'
longitude = '-3.100191'

# Set the start date to current date:
start_date = date.today()

################################################################################
# function to fetch sunrise and sunset data
################################################################################

def fetch_sunrise_sunset_data(date_str):
    """Fetch sunrise and sunset times from API."""
    url = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date_str}&formatted=0'
    response = requests.get(url)

    # Return JSON data if request is successful, else print error and return None
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching sunrise/sunset data: {response.status_code}")
        return None

################################################################################
# function to convert times to local
################################################################################

def convert_to_bst(time_str):
    """Convert GMT time string to BST."""
    gmt = pytz.timezone('GMT')
    bst = pytz.timezone('Europe/London')
    gmt_time = datetime.fromisoformat(time_str).replace(tzinfo=gmt)
    bst_time = gmt_time.astimezone(bst)
    return bst_time.strftime('%H:%M')

################################################################################
# use the functions to fetch times for one week
################################################################################

sun_data = []

for i in range(7):
    # Calculate the date for each day in the range
    current_date = start_date + timedelta(days=i)
    date_str = current_date.isoformat()

    # Fetch sunrise and sunset data for the current date
    sun_info = fetch_sunrise_sunset_data(date_str)

    # If data is successfully fetched, convert times to BST and add to sun_data
    if sun_info and 'results' in sun_info:
        sun_data.append({
            'date': date_str,
            'sunrise': convert_to_bst(sun_info['results']['sunrise']),
            'sunset': convert_to_bst(sun_info['results']['sunset'])
        })
    else:
        print(f"No sun data fetched for date: {date_str}")

################################################################################
# put the data in a dataframe
################################################################################

df = pd.DataFrame(sun_data)

################################################################################
# use the date column as the index
################################################################################

df.set_index('date', inplace=True)

# convert the index to datetime
df.index = pd.to_datetime(df.index)

# create a new column for the day of the week
df['day_of_week'] = df.index.day_name()

# Define the new order of the columns with 'day_of_week' at the beginning
column_order = ['day_of_week', 'sunrise', 'sunset']

# Reorder the DataFrame
df = df[column_order]

url = 'https://www.tidetime.org/europe/united-kingdom/portobello.htm'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table in the soup.
table = soup.find('table', {'id': 'tideTable'})

# Find all the table rows in the table.
rows = table.find_all('tr')

# Initialize an empty list to hold the data.
data = []

# Initialize a counter for the day of the week.
day = 0

# Loop through each row.
for row in rows:
    # Find all the table data cells in the row.
    cells = row.find_all('td')

    # Loop through each cell.
    for cell in cells:
        # Increment the day counter.
        day += 1

        # Find all the high and low tides in the cell.
        tides = cell.find_all('li', {'class': ['highTide', 'lowTide']})

        # Loop through each tide.
        for tide in tides:
            # Get the tide type, time and height from the tide text.
            tide_type = tide.find('span', {'class': 'tidal-state'}).text
            tide_time = tide.find('strong').text.replace(tide_type, '').strip()
            tide_height = tide.text.split(')')[0].split('(')[-1]

            # Add the day, tide type, time and height to the data list.
            data.append([day, tide_type, tide_time, tide_height])

# Convert the data list into a DataFrame.
df_tides = pd.DataFrame(data, columns=['Day', 'Tide Type', 'Tide Time', 'Tide Height'])

df_tides.drop('Tide Type', axis=1, inplace=True)