import urllib.request
import time
from datetime import datetime

# Apgar Mt. Northeast View NPS Webcam
url = 'https://www.nps.gov/webcams-glac/aplocam.jpg'

if __name__ == "__main__":

    # Returns the hour (0-24). Meant to be used in the Pacific timezone
    timeLocal = time.localtime(time.time()).tm_hour

    nameString = ''

    # If a night photo - from 8 to 4 am
    if timeLocal > 20 or timeLocal < 4:
        nameString = 'Night/aplocam'
    else:
        nameString = 'Day/aplocam'

    # Save the webcam capture in the desired location
    urllib.request.urlretrieve(url, nameString + str(time.time()) + '.jpg')