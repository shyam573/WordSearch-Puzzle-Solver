# -*- coding: utf-8 -*-
"""
Created by Shyam Chanduri
MIT License
"""

from utils import get_dir_dict
import pandas as pd

class WordSearch():
    
    def __init__(self, orig_array, target_words):
        self.orig_array = orig_array
        self.target_words = target_words
        self.orig_length = len(self.orig_array)
        self.res_words = target_words
        self.dir_dict = get_dir_dict()
        

    def get_search_letters(self, target_words):
        search_letters = []
        for word in target_words:
            if word[0] not in search_letters:
                search_letters.append(word[0])
                
        return search_letters
    

    def get_dir_string(self, index, direction):
        output_word = [self.letter]
        for i in range(1, self.max_len):
            first_index = int(self.dir_dict[direction][0] * i) + index[0]
            second_index = int(self.dir_dict[direction][1] * i) + index[1]
            if (first_index >= 0 and first_index < self.orig_length and second_index >= 0 and second_index < self.orig_length):
                output_word.append(self.orig_array[first_index][second_index])
            else:
                pass
            
        output_word = "".join(output_word)
        return output_word
    
    
    def search_around(self, index, letter):
        self.letter = letter
        cur_search_words = [word for word in self.target_words if word[0]==self.letter]
        self.max_len = len(max(cur_search_words, key = len))
        
        for direction in list(self.dir_dict):
            output_word = self.get_dir_string(index, direction)
            for target_word in self.res_words:
                if target_word in output_word:
                    extra_steps = output_word.index(target_word)
                    first_index = int(self.dir_dict[direction][0] * extra_steps) + index[0]
                    second_index = int(self.dir_dict[direction][1] * extra_steps) + index[1]
                    self.res_words = list(set(self.res_words) - set(target_word))
                    new_row = {'word':target_word, 'row':first_index, 'col':second_index, 'direction':direction}
                    self.answers = self.answers.append(new_row, ignore_index=True)
                
                    
    def finder(self):
        self.answers = pd.DataFrame(columns=['word', 'row', 'col', 'direction'])
        search_letters = self.get_search_letters(self.target_words)
        for i in range(self.orig_length):
            for j in range(self.orig_length):
                if self.orig_array[i][j] in search_letters:
                    self.search_around((i,j), self.orig_array[i][j])
                                  
        return self.answers.drop_duplicates()












