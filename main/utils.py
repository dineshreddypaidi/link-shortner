import requests
from django.conf import settings

def get_geolocation(ip_address):
    #ip stack
        #url = f'http://api.ipstack.com/{ip_address}?access_key={settings.IPINFO_API_KEY}'
    #ipinfo
    url = f"https://ipinfo.io/{ip_address}?token={settings.IPINFO_API_KEY}"
    response = requests.get(url)
    data = response.json()
    loc = data.get('loc')
    try:
        lat, lon = loc.split(',')
    except:
        lat, lon = 0,0    
    return {
        'country': data.get('country'),
        'city': data.get('city'),
        'region': data.get('region'),
        'isp': data.get('org'),
        'latitude': lat,
        'longitude': lon,
    }