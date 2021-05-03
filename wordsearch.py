# -*- coding: utf-8 -*-
"""
Created by Shyam Chanduri
MIT License
"""


# orig_array = [["A", "B", "C", "Z"],
#               ["D", "E", "F", "Y"],
#               ["G", "H", "I", "Y"],
#               ["A", "B", "C", "Z"]]

# target_words = ["EA", "EI", "BD", "HI", "IFC", "IHG", "AEI"]



# orig_array_1 = [['U', 'D', 'U', 'S', 'T', 'N', 'Y', 'A', 'Z'],
#               ['L', 'H', 'H', 'K', 'O', 'M', 'C', 'G', 'A'],
#               ['I', 'F', 'O', 'B', 'E', 'A', 'Y', 'W', 'N'],
#               ['A', 'O', 'G', 'N', 'R', 'A', 'M', 'B', 'X'],
#               ['C', 'S', 'D', 'D', 'L', 'O', 'Z', 'V', 'W'],
#               ['F', 'I', 'H', 'P', 'P', 'B', 'P', 'O', 'F'],
#               ['B', 'R', 'C', 'X', 'S', 'O', 'Q', 'Y', 'Y'],
#               ['G', 'P', 'Y', 'D', 'U', 'T', 'S', 'N', 'X'],
#               ['U', 'V', 'L', 'E', 'J', 'A', 'O', 'Z', 'T']]

# target_words_1 = ["DUST", "COOK", "DO", "GO", "PLAY", "STUDY"]

from utils import get_dir_dict

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
        
        search_result = {}
        for direction in list(self.dir_dict):
            output_word = self.get_dir_string(index, direction)
            for target_word in self.res_words:
                if target_word in output_word:
                    extra_steps = output_word.index(target_word)
                    first_index = int(self.dir_dict[direction][0] * extra_steps) + index[0]
                    second_index = int(self.dir_dict[direction][1] * extra_steps) + index[1]
                    res_index = (first_index, second_index)
                    search_result.update({target_word: (res_index, direction)})
                    self.res_words = list(set(self.res_words) - set(target_word))
                    
        return search_result
                
    
    def finder(self):
        
        answers_dict = {}
        search_letters = self.get_search_letters(self.target_words)
        for i in range(self.orig_length):
            for j in range(self.orig_length):
                if self.orig_array[i][j] in search_letters:
                    search_result = self.search_around((i,j), self.orig_array[i][j])
                    answers_dict.update(search_result)
                                    
        return answers_dict

                    
                
# sample =  WordSearch(orig_array, target_words)
# print(sample.finder())

# sample_1 =  WordSearch(orig_array_1, target_words_1)
# print(sample_1.finder())











