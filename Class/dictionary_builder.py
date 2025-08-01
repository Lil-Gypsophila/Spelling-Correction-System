"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 24/12/2024

Module to build the dictionary
"""

import os
import nltk

from Class.corpus_builder import CorpusBuilder
from Class.tokens_cleaning import TokenCleaner

class DictionaryBuilder:
    
    def __init__(self, dict_cache_file = 'dictionary.txt', psy_dict_cache_file = 'psychology_dictionary.txt'):
        
        # Directory to store dictionary files
        self.dict_dir = "Dictionary"
        os.makedirs(self.dict_dir, exist_ok=True)

        # Define full paths for dictionary files
        self.dict_cache_file_path = os.path.join(self.dict_dir, dict_cache_file)
        self.psy_dict_cache_file_path = os.path.join(self.dict_dir, psy_dict_cache_file)

        # Check if the cache files need to be rebuilt
        if (not os.path.exists(self.dict_cache_file_path) or os.path.getsize(self.dict_cache_file_path) == 0 or
            not os.path.exists(self.psy_dict_cache_file_path) or os.path.getsize(self.psy_dict_cache_file_path) == 0):

            # Initialise Classes
            token_cleaner = TokenCleaner()
            corpus_builder = CorpusBuilder()

            # Get corpus 
            cleaned_body_text = corpus_builder.merge_cleaned_corpora()
            
            # Clean tokens
            cleaned_tokens = token_cleaner.clean_tokens_dict(cleaned_body_text.split())
            
            # Build dictionaries
            self.psy_dict = set(cleaned_tokens)
            general_eng_dict = set(w.lower() for w in nltk.corpus.words.words())
            self.dict = self.psy_dict.union(general_eng_dict)
            
            # Save dictionaries to files
            self._save_dictionary_to_file(self.dict, self.dict_cache_file_path)
            self._save_dictionary_to_file(self.psy_dict, self.psy_dict_cache_file_path)
            
        else:
            
            # Load dictionaries from cache files
            self.dict = self._load_dictionary_from_file(self.dict_cache_file_path)
            self.psy_dict = self._load_dictionary_from_file(self.psy_dict_cache_file_path)

    
    # Function to save dictionary to a file
    def _save_dictionary_to_file(self, dictionary, file_path):
        with open(file_path, 'w', encoding='UTF-8') as f:
            for word in sorted(dictionary):  # Save in sorted order for consistency
                f.write(word + '\n')

    
    # Function to load dictionary from file
    def _load_dictionary_from_file(self, file_path):
        with open(file_path, 'r', encoding='UTF-8') as f:
            return set(line.strip() for line in f)

    
    # Function to add new words to dictionary
    def add_word_to_dict(self, word):
        word = word.lower()
        if word not in self.dict:
            self.dict.add(word)
            with open(self.dict_cache_file_path, 'a', encoding = 'UTF-8') as f:
                f.write(word + '\n')

    
    # Function to get dictionary
    def get_dict(self):
        return self.dict

    
    # Function to get sorted dictionary
    def get_sorted_dict(self):
        return sorted(self.dict)

    
    # Function to get psychology dictionary
    def get_psy_dict(self):
        return self.psy_dict