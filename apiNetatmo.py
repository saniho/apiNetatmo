# class _apiNetatmo:
#     import patatmo
#     def __init__(self):
#         CLIENT_ID = '5f10bdd86f43bb494a5bce4e'
#         CLIENT_SECRET = 'PA7qEzhnKzCKsXe0Ehrv6zPZTM'
#         USERNAME = 'nicolas.juignet@gmail.com'
#         PASSWORD = 'F8Dd?Yeht5@f?8J'
#         self._credentials = {
#             "password":PASSWORD,
#             "username":USERNAME,
#             "client_id": CLIENT_ID,
#             "client_secret":CLIENT_SECRET
#         }
#
#         self._authentication = patatmo.api.authentication.Authentication(
#             credentials= self._credentials,
#             tmpfile="temp_auth.json"
#         )
#         self._client = patatmo.api.client.NetatmoClient(self._authentication)
#
#         pass
#     def _setTemperature(self, temp):
#         self._temperature = temp
#     def _setHumidity(self, temp):
#         self._humidity = temp
#     def _setPressure(self, temp):
#         self._pressure = temp
#
#     def getTemperature(self):
#         return self._temperature
#     def getHumidity(self):
#         return self._humidity
#     def getPressure(self):
#         return self._pressure
#
#     def getInformation(self, myCoord, deviceId ):
#         self._netatmoInfo = self._client.Getpublicdata(region=myCoord)
#
#         for sensor in self._netatmoInfo.response['body'][:2]:
#             myData = sensor['measures']
#             print("myData :", myData)
#             print("location", sensor["place"])
#             # on va voir pour filtrer que les id interessant ici langeais : 02:00:00:05:7a:ba
#             for mykey in myData.keys():
#                 if ( mykey in deviceId ):
#                     #print(mykey)
#                     if ('res' in myData[mykey]):
#                         # print('measure:',myData[mykey]['res'])
#                         myMeasure = myData[mykey]
#                         # ch = myData[myData.keys()[0]]
#                         for x in range(len(myMeasure['type'])):
#                             for y in myMeasure['res'].keys():
#                                 print("*", myMeasure['type'][x], myMeasure['res'][y][x])
#                                 if ( myMeasure['type'][x] == "temperature"):
#                                     self._setTemperature( myMeasure['res'][y][x] )
#                                 if ( myMeasure['type'][x] == "humidity"):
#                                     self._setHumidity( myMeasure['res'][y][x] )
#                                 if ( myMeasure['type'][x] == "pressure"):
#                                     self._setPressure( myMeasure['res'][y][x] )
#                     elif ('rain_live' in myData[mykey].keys()):
#                         print('rain:', myData[mykey])
#                     elif ('wind_strength' in myData[mykey].keys()):
#                         print('wind_strength:', myData[mykey])
#                     else:
#                         print("ici")
#                         print(myData[mykey].keys())
#
#
#     def getListStationInfo(self, mycoord ):
#         pass


import json
import requests

class apiNetatmo:
    def __init__(self, myRegion):
        self.CLIENT_ID = '5f10bdd86f43bb494a5bce4e'
        self.CLIENT_SECRET = 'PA7qEzhnKzCKsXe0Ehrv6zPZTM'
        self.USERNAME = 'nicolas.juignet@gmail.com'
        self.PASSWORD = 'F8Dd?Yeht5@f?8J'
        self._myRegion = myRegion
        pass
    def _setTemperature(self, temp):
        self._temperature = temp
    def _setHumidity(self, temp):
        self._humidity = temp
    def _setPressure(self, temp):
        self._pressure = temp

    def getTemperature(self):
        return self._temperature
    def getHumidity(self):
        return self._humidity
    def getPressure(self):
        return self._pressure

    def post_and_get_json(self, url, key, data=None, params=None):
        try:
            response = requests.post(url, params=params, data=data)
            response.raise_for_status()
            return response.json()[key]
        except requests.exceptions.HTTPError as error:
            print('%s: %s', error.response.status_code, error.response.text)
            return None

    def authenticate(self, ):
        payload = {'grant_type': 'password',
                   'username': self.USERNAME,
                   'password': self.PASSWORD,
                   'client_id': self.CLIENT_ID,
                   'client_secret': self.CLIENT_SECRET,
                   'scope': 'read_station'}
        return self.post_and_get_json("https://api.netatmo.com/oauth2/token", "access_token", data=payload)

    def get_wind(self, access_token, deviceId):
        device_id = "06:00:00:02:5e:ce"
        params = {
            'access_token': access_token,
            'device_id': device_id,
            'lat_ne': self._myRegion['lat_ne'],
            'lon_ne': self._myRegion['lon_ne'],
            'lat_sw': self._myRegion['lat_sw'],
            'lon_sw': self._myRegion['lon_sw'],
        }
        data = self.post_and_get_json("https://api.netatmo.com/api/getpublicdata", "body", params=params)
        if ( data is None ):
            return None
        else:

            for sensor in data[:2]:
                myData = sensor['measures']
                print("myData :", myData)
                print("location", sensor["place"])
                self._setTemperature(12.3)
                # on va voir pour filtrer que les id interessant ici langeais : 02:00:00:05:7a:ba
                for mykey in myData.keys():
                    if ( mykey in deviceId ):
                        #print(mykey)
                        if ('res' in myData[mykey]):
                            # print('measure:',myData[mykey]['res'])
                            myMeasure = myData[mykey]
                            # ch = myData[myData.keys()[0]]
                            for x in range(len(myMeasure['type'])):
                                for y in myMeasure['res'].keys():
                                    print("*", myMeasure['type'][x], myMeasure['res'][y][x])
                                    if ( myMeasure['type'][x] == "temperature"):
                                        self._setTemperature( myMeasure['res'][y][x] )
                                    if ( myMeasure['type'][x] == "humidity"):
                                        self._setHumidity( myMeasure['res'][y][x] )
                                    if ( myMeasure['type'][x] == "pressure"):
                                        self._setPressure( myMeasure['res'][y][x] )
                        elif ('rain_live' in myData[mykey].keys()):
                            print('rain:', myData[mykey])
                        elif ('wind_strength' in myData[mykey].keys()):
                            print('wind_strength:', myData[mykey])
                        else:
                            print("ici")
                            print(myData[mykey].keys())

    def get_favorites_stations(self, access_token, deviceId):
        device_id = "06:00:00:02:5e:ce"
        params = {
            'access_token': access_token,
            'device_id': "02:00:00:05:7A:BA",
            'get_favorites': "true",
        }
        data = self.post_and_get_json("https://api.netatmo.com/api/getstationsdata", "body", params=params)
        if ( data is None ):
            return None
        else:
            return data

    def getListStationInfo(self, mycoord ):
        pass