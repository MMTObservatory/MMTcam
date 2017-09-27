"""
Utilities for querying MMT systems to get information to include in image headers
"""

import json
from urllib.parse import urlencode

import urllib3
urllib3.disable_warnings()

import redis

import astropy.units as u
from astropy.coordinates import Angle

API_HOST = "https://api.mmto.arizona.edu/APIv1"
REDIS_HOST = "ops.mmto.arizona.edu"

HEADER_MAP = {
    'mount_mini_ra': {
        'fitskey': "RA",
        'comment': "Object RA",
        'units': u.hourangle,
    },
    'mount_mini_declination': {
        'fitskey': "DEC",
        'comment': "Object Dec",
        'units': u.deg,
    },
    'mount_mini_epoch': {
        'fitskey': "EPOCH",
        'comment': "Coordinate Epoch",
        'units': u.year,
    },
    'mount_mini_cat_id': {
        'fitskey': "CAT_ID",
        'comment': "Catalog Source Name",
        'units': None,
    },
    'mount_mini_cat_ra2000': {
        'fitskey': "RA_2000",
        'comment': "Catalog RA (J2000)",
        'units': u.hourangle,
    },
    'mount_mini_cat_dec2000': {
        'fitskey': "DEC_2000",
        'comment': "Catalog Dec (J2000)",
        'units': u.deg,
    },
    'mount_mini_alt': {
        'fitskey': "EL",
        'comment': "Object Elevation at time of observation",
        'units': u.deg,
    },
    'mount_mini_az': {
        'fitskey': "AZ",
        'comment': "Object Azimuth at time of observation",
        'units': u.deg,
    },
    'mount_mini_rot': {
        'fitskey': "ROT",
        'comment': "Instrument Rotator Angle",
        'units': u.deg,
    },
    'mount_mini_pa': {
        'fitskey': "PA",
        'comment': "Parallactic Angle",
        'units': u.deg,
    },
    'mount_mini_uttime': {
        'fitskey': "UT",
        'comment': "UT of observation",
        'units': u.hour,
    },
    'mount_mini_lst': {
        'fitskey': "LST",
        'comment': "Sidereal Time of observation",
        'units': u.hour,
    },
    'mount_mini_ha': {
        'fitskey': "HA",
        'comment': "Hour Angle of observation",
        'units': u.hour,
    },
    'mount_mini_airmass': {
        'fitskey': "AIRMASS",
        'comment': "Object Airmass (Secant of Zenith Distance) at time of observation",
        'units': None,
    },
    'mount_mini_total_off_alt': {
        'fitskey': "EL_OFF",
        'comment': "Total elevation offset",
        'units': u.arcsec,
    },
    'mount_mini_total_off_az': {
        'fitskey': "AZ_OFF",
        'comment': "Total azimuth offset",
        'units': u.arcsec,
    },
    'mount_mini_total_off_ra': {
        'fitskey': "RA_OFF",
        'comment': "Total RA offset",
        'units': u.arcsec,
    },
    'mount_mini_total_off_dec': {
        'fitskey': "DEC_OFF",
        'comment': "Total Dec offset",
        'units': u.arcsec,
    },
    'mount_mini_instoff_az': {
        'fitskey': "AZ_INST",
        'comment': "Instrument Az offset",
        'units': u.arcsec,
    },
    'mount_mini_instoff_alt': {
        'fitskey': "EL_INST",
        'comment': "Instrument El offset",
        'units': u.arcsec,
    },
    'hexapod_mini_curxyz_z': {
        'fitskey': "FOCUS",
        'comment': "Hexapod Focus (um)",
        'units': u.micron,
    },
    'hexapod_mini_curxyz_y': {
        'fitskey': "TRANSY",
        'comment': "Hexapod Y Translation (um)",
        'units': u.micron,
    },
    'hexapod_mini_curxyz_z': {
        'fitskey': "TRANSX",
        'comment': "Hexapod X Translation (um)",
        'units': u.micron,
    },
    'hexapod_mini_curxyz_tx': {
        'fitskey': "TILTX",
        'comment': "Hexapod X Tilt (arcsec)",
        'units': u.arcsec,
    },
    'hexapod_mini_curxyz_ty': {
        'fitskey': "TILTY",
        'comment': "Hexapod Y Tilt (arcsec)",
        'units': u.arcsec,
    },
    'hexapod_mini_curr_temp': {
        'fitskey': "OSSTEMP",
        'comment': "Average OSS Temperature",
        'units': u.Celsius,
    },
}


def get_redis_keys(r=redis.StrictRedis(host=REDIS_HOST)):
    keys = sorted([k.decode() for k in r.keys()])
    return keys


def get_api_keys(http=urllib3.PoolManager()):
    """
    Get list of redis keys via the MMTO web api
    """
    url = API_HOST + "/keys"
    r = http.request('GET', url)
    data = json.loads(r.data.decode('utf-8'))
    return sorted(data)


def get_api(keys=[], http=urllib3.PoolManager()):
    """
    Given list of keys, return a dict containing the redis values for each keys
    """
    url = API_HOST + "/vals"
    r = http.request(
        'POST',
        url,
        fields={'keys': ",".join(keys)}
    )
    data = json.loads(r.data.decode('utf-8'))
    return data
