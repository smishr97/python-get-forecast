from pathlib import Path
from geopy.geocoders import Nominatim
import requests
import pandas as pd

def CityNotFoundError( ):
  print("Latitude and Longitude for this city does not exist")


def search_for_tonight( forecast ):
    return [element for element in forecast if element['name'] == 'Tonight']


def get_forecast( city='Pittsburgh' ):
    '''
    Returns the nightly's forecast for a given city.

    Inputs:
    city (string): A valid string

    Output:
    period (dictionary/JSON): a dictionary containing at least, the forecast keys startTime, endTime and detailedForecast.

    Throws:
    CityNotFoundError if geopy returns empty list or if the latitude longitude fields are empty.

    ForecastUnavailable if the period is empty or the API throws any status code that is not 200

    Hint:
    * Return the period that is labeled as "Tonight"
    '''

    geolocator = Nominatim(user_agent='Shivam Mishra')
    try: 
        location = geolocator.geocode(city)
    except: 
        raise CityNotFoundError()
    
    if location==None:
      return CityNotFoundError()

    # use the latitude and longitude to get the weather forecast
    URL = f'https://api.weather.gov/points/{location.latitude},{location.longitude }'
    response = requests.get(URL)
    response = response.json()
    
    forecast_url = response['properties']['forecast']
    response_2 = requests.get(forecast_url).json()

    forecast = response_2['properties']['periods']
    forecast_tonight = search_for_tonight(forecast)
    startTime, endTime, detailedForecast = forecast_tonight[0]['startTime'], forecast_tonight[0]['endTime'], forecast_tonight[0]['detailedForecast']

    return {'startTime':startTime, 'endTime':endTime, 'detailedForecast':detailedForecast}
    raise NotImplementedError()

 
def main():
    period = get_forecast()

    file = 'weather.pkl'

    if Path(file).exists():
        df = pd.read_pickle( file )
    else:
        df = pd.DataFrame(columns=['Start Date', 'End Date', 'Forecast'])

    df = df.append({'Start Date': period['startTime'], 'End Date': period['endTime'], 'Forecast': period['detailedForecast']}, ignore_index=True)
    df = df.drop_duplicates()
    df.to_pickle(file)

    #sort repositories
    file = open("README.md", "w")
    file.write('![Status](https://github.com/smishr97/python-get-forecast/actions/workflows/build.yml/badge.svg)\n')
    file.write('![Status](https://github.com/smishr97/python-get-forecast/actions/workflows/pretty.yml/badge.svg)\n')
    file.write('# Pittsburgh Nightly Forecast\n\n')
    
    file.write(df.to_markdown(tablefmt='github'))
    file.write('\n\n---\nCopyright © 2022 Pittsburgh Supercomputing Center. All Rights Reserved.')
    file.close()

if __name__ == "__main__":
    main()
