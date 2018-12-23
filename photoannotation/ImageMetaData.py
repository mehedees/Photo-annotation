from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import datetime, requests, json

class ImageMetaData(object):
    '''
    Extract the exif data from any image. Data includes GPS coordinates,
    Focal Length, Manufacture, and more.
    '''
    exif_data = None
    image = None

    def __init__(self, img_path):
        self.image = Image.open(img_path)
        #self.image = img_path
        #print(self.image._getexif())
        #self.get_exif_data()
        super(ImageMetaData, self).__init__()

    def get_exif_data(self):
        """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
        exif_data = {}
        info = self.image._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[str(decoded)] = gps_data
                else:
                    exif_data[str(decoded)] = value
        self.exif_data = exif_data
        return exif_data

    def get_if_exist(self, data, key):
        if key in data:
            return data[key]
        return None

    def convert_to_degress(self, value):

        """Helper function to convert the GPS coordinates
        stored in the EXIF to degress in float format"""
        d0 = value[0][0]
        d1 = value[0][1]
        d = float(d0) / float(d1)

        m0 = value[1][0]
        m1 = value[1][1]
        m = float(m0) / float(m1)

        s0 = value[2][0]
        s1 = value[2][1]
        s = float(s0) / float(s1)

        return d + (m / 60.0) + (s / 3600.0)

    def get_gps(self):
        """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
        lat = 0
        lng = 0
        gps_alt = 0
        gps_alt_ref = 0
        exif_data = self.get_exif_data()
        #print(exif_data)
        if "GPSInfo" in exif_data:
            gps_info = exif_data["GPSInfo"]
            gps_latitude = self.get_if_exist(gps_info, "GPSLatitude")
            gps_latitude_ref = self.get_if_exist(gps_info, 'GPSLatitudeRef')
            gps_longitude = self.get_if_exist(gps_info, 'GPSLongitude')
            gps_longitude_ref = self.get_if_exist(gps_info, 'GPSLongitudeRef')
            if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
                lat = self.convert_to_degress(gps_latitude)
                if gps_latitude_ref != "N":
                    lat = 0 - lat
                lng = self.convert_to_degress(gps_longitude)
                if gps_longitude_ref != "E":
                    lng = 0 - lng

            if 'GPSAltitudeRef' in gps_info:
                gps_alt_ref = self.get_if_exist(gps_info, 'GPSAltitudeRef')
            else:
                gps_alt_ref = 0

            if 'GPSAltitude' in gps_info:
                gps_alt = self.get_if_exist(gps_info, 'GPSAltitude')
            else:
                gps_alt = 0

        return lat, lng, gps_alt, gps_alt_ref

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
    def get_weather_info(lat, long, date=0):
        if date == 0:
            result = {'result': 'No date'}
        else:
            dateString = date.date().__str__() + 'T' + date.time().__str__()
            '''2018-11-11T00:00:00'''
            query = ("https://api.darksky.net/forecast/85409944ffc4446e1e75b5802c2407db/{},{},{}".format(lat, long,
                                                                                                         dateString))
            try:
                r = requests.get(query)
                result = json.loads(r.text)
            except Exception as e:
                result = e
            return result