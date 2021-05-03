# -*- coding: utf-8 -*-
"""
Created by Shyam Chanduri
MIT License
"""

import cv2
import pytesseract
import numpy as np

from utils import *
from wordsearch import WordSearch


image_path = "test_images/word-search-12.png"

### reading the input image
input_image = read_image(image_path)

### find contours to detec tregions of interest
contours = find_contours(input_image)

### Puzzle is assumed to be largest contour and traget words as second largest
first, second = n_largestcontours(contours,num=2)

### get target words
target_words_img = get_cropped_image(input_image, second)
target_words = wordsfromimage(target_words_img, config=r'--psm 3 --oem 3')

colors = []
for i in range(len(target_words)):
    color = tuple(np.random.choice(range(256), size=3))
    colors.append(color)

### get puzzle words
puzzle_img = get_cropped_image(input_image, first)
puzzle_contours = find_contours(puzzle_img, close=False)

contour_map = {}
last_puz_ind = len(puzzle_contours)-1
detections = []
for i,cnt in enumerate(puzzle_contours):
    contour_map[last_puz_ind-i] = cnt    ### storing in reverse order which will be corrected later
    cropped_image = get_cropped_image(puzzle_img, cnt)
    txt = wordsfromimage(cropped_image, config=r'--psm 10')
    detections.append(txt)

rows = cols = int(np.sqrt(len(detections)))  ##assuming square puzzle
puzzle_words = get_pzlwords(detections, (rows, cols))


### Find answers from puzzle
answers_search = WordSearch(puzzle_words, target_words)
answers = answers_search.finder()

puzzle_img = cv2.cvtColor(puzzle_img, cv2.COLOR_GRAY2RGB)
out_image = highlight_contours(puzzle_img, answers, contour_map, rows)

cv2.imshow("image", out_image)
cv2.waitKey(0)

#print(answers)