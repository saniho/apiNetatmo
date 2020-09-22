
import logging

_LOGGER = logging.getLogger(__name__)


import json
import requests

class myStation:
    def __init__(self):
        self._pressure = None
        self._temperature = None
        self._humidity = None
        self._wind = None
        self._windMax = None
        self._windMaxTime = None
        self._lastSynchro = None
        pass

    def getPressure(self):
        return self._pressure
    def getTemperature(self):
        return self._temperature
    def getHumidity(self):
        return self._humidity
    def getWind(self):
        return self._wind
    def getWindMax(self):
        return self._windMax
    def getWindMaxTime(self):
        return self._windMaxTime

    def getIdStation(self):
        return self._idStation

    def getNomStation(self):
        return self._nomStation

    def createStation(self, myDevice):
        #print(myDevice)
        self._idStation = myDevice["_id"]
        self._nomStation = myDevice["station_name"]
        #print(self._nomStation)
        for dataType in myDevice["data_type"]:
            # print(dataType)
            if (dataType == "Pressure"):
                self._pressure = myDevice["dashboard_data"]["Pressure"]

        for module in myDevice["modules"]:
            #print(module)
            for dataType in module["data_type"]:
                #print(dataType)
                # pressure ???
                if (dataType == "Temperature"):
                    if( "dashboard_data" in module.keys()):
                        self._temperature = module["dashboard_data"]["Temperature"]
                if (dataType == "Humidity"):
                    if ("dashboard_data" in module.keys()):
                        self._humidity = module["dashboard_data"]["Humidity"]
                if (dataType == "Wind"):
                    if ("dashboard_data" in module.keys()):
                        self._wind = module["dashboard_data"]["WindStrength"]
                        self._windMax = module["dashboard_data"]["max_wind_str"]
                        self._windMaxTime = module["dashboard_data"]["date_max_wind_str"]

        pass

    def setLastSynchro(self, lastSynchro):
        self._lastSynchro = lastSynchro

    def getLastSynchro(self):
        return self._lastSynchro

class apiNetatmo:
    def __init__(self, clientID, clientSecret, username, password, deviceId):
        self.CLIENT_ID = clientID
        self.CLIENT_SECRET = clientSecret
        self.USERNAME = username
        self.PASSWORD = password
        self.deviceId = deviceId
        pass

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


    def get_favorites_stations(self, access_token ):
        import datetime
        device_id = "06:00:00:02:5e:ce"
        params = {
            'access_token': access_token,
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
            for device in data['devices']:
                mySt = myStation()
                mySt.createStation( device )
                mySt.setLastSynchro( datetime.datetime.now() )
                lstStation[ mySt.getIdStation() ] = mySt
            return lstStation

    def update_favorites_stations(self, access_token, lstStation ):
        import datetime
        params = {
            'access_token': access_token,
            'device_id': self.deviceId,
            'get_favorites': "true",
        }
        data = self.post_and_get_json("https://api.netatmo.com/api/getstationsdata", "body", params=params)
        if ( data is None ):
            return None
        else:
            # remplace lstStation par un lstStation avec key et ou la key est l'id de lstation ..
            # pour faire un update ensuite et update la bonne station de la liste.
            for device in data['devices']:
                mySt = myStation()
                mySt.createStation( device )
                mySt.setLastSynchro(datetime.datetime.now())
                if mySt.getIdStation() in lstStation.keys():
                    lstStation[ mySt.getIdStation() ] = mySt
            return lstStation
