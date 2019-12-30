import urllib.request
import time
import argparse
import sys      # For accepting parameters
import cv2      # For video combining
import os       # "
import glob     # "
from os import path
from datetime import datetime

# Apgar Mt. Northeast View NPS Webcam
#url = 'https://www.nps.gov/webcams-glac/'
parser = argparse.ArgumentParser(description='Get some webcam footage')
parser.add_argument('-c', '-cam', default = 'aplocam', \
    help = 'The camera to grab the snapshot from. Is the unique identifier in the camera\'s URL', \
       metavar = 'CAM', dest = 'camera')
parser.add_argument('-u', '-url', default = 'https://www.nps.gov/webcams-glac/', \
    help = 'The url location of the webcam\'s snapshot', metavar = 'URL', dest = 'URL')

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
    out = cv2.VideoWriter(initialLocation + args.camera + folderName + '.avi', cv2.VideoWriter_fourcc(*'DIVX'), 2, size)

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

# First argument is the name of the camera as. specified in the image's URL (e.g. aplocam)
if __name__ == "__main__":

    # Returns the hour (0-24). Meant to be used in the Pacific timezone
    timeLocal = time.localtime(time.time()).tm_hour
    folderName = 'Day'

    # If a night photo - from 8 pm to 4 am
    if timeLocal > 19 or timeLocal < 4:
        folderName = 'Night'

    args = parser.parse_args()

    checkAndCreateFolders(folderName, args)
    getPhoto(folderName, args)
    createVideo(folderName, args)
    


    