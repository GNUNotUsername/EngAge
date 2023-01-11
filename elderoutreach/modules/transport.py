import requests
from json import loads

"""
NOTICE

This is pretty much deprecated.
May as well delete this before submission.
Not actually gonna do it until as late as possible tho unless it bricks something
"""

GEOCODE_REVERSE_HEADERS = {
    "QLD": {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://geocode.information.qld.gov.au/validate',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
}

GEOCODE_HEADERS = {
    "QLD": {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Referer': 'https://geocode.information.qld.gov.au/validate',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
    }
}

GEOCODE_PARAMS = {
    "QLD": {
        'address': 'rpl_address'
    },
}

GEOCODE_REVERSE_PARAMS = {
    "QLD": {
        'latitude': 'rpl_lat',
        'longitude': 'rpl_long',
    }
}

GEOCODE_ADDRESS = {
    "QLD": "https://geocode.information.qld.gov.au/api/parseLocationAddress"
}
GEOCODE_REVERSE_ADDRESS = {
    "QLD": 'https://geocode.information.qld.gov.au/api/validateCoordinates'
}

def geocode(address, state="QLD"):
    new_params = GEOCODE_PARAMS[state].copy()
    new_params["address"] = address
    response = requests.get(GEOCODE_ADDRESS[state], params=new_params, headers=GEOCODE_HEADERS[state]).json()
    coordinates = response[0]["coordinates"]
    return coordinates

def reverse_geocode(latitude, longitude, state="QLD"):
    new_params = GEOCODE_REVERSE_PARAMS[state].copy()
    new_params["latitude"] = str(latitude)
    new_params["longitude"] = str(longitude)
    response = requests.get(GEOCODE_REVERSE_ADDRESS[state], params=new_params, headers=GEOCODE_REVERSE_HEADERS[state]).json()
    address = response[0]["fullAddress"]
    return address
