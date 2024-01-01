"""Sensor for my first"""
import logging
from collections import defaultdict
from datetime import timedelta

import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_TOKEN,
    CONF_CODE,
    CONF_HOST,
    ATTR_ATTRIBUTION,
    CONF_SCAN_INTERVAL,
)

from .const import ( __VERSION__ , CONF_REFRESH_TOKEN, CONF_ACCESS_TOKEN)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

DOMAIN = "saniho"

ICON = "mdi:package-variant-closed"

SCAN_INTERVAL = timedelta(seconds=1800)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_REFRESH_TOKEN): cv.string,
        vol.Required(CONF_ACCESS_TOKEN): cv.string,
        vol.Required(CONF_TOKEN): cv.string,
        vol.Required(CONF_CODE): cv.string,
        vol.Required(CONF_HOST): cv.string,
        vol.Optional(CONF_NAME): cv.string,
    }
)

from . import apiNetatmo

class myNetatmo:
    def __init__(self, clientID, clientSecret, refreshToken, accessToken, host, _update_interval):
        self._lastSynchro = None
        self._lstStation = None
        self._update_interval = _update_interval
        self.clientID, self.clientSecret, self.refreshToken, self.accessToken, self.host = \
            clientID, clientSecret, refreshToken, accessToken, host
        pass


    def update(self,):
        import json
        import datetime

        courant = datetime.datetime.now()
        if ( self._lastSynchro == None ) or \
            ( (self._lastSynchro + self._update_interval) < courant ):

            self._myNetatmo = apiNetatmo.apiNetatmo( \
                self.clientID, self.clientSecret, self.refreshToken, self.accessToken, self.host )
            token = self._myNetatmo.authenticate()
            if ( self._lstStation == None ):
                self._lstStation = self._myNetatmo.get_favorites_stations()
            else:
                self._lstStation = self._myNetatmo.update_favorites_stations( self._lstStation )
            self._lastSynchro = datetime.datetime.now()
            _LOGGER.info("update fait, last synchro ... %s " %(self._lastSynchro))

    def getLstStation(self):
        return self._lstStation


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the platform."""
    name = config.get(CONF_NAME)
    update_interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)

    refreshToken = config.get(CONF_REFRESH_TOKEN)
    accessToken = config.get(CONF_ACCESS_TOKEN)
    clientID = config.get(CONF_CODE)
    clientSecret = config.get(CONF_TOKEN)
    host = config.get(CONF_HOST)

    try:
        session = []
    except :
        _LOGGER.exception("Could not run my First Extension")
        return False

    myNet = myNetatmo( clientID, clientSecret, refreshToken, accessToken, host, update_interval )
    myNet.update()
    lstStations = myNet.getLstStation()
    for myStationKeys in lstStations.keys():
        myStation = lstStations[ myStationKeys ]
        if ( myStation.getTemperature() != None ):
            add_entities([netatmoSensorTemperature(session, name, update_interval, myNet, myStationKeys )], True)
        if ( myStation.getHumidity() != None ):
            add_entities([netatmoSensorHumidity(session, name, update_interval, myNet, myStationKeys )], True)
        if ( myStation.getRain() != None ):
            add_entities([netatmoSensorRain(session, name, update_interval, myNet, myStationKeys )], True)
        if ( myStation.getPressure() != None ):
            add_entities([netatmoSensorPressure(session, name, update_interval, myNet, myStationKeys )], True)
        if ( myStation.getWind() != None ):
            add_entities([netatmoSensorWind(session, name, update_interval, myNet, myStationKeys )], True)
        if ( myStation.getWindMax() != None ):
            add_entities([netatmoSensorWindMax(session, name, update_interval, myNet, myStationKeys )], True)
        if (myStation.getWindGustStrenght() != None):
            add_entities([netatmoSensorWindGustStrenght(session, name, update_interval, myNet, myStationKeys)], True)
        if ( myStation.getWindMaxTime() != None ):
            add_entities([netatmoSensorWindMaxTime(session, name, update_interval, myNet, myStationKeys )], True)
        add_entities([netAtmoSensorlastSynchro(session, name, update_interval, myNet, myStationKeys )], True)
    # on va gerer  un element par heure ... maintenant

class netatmoSensorTemperature(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.temperature" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.temperature" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "°C"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        try:
            temperature = self._myNet.getLstStation()[ self._myStationNetatmoKey].getTemperature()
            status_counts["temperature"] = temperature
            status_counts["version"] = __VERSION__
        except:
            return
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %temperature

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON

class netatmoSensorHumidity(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.humidity" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.humidity" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "%"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        humidity = self._myNet.getLstStation()[ self._myStationNetatmoKey].getHumidity()
        status_counts["humidity"] = humidity
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %humidity

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON


class netatmoSensorRain(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.rain" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.rain" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "%"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        rain = self._myNet.getLstStation()[ self._myStationNetatmoKey].getRain()
        status_counts["rain"] = rain
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %rain

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON


class netatmoSensorPressure(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.pressure" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.pressure" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "hPa"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        pressure = self._myNet.getLstStation()[ self._myStationNetatmoKey].getPressure()
        status_counts["Pressure"] = pressure
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %pressure

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON

class netatmoSensorWind(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.wind" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.wind" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "km/h"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        wind = self._myNet.getLstStation()[ self._myStationNetatmoKey].getWind()
        status_counts["Wind"] = wind
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %wind

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON

class netatmoSensorWindMax(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.windMax" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.windMax" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "Km/h"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        windMax = self._myNet.getLstStation()[ self._myStationNetatmoKey].getWindMax()
        status_counts["WindMax"] = windMax
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %windMax

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON

class netatmoSensorWindGustStrenght(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.windGustStrenght" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.windGustStrenght" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return "Km/h"

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        WindGustStrenght = self._myNet.getLstStation()[ self._myStationNetatmoKey].getWindGustStrenght()
        status_counts["WindGustStrenght"] = WindGustStrenght
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = "%s" %WindGustStrenght

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON

class netatmoSensorWindMaxTime(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.windMaxTime" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.windMaxTime" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return ""

    def _update(self):
        """Update device state."""
        import datetime
        status_counts = defaultdict(int)
        self._myNet.update()
        myTime = self._myNet.getLstStation()[ self._myStationNetatmoKey].getWindMaxTime()
        if ( myTime is not None):
            myTimeFormat = datetime.datetime.fromtimestamp(myTime).isoformat()
            status_counts["LastUpdate"] = myTimeFormat
            status_counts["version"] = __VERSION__
            self._attributes = {ATTR_ATTRIBUTION: ""}
            self._attributes.update(status_counts)
            self._state = myTimeFormat

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON

class netAtmoSensorlastSynchro(Entity):
    """."""

    def __init__(self, session, name, interval, myNet, myStationNetatmoKey):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myStationNetatmoKey = myStationNetatmoKey
        self._myNet = myNet
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def unique_id(self):
        "Return a unique_id for this entity."
        return "myNetatmo.%s.%s.derniereSynchro" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.%s.%s.derniereSynchro" \
               %(self._myNet.getLstStation()[ self._myStationNetatmoKey].getIdStation(), \
                 self._myNet.getLstStation()[ self._myStationNetatmoKey].getNomStation())
    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return ""

    def _update(self):
        """Update device state."""
        status_counts = defaultdict(int)
        self._myNet.update()
        lastSynchro = self._myNet.getLstStation()[ self._myStationNetatmoKey].getLastSynchro()
        status_counts["LastSynchro"] = lastSynchro
        status_counts["version"] = __VERSION__
        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = self._myNet.getLstStation()[ self._myStationNetatmoKey].getLastSynchro().strftime("%d-%b-%Y (%H:%M:%S)")

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON