# Curtle - AI Robotics
 AI Robotics Final Project of an image copying turtle 

## Project Goals:
1. Be able to batch process and apply binary thresholding to a myriad number of images using a single image processing function
2. Using the binary images, extract the contours and their coordinates
3. Using the contour coordinates extracted, redraw a processed image using the Python Turtle Module
4. Be able to save the finalized results of the drawing and be able to save the drawing process as a gif


## Methods and Libraries Used:
### Libraries:
1. OpenCV - for image processing and contour extraction
2. Pillow (aka PIL) - for final result image saving and the gif creation
3. Python Turtle - for the image drawing portion

### Methods and Algorithms:
1. OpenCV's adaptive thresholding using the mean method.
2. OpenCV's findContours function using the RETR_LIST mode and CHAIN_APPROX_NONE method

## Curtle's Process Outline:
1. Image Processing:
    - Curtle's image processing contains of a few steps:
    1. Grayscale conversion
    2. Add a blur to our grayscale image
    3. Apply Adaptive Mean Thresholding
2. Extract contours and their coordinates to pass to our drawing function
3. Use Python's Turtle Module to redraw coordinates, coupled with PIL to save final results and GIF of the drawing process

## Further Work and Improvements:
1. In regards to possible future work on Curtle, we would like to find a way to apply Canny Edge Detection so that we can compare our current results to what a Canny implementation's results would look like.

## Errors and How to Handle Them:
- If you recieve an error "OSError: Unable to locate Ghostscript on paths" you should be able to solve it by doing the following:
    1. Install Ghostscript for your corresponding OS at this link: https://ghostscript.com/releases/gsdnld.html
    2. Add Ghostscript to the system path (if it is not added automatically)
    3. Verify installation
    4. Restart and rerun Curtle

## References:
Abhishek. (2024, March 28). Canny edge detection: Explained and compared with opencv in python. Medium. https://medium.com/@abhisheksriram845/canny-edge-detection-explained-and-compared-with-opencv-in-python-57a161b4bd19
Anastasia Murzova    Sakshi Seth, Murzova, A., & Seth, S. (2021, May 5). Otsu’s Thresholding Technique. LearnOpenCV. https://learnopencv.com/otsu-thresholding-with-opencv/
Contours: Getting Started. OpenCV. (n.d.-a). https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html
Image Thresholding. OpenCV. (n.d.-b). https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
Rosebrock, A. (2023, June 9). Adaptive Thresholding with opencv ( cv2.adaptivethreshold ). PyImageSearch. https://pyimagesearch.com/2021/05/12/adaptive-thresholding-with-opencv-cv2-adaptivethreshold/
Vipin. (2024, October 14). Contour detection in opencv: A comprehensive guide. Medium. https://medium.com/thedeephub/mastering-contouring-in-opencv-a-comprehensive-guide-10e6fe2a069a 
## Image References:
Bulbapedia. (2024, September 27). Fuecoco (pokémon). https://bulbapedia.bulbagarden.net/wiki/Fuecoco_%28Pok%C3%A9mon%29
Carpenter, N. (2019, October 9). Pokemon’s developers just want us to take care of Sobble. Polygon. https://www.polygon.com/2019/10/9/20907051/pokemon-sword-shield-three-starter-pokemon-info
Gilliam, R. (2021, September 23). New Kirby game for Switch Leaks ahead of Nintendo Direct. Polygon. https://www.polygon.com/22689856/kirby-nintendo-switch-direct-leak-discovery-stars
Hillenburg, Stephen. “SpongeBob Square Pants.” (2)
Marks, T. (2022, March 24). Kirby and the Forgotten Land Review. IGN. https://www.ign.com/articles/kirby-and-the-forgotten-land-review 