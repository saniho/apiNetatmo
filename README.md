# apiNetatmo
apiNetatmo vous permet de recupere les informations des stations favorits de votre compte NetAtmo


il suffit d'ajouter le sensor suvant dans votre configuration home assistant


```yaml
- platform: apiNetatmo
  username : <votreusername>
  password : <votrepassword>
  code: <votrecode>
  token: <votretoken>
  host: <une des adresse mac d'un de vos favori>
  scan_interval: 600
```
