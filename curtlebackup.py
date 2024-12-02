#imports needed
import os

#importing for image wrangling
import numpy as np
#import pandas as pd
#importing OpenCV
import cv2
#importing PIL for image saving portion and gif saving
from PIL import Image
#turtle mod
import turtle as t
import random

"""
Error notes: 
    If you recieve an error "OSError: Unable to locate Ghostscript on paths" you wioll need to install ghostscript
    1. Install Ghostscript for your OS
    2. Add Ghostscript to the system path (if it is not done automatically)
        - my path i will be adding to path looks like this "C:\Program Files (x86)\gs\gs10.04.0\bin"
        - you should only need the path to the bin folder
    3. verify installation
        - run gswin64c -version in cmd prompt
    4. restart and rerun
    """

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
def curtle_drawing(coordinates, h, w, finalImgName):
    """
    curtle will take in a coordinates list 
    coordinates list will be gotten from the contours function
    
    Image saving and gif saving portions will also be handled here
    Links:
    https://pillow.readthedocs.io/en/stable/reference/Image.html
    https://www.geeksforgeeks.org/python-pil-image-alpha_composite-method/
    https://www.geeksforgeeks.org/create-and-save-animated-gif-with-python-pillow/
    https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

    """

    colors = ["white","red", "yellow", "orange"]
    
    #init list for frames for saving the gif
    gif_frames = []

    # make canvas
    canvas = t.Screen()
    canvas.mode("world")
    canvas.setworldcoordinates(0,0,w,h)
    canvas.bgcolor("black")

    # making pencil
    pencil = t.Turtle()
    pencil.speed(0)
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

            # capture the current frame/drawing result for the GIF
            # here we use ps since turtle doesnt allow for jpg/png saving natively
            # saving the color as well
            canvas.getcanvas().postscript(file="frame.ps", colormode='color')
            # converting the .ps file to RGBA
            frame = Image.open("frame.ps").convert("RGBA")
            #create a new black background image so we can save results with the black background
            background = Image.new("RGBA", frame.size, "black")
            #using alpha composite 
            gifFrame = Image.alpha_composite(background, frame)
            # append the frame 
            gif_frames.append(gifFrame)

        #print ("endline")
        canvas.update()
        pencil.penup()
    
    #final canvas update
    canvas.tracer(1)
    canvas.update()

    # saving the final drawing result as an image before we continue 
    #similiar process to gif, only we will be saving the end version
    canvas.getcanvas().postscript(file="results.ps", colormode='color')
    results = Image.open("results.ps").convert("RGBA")
    background = Image.new("RGBA", results.size, "black")
    finalImg = Image.alpha_composite(background, results)
    finalImg.save(f"processed/{finalImgName}_drawing.png")

    #saving the stop-motion animated gif
    #we may need to adjust duration
    gif_frames[0].save(f"processed/{finalImgName}.gif", save_all=True,
                        append_images=gif_frames[1:], duration=10, loop=0)
    
    #input to continue to the next drawing process
    input("Press enter to continue: ")



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

                #generating our imagefinalname field to pass to curtle_drawing
                # this is just using our same count format
                saveImgName = f"results_{count}"
                #drawing function for image
                curtle_drawing(coords, cH, cW, saveImgName)

                #update count for sequential file formats(assuming we use this)
                count += 1
    
    