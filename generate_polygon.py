
import sys
import cv2
import numpy
import copy
import scipy.misc
import itertools
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import morphology, label
from copy import deepcopy
from operator import itemgetter
from statistics import median, mean
from math import sqrt
from random import randint
from scipy.misc import toimage



# generation parameters (CAN CHANGE)
num_rect = randint(5, 15)
canvas_width = 20
canvas_height = 20
min_size = 1
max_size = 5
increments = 100



# Basic vision
orig = Image.open(sys.argv[1])                      # must feed in blank, black canvas image as input (blank.png)
img = ImageOps.grayscale(orig)
im = numpy.array(img)
im = morphology.grey_dilation(im, (3, 3)) - im      # inner morphological gradient
img = Image.fromarray(im)
visual = img.convert('RGB')
draw = ImageDraw.Draw(visual)



# Generate random number of rectangles (must be touching) of random sizes
boxes = []
for i in range(num_rect):
    valid = 0
    while(valid == 0):
        width = randint(min_size, max_size)*increments
        height = randint(min_size, max_size)*increments
        pos_x = randint(max_size+1, canvas_width-max_size-1)*increments
        pos_y = randint(max_size+1, canvas_height-max_size-1)*increments
        for j in boxes:
            touching = 1
            if (pos_x+(width/2.0) < j[0]-(j[2]/2.0)):
                touching = 0
            if (pos_x-(width/2.0) > j[0]+(j[2]/2.0)):
                touching = 0
            if (pos_y+(height/2.0) < j[1]-(j[3]/2.0)):
                touching = 0
            if (pos_y-(height/2.0) > j[1]+(j[3]/2.0)):
                touching = 0
            if touching == 1:
                valid = 1
        if len(boxes) == 0:
            valid = 1
    boxes.append([pos_x,pos_y,width,height])



# Extend those that stick out to the ground
bottom_ground = 0
for i in boxes:
    if (i[1] + (i[3]/2.0)) > bottom_ground:
        bottom_ground = (i[1] + (i[3]/2.0))

for i in range(len(boxes)):
    bottom_left = [boxes[i][0]-(boxes[i][2]/2.0),boxes[i][1]+(boxes[i][3]/2.0)]
    bottom_right = [boxes[i][0]+(boxes[i][2]/2.0),boxes[i][1]+(boxes[i][3]/2.0)]
    line_check = [bottom_left,bottom_right]
    intersect = 0
    for j in range(len(boxes)):
        if i!=j:
            p1 = [boxes[j][0]-(boxes[j][2]/2.0),boxes[j][1]-(boxes[j][3]/2.0)-1]
            p2 = [boxes[j][0]-(boxes[j][2]/2.0),boxes[j][1]+(boxes[j][3]/2.0)+1]
            p3 = [boxes[j][0]+(boxes[j][2]/2.0),boxes[j][1]-(boxes[j][3]/2.0)-1]
            p4 = [boxes[j][0]+(boxes[j][2]/2.0),boxes[j][1]+(boxes[j][3]/2.0)+1]
            line_check2 = [p1,p2]
            line_check3 = [p3,p4]
            if (line_check[0][0] < line_check2[0][0]) and (line_check[1][0] > line_check2[0][0]):
                if (line_check[0][1] > line_check2[0][1]) and (line_check[0][1] < line_check2[1][1]):
                    intersect = 1
            if (line_check[0][0] < line_check3[0][0]) and (line_check[1][0] > line_check3[0][0]):
                if (line_check[0][1] > line_check3[0][1]) and (line_check[0][1] < line_check3[1][1]):
                    intersect = 1
            if (line_check[0][0] > line_check2[0][0]) and (line_check[1][0] > line_check2[0][0]):
                if (line_check[0][0] < line_check3[0][0]) and (line_check[1][0] < line_check3[0][0]):
                    if (line_check[0][1] > line_check2[0][1]) and (line_check[0][1] < line_check2[1][1]):
                        intersect = 1
    if intersect == 0:
        current_bottom = boxes[i][1] + (boxes[i][3]/2.0)
        to_add = bottom_ground-current_bottom
        boxes[i][3] = boxes[i][3] + to_add
        boxes[i][1] = boxes[i][1] + (to_add/2.0)
        


# Draw resulting rectangles as image
for i in boxes:
    print(i)
    top_left = (i[0]-(i[2]/2.0),i[1]-(i[3]/2.0))
    bottom_right = (i[0]+(i[2]/2.0),i[1]+(i[3]/2.0))
    draw.rectangle((top_left,bottom_right), fill='white')
visual.save("output.jpg")



