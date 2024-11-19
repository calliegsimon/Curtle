#imports needed
import os

#importing for image wrangling
import numpy as np
#import pandas as pd
#importing OpenCV
import cv2

#from PIL import Image, ImageFilter
import turtle as t

#for future reference in reagrds to making gifs of the turtle drawing
#https://zulko.github.io/moviepy/getting_started/videoclips.html

#note to self, we may need to do some preprocessing for large
#images so that wed ont overwhelm the curtle
def image_processing(inputImg):
    """
    This function is our main image processing function
    1. will convert an image to grayscale
    2. will apply a gaussian blur 
    3. apply adaptive thresholding
    4. find the contours 
    5. return the coordinates and hierarchy of the contours
    """
    inputImg = cv2.imread(inputImg)
    #converting our input image to grayscale
    grayImg = cv2.cvtColor(inputImg, cv2.COLOR_BGR2GRAY)

    #apply gaussian blur
    blurImg = cv2.GaussianBlur(grayImg, (7,7), 0)

    # using adaptive thresholding
    threshMeanImg = cv2.adaptiveThreshold(blurImg, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 21, 10)

    return threshMeanImg

def extract_contours(inputImg):
    """ 
    - The contours function will take in an already thresholded image
        and find the coordinates of the contours of that image.
    - contours will likely use the retr list or retr comp, whichever ends up working
        best for our turtle drawing logic
    - The contours function will then return the list of coordinates and the shape of the image
    """
    #init the coord list
    coords = []
    # find the shape of our input image
    h, w = inputImg.shape[:2]
    # 1. find the contours of our image
    #default is using retr_list
    contours, hierarchy = cv2.findContours(inputImg, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #Uncomment this line if we want to switch the mode
    #contours, hierarchy = cv2.findContours(inputImg, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    # 2. extract the coordinates of the white regions of our image
    white_coords = []
    for contour in contours:
        coordinates = contour.squeeze().astype(float).tolist()
        white_coords.append(coordinates)

    # 3. writing the coordinates of each white region to our coords list
    for i, region in enumerate(white_coords):
        if type(region[0]) is list:
            if len(region) > 2:
             # Calculate the area of the contour
                area = cv2.contourArea(np.around(np.array([[pnt] for pnt in region])).astype(np.int32))
                if area > 100:
                    # Convert coordinates to the required format
                    # we can change this needbe to make it easier for drawing
                    crdnts = [{'x': i[0], 'y': i[1]} for i in region]
                    coords.append(crdnts)

    return coords, h, w
    



#TODO: curtle logic :D
def curtle_drawing(coordinates, h, w):
    """curtle will take in a coordinates list 
    coordinates list will be gotten from a contours function
    
    Sample of expected coordinate format:
    [[{'x': 95.0, 'y': 693.0}, {'x': 94.0, 'y': 694.0}, {'x': 93.0, 'y': 694.0},
    {'x': 92.0, 'y': 694.0}, {'x': 91.0, 'y': 694.0}, {'x': 90.0, 'y': 694.0}, {'x': 89.0, 'y': 695.0}
    
    """

    #the video portion of the turtle drawing will likely also be in here i assume atm
    #same with the file? if not itll be in main
    
    # make canvas
    canvas = t.Screen()
    canvas.setup(h,w)
    canvas.bgcolor("black")

    # making pencil
    pencil = t.Turtle()
    pencil.speed(0)
    pencil.penup()
    pencil.color("white")
    pencil.pensize(2)

    colors = []

    # start draw
    for spot in coordinates:

    t.done()
    


if __name__ == '__main__':
    #inits needed 
    #we want image to 
    count = 1
    #making sure the processed directories exist
    # ^ this will have both gifs and end results of images
    os.makedirs("processed", exist_ok=True)


    with os.scandir("raw") as fileList:
        #loop through all the files
        for img in fileList:
            #if image is a jpg or a png
            if (img.name.endswith(".jpg") or img.name.endswith(".png")) and img.is_file():
                #process image
                processedImg = image_processing(img)
                print(f"Image #{count} processed")

                #extract contours for image
                #coords should be a list of coordinates returned from extract_contours
                coords, cH, cW = extract_contours(processedImg)
                print(f"Image #{count}'s contours extracted")

                #drawing function for image
                if img.name == "Blind_Obsession_Ishmael.png":
                    curtle_drawing(coords, cH, cW)
                    print("wa")
                #save the turtle img

                #saving the gif of turtle drawing

                #update count for sequential file formats(assuming we use this)
                count += 1

    