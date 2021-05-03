# -*- coding: utf-8 -*-
"""
Created by Shyam Chanduri
MIT License
"""


import cv2
import numpy as np
import pytesseract

import itertools


def read_image(imagepath):
    image = cv2.imread(imagepath)
    if len(image.shape) != 2:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    return image
    

def find_contours(image, close=True):
    ret, thresh = cv2.threshold(image, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    if close:
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50,30)))
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(thresh, rect_kernel, iterations=1)
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)     
    
    return contours


def n_largestcontours(contours, num=2):
    areas = [cv2.contourArea(c) for c in contours]
    areas_sorted = sorted(range(len(areas)), key=lambda x: areas[x])
    largest_indices = areas_sorted[-num:]
    largest_cnts = [contours[i] for i in largest_indices][::-1]
    
    return largest_cnts


def get_cropped_image(image, contour):
    x, y, w, h = cv2.boundingRect(contour)
    cropped_image = image[y:y + h, x:x + w] 
    
    return cropped_image


def wordsfromimage(image, config):
    text = pytesseract.image_to_string(image, config=config)
    words = text.split("\n")
    words = [word.upper() for word in words if word.isalpha()]
    
    return words


def get_pzlwords(detections, shape):
    puzzle_words = list(itertools.chain.from_iterable(detections))[::-1]
    puzzle_words = [puzzle_words[i][0] for i in range(len(puzzle_words))]
    puzzle_words = np.array(puzzle_words).reshape(shape)
    return puzzle_words

def get_dir_dict():
    
    return {"right" : (0,1),
            "right_down" : (1,1),
            "down" : (1,0),
            "left_down" : (1,-1),
            "left" : (0,-1),
            "top_left" : (-1,-1),
            "top" : (-1,0),
            "top_right" : (-1,1)}
    
     
def highlight_contours(image, answers, contour_map, rows):
    
    dir_dict = get_dir_dict()
    for key in answers:
        num_contours = len(key)
        dir_index  = dir_dict[answers[key][1]] 
        curr_index = answers[key][0]
        net_index = rows * curr_index[0] + curr_index[1]
        cur_cnt = contour_map[net_index]
        x,y,w,h = cv2.boundingRect(cur_cnt)
        cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), -1)
     
        for i in range(num_contours-1):
            
            curr_index = tuple(map(sum, zip(curr_index, dir_index)))
            net_index = rows * curr_index[0] + curr_index[1]
            cur_cnt = contour_map[net_index]
            x,y,w,h = cv2.boundingRect(cur_cnt)
            cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), -1)

        
    return image


            
    
    
    
    
    
    
    
    
    
    
    
    