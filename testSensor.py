
def test1():
    CLIENT_ID = '5f10bdd86f43bb494a5bce4e'
    CLIENT_SECRET = 'PA7qEzhnKzCKsXe0Ehrv6zPZTM'
    USERNAME = 'nicolas.juignet@gmail.com'
    PASSWORD = 'F8Dd?Yeht5@f?8J'
    import patatmo

    # your netatmo connect developer credentials
    credentials = {
        "password":PASSWORD,
        "username":USERNAME,
        "client_id": CLIENT_ID,
        "client_secret":CLIENT_SECRET
    }

    # configure the authentication
    authentication = patatmo.api.authentication.Authentication(
        credentials=credentials,
        tmpfile = "temp_auth.json"
    )
    # providing a path to a tmpfile is optionally.
    # If you do so, the tokens are stored there for later reuse,
    # e.g. next time you invoke this script.
    # This saves time because no new tokens have to be requested.
    # New tokens are then only requested if the old ones expire.

    # create a api client
    client = patatmo.api.client.NetatmoClient(authentication)

    # lat/lon outline of Hamburg/Germany
    myRegion = {
        "lat_ne" : 47.356089,
        "lon_ne" : 0.466389,
        "lat_sw" : 47.314906,
        "lon_sw" : 0.399441,
    }

    # issue the API request
    netatmoInfo = client.Getpublicdata(region = myRegion)

    # convert the response to a pandas.DataFrame
    #print(netatmoInfo.dataframe)
    print(netatmoInfo.response['body'])
    for sensor in netatmoInfo.response['body'][:2]:
        myData = sensor['measures']
        print("myData :", myData)
        print("location", sensor["place"])
        # on va voir pour filtrer que les id interessant ici langeais : 02:00:00:05:7a:ba
        for mykey in myData.keys():
            #print(myData[mykey])
            if ( 'res' in myData[mykey] ):
                #print('measure:',myData[mykey]['res'])
                myMeasure = myData[mykey]
                #ch = myData[myData.keys()[0]]
                for x in range(len(myMeasure['type'])):
                    for y in myMeasure['res'].keys():
                        print( "*", myMeasure['type'][x], myMeasure['res'][y][x])
            elif ( 'rain_live' in myData[mykey].keys() ):
                print('rain:', myData[mykey])
            elif ( 'wind_strength' in myData[mykey].keys() ):
                print('wind_strength:', myData[mykey])
            else:
                print("ici")
                print(myData[mykey].keys())

    #response ..to le public data, à voir geocding zone saint jean de monts pour check ;)


import apiNetatmo


myNetatmo = apiNetatmo.apiNetatmo()
token = myNetatmo.authenticate()
data = myNetatmo.get_favorites_stations(token)
print(data[0].getTemperature())

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