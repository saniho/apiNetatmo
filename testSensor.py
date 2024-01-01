# pour recupere le fichier avec les credential
import configparser
mon_conteneur = configparser.ConfigParser()
mon_conteneur.read("../myCredential/security.txt")
CLIENT_ID = mon_conteneur['NETATMO']['CLIENT_ID']
CLIENT_SECRET = mon_conteneur['NETATMO']['CLIENT_SECRET']
REFRESH_TOKEN = mon_conteneur['NETATMO']['REFRESH_TOKEN']
ACCESS_TOKEN = mon_conteneur['NETATMO']['ACCESS_TOKEN']
from custom_components.apiNetatmo import apiNetatmo

from custom_components.apiNetatmo import  lnetatmo

myNetatmo = apiNetatmo.apiNetatmo( CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, ACCESS_TOKEN, deviceId="06:00:00:02:5e:ce")
#authorization = lnetatmo.ClientAuth( CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, ACCESS_TOKEN )

#devList = lnetatmo.WeatherStationData(authorization)
#print( devList )
myNetatmo.authenticate()
data = myNetatmo.get_favorites_stations()
for clef in data.keys():
    print(" -----", clef, " ----" )
    print("getWindMax : ", data[clef].getWindMax())
    print("getRain : ", data[clef].getRain())

# for device in data['devices']:
#     print( "--------" )
#     print(device["_id"])
#     print(device["station_name"])
#     for dataType in device["data_type"]:
#         #print(dataType)
#         if(dataType=="Pressure"):
#             print(dataType, device["dashboard_data"]["Pressure"])
#         #pressure ???
#     #for clef in device.keys():
#     #    print(clef, device[clef])
#     for module in device["modules"]:
#         #print(module)
#         for dataType in module["data_type"]:
#             #print(dataType)
#             #pressure ???
#             if(dataType=="Temperature"):
#                 print(dataType, module["dashboard_data"]["Temperature"])
#             if(dataType=="Humidity"):
#                 print(dataType, module["dashboard_data"]["Humidity"])
#             if(dataType=="Rain"):
#                 print(dataType, module["dashboard_data"]["Rain"])
#                 print("sum_rain_1", module["dashboard_data"]["sum_rain_1"])
#                 print("sum_rain_24", module["dashboard_data"]["sum_rain_24"])
#             if(dataType=="Wind"):
#                 print("WindStrength", module["dashboard_data"]["WindStrength"])
#                 print("max_wind_str", module["dashboard_data"]["max_wind_str"])
#
#         #print(module["dashboard_data"])
#         """
#         70:ee:50:05:83:34
#         Langeais
#         Pressure 1008.1
#         ==> 70:ee:50:05:83:34_Langeais.Pressure.value = 1008.1
#         un objet par station, avec tous les items rattachés
#         """