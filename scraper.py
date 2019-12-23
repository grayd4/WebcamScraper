#import requests
import urllib.request
import time
#from bs4 import BeautifulSoup

url = 'https://www.nps.gov/webcams-glac/aplocam.jpg'
#response = requests.get(url)
#soup = BeautifulSoup(response.text, "html.parser")
#imgTag = soup.findall('img')[0]
#link = 

urllib.request.urlretrieve(url, 'aplocam' + str(time.time()) + '.jpg')
time.sleep(60)