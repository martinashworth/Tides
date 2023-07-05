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


# Fetch tide data
tide_data = fetch_tide_data(TIDE_URL)
cdate = date.today()

# Loop over each day's tide data
for each_day in tide_data:
    # Fetch and print sunrise and sunset times
    sunrise, sunset = get_sun_times(cdate)
    print(f"{cdate.strftime('%A')} - Sunrise: {sunrise} - Sunset: {sunset}")

    # Find and print each tide time and type
    tides = each_day.find_all('li', {'class': ['highTide', 'lowTide']})
    for tide in tides:
        tide_time = tide.find('strong').text.split(' ')[1]
        tide_type = tide.find('span', {'class': 'tidal-state'}).text
        print(f"{tide_time} - {tide_type}")

    # Advance to the next day
    cdate = cdate + timedelta(days=1)
    print()
