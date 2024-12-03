#imports needed
import os
import io
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
    https://docs.python.org/3/library/io.html

    As I was working through this, kept running into issues with images not saving right.
    To avoid this issues, going to change colors around and set the turtle background to white instead.

    """
    colors = ["red", "orange", "#B0578D","#3E001F","#7A316F","#624E88","#6A1E55","#C65BCF",
            "#91D18B", "#243D25", "#5F7464"]
    #colors = ["white","red", "yellow", "orange","#f8df81", "#f6aa90", "#f6b4bf", "#d5b6d5",
    #        "#badfda", "#9bd0b7", "#F2BFD7", "#F6D7E8", "#DCD0EA", "#F2E8CE", "#F1DCC5"]
    
    #init list for frames for saving the gif
    gif_frames = []

    # make canvas
    canvas = t.Screen()
    canvas.mode("world")
    canvas.setworldcoordinates(0,0,w,h)
    canvas.bgcolor("white")

    # making pencil
    pencil = t.Turtle()
    pencil.speed(0)
    pencil.pensize(1)
    pencil.penup()
    canvas.tracer(0)

    #begin drawing process
    # adding a frame capture interval to speed up the process of drawing coords and saving
    #capture every 5th move (this may be adjusted)

    frameCapInterval = 10

    #we're gonna edit the original drawing portion
    for i, line in enumerate(coordinates):
        
        temp = line[0]
        temp[1] = h - temp[1]
        pencil.goto(temp)
        pencil.color(random.choice(colors))

        # start draw
        for j, spot in enumerate(line):
            pencil.pendown()
            if spot == line[0]:
                spot[1] = h - spot[1]
            
            spot[1] = h - spot[1]
            pencil.goto(spot)

            #here we are going to capture the frame every nth(whichever val we decide on)
            if j % frameCapInterval == 0:
                # capture the current frame/drawing result for the GIF
                # here we use ps since turtle doesnt allow for jpg/png saving natively
                # saving the color as well
                #canvas.getcanvas().postscript(file="processed/frame.ps", colormode='color')
                # for optimization sake we are gonna comment out this line and switch it 
                psData = canvas.getcanvas().postscript(colormode="color")
                # converting the .ps file to RGBA
                #frame = Image.open("processed/frame.ps").convert("RGBA")
                # ^ for opti sake, swapping this line so we don't need to worry about PIL opening and closing files over and over
                #using BytesIO to speed up program so that we dont need to work with the filesystem
                #also makes more sense to avoid clutter, and since our data is temp
                gifFrame = Image.open(io.BytesIO(psData.encode())).convert("RGBA")
                #create a new black background image so we can save results with the black background
                # to ensure that it is a fully opaque black background, rather than using "black" we're 
                # gonna use (0,0,0,255)
                # https://johndecember.com/html/spec/colorrgbadec.html
                #background = Image.new("RGBA", (w,h), (0,0,0,255))
                #using alpha composite 
                #gifFrame = Image.alpha_composite(background, frame)
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
    #canvas.getcanvas().postscript(file="processed/results.ps", colormode='color')
    #results = Image.open("processed/results.ps").convert("RGBA")
    finalPSData = canvas.getcanvas().postscript(colormode="color")
    results = Image.open(io.BytesIO(finalPSData.encode())).convert("RGBA")
    #background = Image.new("RGBA", (w,h), (0,0,0,255))
    #finalImg = Image.alpha_composite(background, results)
    results.save(f"processed/{finalImgName}_drawing.png")

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
    
    