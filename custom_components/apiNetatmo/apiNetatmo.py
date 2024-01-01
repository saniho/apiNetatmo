
from sys import version_info

PYTHON3 = (version_info.major > 2)
import logging

_LOGGER = logging.getLogger(__name__)

import requests, urllib

class myStation:
    def __init__(self):
        self._pressure = None
        self._temperature = None
        self._humidity = None
        self._rain = None
        self._wind = None
        self._windMax = None
        self._windGustStrenght = None
        self._windMaxTime = None
        self._lastSynchro = None
        pass

    def getPressure(self):
        return self._pressure
    def getTemperature(self):
        return self._temperature
    def getHumidity(self):
        return self._humidity
    def getRain(self):
        return self._rain
    def getWind(self):
        return self._wind
    def getWindMax(self):
        return self._windMax
    def getWindMaxTime(self):
        return self._windMaxTime
    def getWindGustStrenght(self):
        return self._windGustStrenght

    def getIdStation(self):
        return self._idStation

    def getNomStation(self):
        return self._nomStation

    def createStation(self, myDevice):
        print(myDevice)
        self._idStation = myDevice["_id"]
        self._nomStation = myDevice["place"]["city"]
        print(self._nomStation)
        for dataType in myDevice["data_type"]:
             # print(dataType)
            if ( "dashboard_data" in myDevice.keys()):
                self._pressure = myDevice["dashboard_data"]["Pressure"]

        for module in myDevice["modules"]:
            if ( module['_id'] == "70:ee:50:3e:e2:5c" ):
                print(module)
            for dataType in module["data_type"]:
                print(dataType)
                # pressure ???
                if (dataType == "Temperature"):
                    if( "dashboard_data" in module.keys()):
                        self._temperature = module["dashboard_data"]["Temperature"]
                if (dataType == "Humidity"):
                    if ("dashboard_data" in module.keys()):
                        self._humidity = module["dashboard_data"]["Humidity"]
                if (dataType == "Rain"):
                    if ("dashboard_data" in module.keys()):
                        self._rain = module["dashboard_data"]["Rain"]
                if (dataType == "Wind"):
                    if ("dashboard_data" in module.keys()):
                        try:
                            self._wind = module["dashboard_data"]["WindStrength"]
                        except:
                            self._wind = None
                        try:
                            self._windGustStrenght = module["dashboard_data"]["GustStrength" ]
                        except:
                            self._windGustStrenght = None
                        try:
                            self._windMax = module["dashboard_data"]["max_wind_str" ]
                        except:
                            self._windMax = None
                        
                        try:
                            self._windMaxTime = module["dashboard_data"]["date_max_wind_str"]
                        except:
                            self._windMaxTime = None

        pass

    def setLastSynchro(self, lastSynchro):
        self._lastSynchro = lastSynchro

    def getLastSynchro(self):
        return self._lastSynchro

class apiNetatmo:
    def __init__(self, clientID, clientSecret, refreshToken, accessToken, deviceId):
        self.CLIENT_ID = clientID
        self.CLIENT_SECRET = clientSecret
        self.refreshToken = refreshToken
        self.deviceId = deviceId
        self.expiration = 0 # Force refresh token
        self._accessToken = accessToken
        pass

    def renew_token(self):
        import time
        payload = {
                "grant_type" : "refresh_token",
                "refresh_token" : self.refreshToken,
                "client_id" : self.CLIENT_ID,
                "client_secret" : self.CLIENT_SECRET
                }
        resp = self.post_and_get_json("https://api.netatmo.com/oauth2/token", "authentication", params=payload)
        print(resp)
        if self.refreshToken != resp['refresh_token']:
            print("New refresh token:", resp['refresh_token'])
        self._accessToken = resp['access_token']
        self.refreshToken = resp['refresh_token']
        self.expiration = int(resp['expire_in'] + time.time())

    def accessToken(self):
        import time
        if self.expiration < time.time() : self.renew_token()
        return self._accessToken

    def post_and_get_json(self, url, key, params=None, timeout=10):
        #response = requests.post(url, params=params, data=data)
        import json
        import urllib
        req = urllib.request.Request(url)
        if params:
            req.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
            params = urllib.parse.urlencode(params).encode('utf-8')
        try:
            response = urllib.request.urlopen(req, params, timeout=timeout)
        except urllib.error.HTTPError as err:
            if err.code == 403:
                logger.warning("Your current token scope do not allow access to %s" % topic)
            else:
                print("code=%s, reason=%s, body=%s" % (err.code, err.reason, err.fp.read()))
            return None
        data = b""
        for buff in iter(lambda: response.read(65535), b''): data += buff
        return json.loads(data.decode("utf-8"))
            #return response.json()[key]

    def authenticate(self, ):
        self.accessToken()

    def get_favorites_stations(self):
        import datetime
        device_id = "06:00:00:02:5e:ce"
        params = {
            'access_token': self._accessToken,
            'device_id': self.deviceId,
            'get_favorites': "true",
        }
        data = self.post_and_get_json("https://api.netatmo.com/api/getstationsdata", "body", params=params)
        #print(data)
        if ( data is None ):
            return None
        else:
            # remplace lstStation par un lstStation avec key et ou la key est l'id de lstation ..
            # pour faire un update ensuite et update la bonne station de la liste.
            lstStation = {}
            for device in data['body']['devices']:
                mySt = myStation()
                mySt.createStation( device )
                mySt.setLastSynchro( datetime.datetime.now() )
                lstStation[ mySt.getIdStation() ] = mySt
            return lstStation

    def update_favorites_stations(self, lstStation ):
        import datetime
        params = {
            'access_token': self._accessToken,
            'device_id': self.deviceId,
            'get_favorites': "true",
        }
        data = self.post_and_get_json("https://api.netatmo.com/api/getstationsdata", "body", params=params)
        if ( data is None ):
            return None
        else:
            # remplace lstStation par un lstStation avec key et ou la key est l'id de lstation ..
            # pour faire un update ensuite et update la bonne station de la liste.
            for device in data['body']['devices']:
                mySt = myStation()
                mySt.createStation( device )
                mySt.setLastSynchro(datetime.datetime.now())
                if mySt.getIdStation() in lstStation.keys():
                    lstStation[ mySt.getIdStation() ] = mySt
            return lstStation
