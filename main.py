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

import gradio as gr


def run_app(img):
    ### reading the input image
    input_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#read_image(img)
    
    ### find contours to detec tregions of interest
    contours = find_contours(input_image)
    
    ### Puzzle is assumed to be largest contour and traget words as second largest
    first, second = n_largestcontours(contours,num=2)
    
    ### get target words
    target_words_img = get_cropped_image(input_image, second)
    target_words = wordsfromimage(target_words_img, config=r'--psm 3 --oem 3')
    
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
    words_count = str(len(answers)) + "/" + str(len(target_words))
    return out_image, target_words, words_count, answers


input_image = gr.inputs.Image(image_mode="RGB", label="Input Puzzle")
solved_image = gr.outputs.Image(type="auto", label="Solved Puzzle")
detected_words =  gr.outputs.Textbox(type="auto", label="Words detected")
num_words =  gr.outputs.Textbox(type="auto", label="Number of Words - Detected/Found")
answers = gr.outputs.Dataframe(type="pandas", label="Words and their directions")

iface = gr.Interface(fn=run_app, 
                     inputs=[input_image], 
                     outputs=[solved_image, detected_words, num_words, answers],
                     examples = "test_images/", 
                     title="Wordsearch Solver",
                     description="This is a wordsearch solver tool.\
                         You can begin with a test image given below \
                             and visualise the result. On an average, \
                                 it takes 30 secs (may vary on number of input words). \
                                     Get started with your own images now.",
                     theme="default")


if __name__ == "__main__":
    iface.launch(inbrowser=True, share=False)