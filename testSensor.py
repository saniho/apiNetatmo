

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