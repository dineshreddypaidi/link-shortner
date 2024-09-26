from django.http import HttpResponse
from . import models
from django.template import loader
from django.conf import settings
from user_agents import parse
import requests
from django.shortcuts import redirect

#---#
def index(request):
    template = loader.get_template('index.html')
    data = models.links.objects.all()
    info = {
        'data' : data,
    } 
    return HttpResponse(template.render(info,request))

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
    
def url_redirect(request,short_url):
    user_agent_str = request.META.get('HTTP_USER_AGENT', '')
    user_agent = parse(user_agent_str)
    
    ip_address = request.META.get('REMOTE_ADDR', '')
    
    geo_data = get_geolocation(ip_address)
    link = models.links.objects.get(short_link=short_url)
    link.no_of_views += 1
    link.save()
    
    data = {}
    data['ip'] = ip_address
    
    data['user_agent'] = user_agent_str 
    data['referrer'] = request.META.get('HTTP_REFERER', '')        
    
    data['os'] = user_agent.os.family
    data['os_version'] = user_agent.os.version_string

    data['device'] = user_agent.device.family
    data['device_brand'] = user_agent.device.brand
    data['device_model'] = user_agent.device.model

    data['browser'] = user_agent.browser.family
    data['browser_version'] = user_agent.browser.version_string

    data['screen_resolution'] = request.META.get('HTTP_SCREEN_RESOLUTION')
    #data['connection_type'] = request.META.get('HTTP_CONNECTION_TYPE')
            
    clicked = models.link_history(link=link,**data,**geo_data)
    clicked.save()
    
    return redirect(link.link)