import urllib.request
import time
import argparse
import sys      # For accepting parameters
import cv2      # For video combining
import os       # "
import glob     # "
import json     # For sunset
import requests # For sunset
from os import path
from datetime import datetime

# Set up arguments command can take
parser = argparse.ArgumentParser(description='Get some webcam footage')
parser.add_argument('-c', '-cam', default = 'aplocam', \
    help = 'The camera to grab the snapshot from. Is the unique identifier in the camera\'s URL', \
       metavar = 'CAM', dest = 'camera')
parser.add_argument('-u', '-url', default = 'https://www.nps.gov/webcams-glac/', \
    help = 'The url location of the webcam\'s snapshot', metavar = 'URL', dest = 'URL')

# Sunset flags:
# If sunset set to true, will only grab photo if the current time is near to the sunset time
# of the given latitude and longitude
parser.add_argument('-s', '-sunset', default = 'false', \
    help = 'If this is set to \'true\', then the photo will only be grabbed if it\'s sunset in the \
        given timezone. \'true\' triggers the sunset, anything else will not.', metavar = 'SUN', dest = 'sunset')
parser.add_argument('-lat', '-latitude', default = '48.5', help = 'Latitude to measure sunset time at.', \
    metavar = 'LAT', dest = 'latitude')
parser.add_argument('-lon', '-longitude', default = '-113.3', help = 'Longitude to measure sunset time at.', \
    metavar = 'LON', dest = 'longitude')



# Retrieve a photo and save it in the correct folder depending on the time of day
# folderName = whetehr to place in day/night folder
# cam = name of cam to get image from
def getPhoto(folderName, args):
    # File location and name of the photo to save
    nameString = 'Output/' + args.camera + '/' + folderName + '/' + args.camera + str(time.time()) + '.jpg'
    # Save the webcam capture in the desired location
    urllib.request.urlretrieve(args.URL + args.camera + '.jpg', nameString)

# Combine images from photos into a video
# folderName = whether in day/night folder
# cam = name of cam we got image from
def createVideo(folderName, args):
    # Largely from https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    imgList = []
    #C:/Working/WebcamScraper
    initialLocation = 'Output/' + args.camera + '/'
    locationToIterate = initialLocation + folderName + '/*.jpg'
    # Iterate through every photo in given folder, adding to the list
    # In the order that they are in in the folder
    for fileName in glob.glob(locationToIterate):
        img = cv2.imread(fileName)
        height, width, layers = img.shape
        size = (width, height)
        imgList.append(img)

    # Create the 'video' that has yet to have images added to it
    # file name, fourcc, fps/images per second, size
    out = cv2.VideoWriter(initialLocation + args.camera + folderName + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 0.5, size)

    # Add image to video
    for i in range(len(imgList)):
        out.write(imgList[i])
    out.release()

# Check if a folder already exists for the given camera parameter
# If it does not, create one and its subdirectories
def checkAndCreateFolders(folderName, args):
    location = 'Output/' + args.camera + '/' + folderName
    if not path.exists(location):
        try:
            os.makedirs(location)
        except OSError:
            print ("Creation of the directory %s failed" % location)

# Execute the standard webcam photo grabbing
def takeWebcamPhotoComplete(args):
    # Returns the hour (0-24). Meant to be used in the Pacific timezone
    timeLocal = time.localtime(time.time()).tm_hour
    folderName = 'Day'
    if (args.sunset == 'true'):
        folderName = 'Sunset'

    # If a night photo - from 8 pm to 4 am
    elif timeLocal > 19 or timeLocal < 4:
        folderName = 'Night'

    checkAndCreateFolders(folderName, args)
    getPhoto(folderName, args)
    createVideo(folderName, args)

# Check sunset time at given coordinates
# Return true if close to sunset time, false if not
def getSunsetTime(args):
    try:
        lat = float(args.latitude)
        lon = float(args.longitude)
    except ValueError:
        print("Latitude or longitude flags are not valid floats.")
        return False, time.time()
    requestURL = 'https://api.sunrise-sunset.org/json?lat=' + lat + '&lng=' + lon 
    response = requests.post(requestURL)
    if response.status_code != 200:
        return False, time.time()
    responseDict = json.loads(response)         # Convert json response to python dict
    
    

# First argument is the name of the camera as. specified in the image's URL (e.g. aplocam)
if __name__ == "__main__":

    args = parser.parse_args()
    takeWebcamPhotoComplete(args) 
    
    


    