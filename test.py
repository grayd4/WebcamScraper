import argparse

parser = argparse.ArgumentParser(description='Get some webcam footage')
parser.add_argument('-c', '-cam', default = 'aplocam', \
    help = 'The camera to grab the snapshot from. Is the unique identifier in the camera\'s URL', \
       metavar = 'CAM', dest = 'camera')
parser.add_argument('-u', '-url', default = 'https://www.nps.gov/webcams-glac/', \
    help = 'The url location of the webcam\'s snapshot', metavar = 'URL', dest = 'URL')
URL = ''
if __name__ == "__main__":
    args = parser.parse_args()
    print (args)
    print(URL)