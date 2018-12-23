import requests
import pandas as pd
import json
import datetime

# import pdb
# pdb.set_trace()
# imgGPS_Data = (imgGPS[0], imgGPS[1]) #object to retrieve gps related info




# print('Weather Info: {}'.format(imgWeather))

# imgElevation = GPSDATA.get_elevation(lat, long)
def get_elevation(lat, long):
    query = r'https://api.open-elevation.com/api/v1/lookup?locations={},{}'.format(lat, long)
    # query = ('https://api.open-elevation.com/api/v1/lookup?locations={lat},{long}')
    try:
        r = requests.get(query)  # json object, various ways you can extract value
    except Exception as e:
        elevation = e
    else:
        elevation = json.loads(r.text)
    return elevation

# imgDayLight = GPSDATA.get_daylight_info(imgExif['DateTime'])
def get_daylight_info(lat, long, dateTime):
    imgDate = datetime.datetime.strptime(dateTime, '%Y:%m:%d %H:%M:%S')
    date = imgDate.date().__str__()
    '''API call to get json formatted data. parameters lat, long and date'''
    query = ('https://api.sunrise-sunset.org/json?lat={}&lng={}&date={}'.format(lat, long, date))
    # print(query)
    r = requests.get(query)
    result = json.load(r)
    if result['status'] == 'OK':
        return result
    else:
        return result['status']

# imgWeather = GPSDATA.get_weather_info(imgExif['DateTime'])
def get_weather_info(lat, long,date=0):
    if date == 0:
        result = {'result': 'No date'}
    else:
        dateString = date.date().__str__()+'T'+date.time().__str__()
        '''2018-11-11T00:00:00'''
        query = ("https://api.darksky.net/forecast/85409944ffc4446e1e75b5802c2407db/{},{},{}".format(lat, long, dateString))
        try:
            r = requests.get(query)
            result = json.loads(r.text)
        except Exception as e:
            result = e
        return result