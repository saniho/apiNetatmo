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
    ATTR_ATTRIBUTION,
    CONF_SCAN_INTERVAL,
)

from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.util import slugify
from homeassistant.util.dt import now, parse_date

_LOGGER = logging.getLogger(__name__)

DOMAIN = "saniho"

ICON = "mdi:package-variant-closed"

SCAN_INTERVAL = timedelta(seconds=1800)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_USERNAME): cv.string,
        vol.Required(CONF_PASSWORD): cv.string,
        vol.Optional(CONF_TOKEN): cv.string,
        vol.Optional(CONF_CODE): cv.string,
        vol.Optional(CONF_NAME): cv.string,
    }
)

from . import apiNetatmo

class myNetatmo:
    def __init__(self, token):
        self._lastSynchro = None
        pass


    def update(self,):
        import json
        import datetime

        courant = datetime.datetime.now()
        #_LOGGER.warning("--------------")
        #_LOGGER.warning("tente un update  ? ... %s" %(self._lastSynchro))
        myRegion = {
            "lat_ne": 47.3290,
            "lon_ne": 0.466389,
            "lat_sw": 47.314906,
            "lon_sw": 0.4010,
        }
        # station à controler
        deviceId = ["02:00:00:05:7a:ba", "70:ee:50:05:83:34", "05:00:00:01:4b:50", "06:00:00:02:5e:ce"]

        self._myNetatmo = apiNetatmo.apiNetatmo( myRegion )
        token = self._myNetatmo.authenticate()
        wind = self._myNetatmo.get_wind(token, deviceId)

        #self._myNetatmo.getInformation(myRegion, deviceId)
        #self._lastSynchro = datetime.datetime.now()

        #_LOGGER.warning("update fait, last synchro ... %s " %(self._lastSynchro))
        return self._myNetatmo

    def getLastSynchro(self):
        return self._lastSynchro

    def getTemperature(self):
        return self._myNetatmo.getTemperature()

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the platform."""
    name = config.get(CONF_NAME)
    update_interval = config.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)

    token = config.get(CONF_TOKEN)
    _LOGGER.warning(token)
    insee = config.get(CONF_CODE)
    _LOGGER.warning(insee)

    try:
        session = []
    except :
        _LOGGER.exception("Could not run my First Extension")
        return False

    myNet = myNetatmo( token )
    myNet.update()
    add_entities([netatmoSensorTemperature(session, name, update_interval, myNet )], True)

    # on va gerer  un element par heure ... maintenant

class netatmoSensorTemperature(Entity):
    """cumulPluieA1h."""

    def __init__(self, session, name, interval, myNetatmo):
        """Initialize the sensor."""
        self._session = session
        self._name = name
        self._myNetatmo = myNetatmo
        self._attributes = None
        self._state = None
        self.update = Throttle(interval)(self._update)

    @property
    def name(self):
        """Return the name of the sensor."""
        return "myNetatmo.temperature"

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
        self._myNetatmo.update()
        status_counts = defaultdict(int)
        status_counts[0] = self._myNetatmo.getTemperature()

        self._attributes = {ATTR_ATTRIBUTION: ""}
        self._attributes.update(status_counts)
        self._state = sum(status_counts.values())

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes

    @property
    def icon(self):
        """Icon to use in the frontend."""
        return ICON
