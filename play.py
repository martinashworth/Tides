import requests
import pytz
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup

# Constants for the coordinates, timezone and URLs
LATITUDE = '55.951009'
LONGITUDE = '-3.100191'
SUN_API_BASE_URL = 'https://api.sunrise-sunset.org/json'
TIMEZONE = 'Europe/London'
TIDE_URL = 'https://www.tidetime.org/europe/united-kingdom/portobello.htm'


def get_request(url):
    """
    Perform a GET request to a given URL.
    Raise an exception if the request fails, and terminate the program.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        exit(1)


def fetch_tide_data(tide_url):
    """
    Fetch the tide data from the given URL.
    Parse the HTML and extract the desired table data.
    """
    tide_response = get_request(tide_url)
    soup = BeautifulSoup(tide_response.text, 'html.parser')
    tide_table = soup.find('table', {'id': 'tideTable'})
    tr_results = tide_table.find_all('tr')   # type: ignore
    columns = tr_results[1].find_all('td')
    return columns


def fetch_sun_data(cdate, lat, long):
    """
    Fetch the sunrise and sunset data for a given date and location.
    """
    url = f'{SUN_API_BASE_URL}?lat={lat}&lng={long}&date={cdate}&formatted=0'
    response = get_request(url)
    return response.json()


def format_sun_time(sun_time):
    """
    Convert time string from sunrise-sunset API to string in local time.
    """
    dt = datetime.fromisoformat(sun_time).astimezone(pytz.timezone(TIMEZONE))
    return dt.strftime('%H:%M')


def get_sun_times(cdate):
    """
    Fetch sunrise and sunset times for a given date, return as strings.
    """
    sun_data = fetch_sun_data(cdate, LATITUDE, LONGITUDE)
    sunrise = format_sun_time(sun_data['results']['sunrise'])
    sunset = format_sun_time(sun_data['results']['sunset'])
    return sunrise, sunset


###############################################################################
# Weather - Make an API call to fetch the hourly temperature data
###############################################################################

url = f'https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=temperature_2m,weathercode&timezone=GMT'
response = requests.get(url)
weather = response.json()   # supplied as a dictionary with hourly data
hourly_data = weather['hourly']
# print(hourly_data.keys())
temperature_2m = hourly_data['temperature_2m']
weathercode = hourly_data['weathercode']
timestamps = hourly_data['time']

# print(timestamps)
# print(len(timestamps))

daily_temperatures = {}

for i, temp in enumerate(temperature_2m):
    dt = datetime.fromisoformat(timestamps[i])
    date_str = dt.strftime('%Y-%m-%d')
    hour = dt.hour
    # print(i, temp, hour)

# ################################################################################
# # Consider daytime hours between 6 AM and 6 PM
# ################################################################################

    if 8 <= hour < 20:
        if date_str not in daily_temperatures:
            daily_temperatures[date_str] = {'total_temp': 0, 'count': 0, 'weathercode': weathercode[i]}
            print(daily_temperatures)
        daily_temperatures[date_str]['total_temp'] += temp
        daily_temperatures[date_str]['count'] += 1

print(daily_temperatures)

# ################################################################################
# # Calculate the average daytime temperature
# ################################################################################

#     for date_str in daily_temperatures:
#         total_temp = daily_temperatures[date_str]['total_temp']
#         count = daily_temperatures[date_str]['count']
#         average_temp = total_temp / count
#         daily_weathercode = daily_temperatures[date_str]['weathercode']
        
################################################################################
# print(f"{date_str}: {average_temp:.1f}°C, weathercode: {daily_weathercode}")
################################################################################
###############################################################################
# the following works fine
###############################################################################
# # Fetch tide data
# tide_data = fetch_tide_data(TIDE_URL)
# cdate = date.today()

# # Loop over each day's tide data
# for each_day in tide_data:
#     # Fetch and print sunrise and sunset times
#     sunrise, sunset = get_sun_times(cdate)
#     print(f"{cdate.strftime('%A')} - Sunrise: {sunrise} - Sunset: {sunset}")

#     # Find and print each tide time and type
#     tides = each_day.find_all('li', {'class': ['highTide', 'lowTide']})
#     for tide in tides:
#         tide_time = tide.find('strong').text.split(' ')[1]
#         tide_type = tide.find('span', {'class': 'tidal-state'}).text
#         print(f"{tide_time} - {tide_type}")

#     # Advance to the next day
#     cdate = cdate + timedelta(days=1)
#     print()

