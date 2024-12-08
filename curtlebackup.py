#imports needed
import os

#importing for image wrangling
import numpy as np
#import pandas as pd
#importing OpenCV
import cv2

#from PIL import Image, ImageFilter
import turtle as t
import random
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
                    crdnts = [[i[0], i[1]] for i in region]
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

    colors = ["red", "orange", "#B0578D","#3E001F","#7A316F","#624E88","#6A1E55","#C65BCF",
            "#91D18B", "#243D25", "#5F7464"]
    
    # make canvas
    canvas = t.Screen()
    canvas.mode("world")
    #canvas.setup(w, h, startx = 10, starty = -10) makes canvas size the size of picture
                                                 # NOT WORKING CORRECTLY, works for first picture but a hit or miss for the rest
    canvas.setworldcoordinates(0,0,w,h)
    canvas.bgcolor("white")

    # making pencil
    pencil = t.Turtle()
    pencil.speed(1)
    pencil.pensize(1)
    pencil.penup()
    canvas.tracer(0)

    for line in coordinates:
        
        temp = line[0]
        temp[1] = h - temp[1]
        pencil.goto(temp)
        pencil.color(random.choice(colors))

        # start draw
        for spot in line:
            pencil.pendown()
            if spot == line[0]:
                spot[1] = h - spot[1]
            
            spot[1] = h - spot[1]
            pencil.goto(spot)
        #print ("endline")
        canvas.update()
        pencil.penup()
    canvas.tracer(1)
    canvas.update()
    temp = input("Press enter to continue: ")



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
                curtle_drawing(coords, cH, cW)

                #save the turtle img

                #saving the gif of turtle drawing

                #update count for sequential file formats(assuming we use this)
                count += 1
    
    