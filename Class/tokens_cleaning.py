"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 30/12/2024

Module to Clean the Tokens from the Corpus
"""

import re
import string

class TokenCleaner:

    # Function to get punctuations
    def get_punctuations(self):
        # Include common punctuations and expand with custom ones
        punct = set(string.punctuation)
        punct.update({'....', '--', '-', '“', '”', '’', '‘', '€', '”', '…', '–', '—'})
        return punct

    # Function to remove leading and trailing underscores
    def remove_leading_underscore(self, token):
        return re.sub(r'^_+|_+$', '', token)

    # Function to remove numeric characters from a token
    def remove_numeric_characters(self, token):
        return re.sub(r'\d', '', token)

    # Function to clean tokens for dictionary
    def clean_tokens_dict(self, tokens):
        punctuations = self.get_punctuations()
        cleaned_tokens = []
        
        for token in tokens:
            # Remove URLs
            token = re.sub(r'http[s]?://\S+', '', token)  # Remove HTTPS URLs
            token = re.sub(r'www\.\S+', '', token)        # Remove WWW URLs
            
            # Remove special characters that don't form meaningful words
            token = re.sub(r'[^\w\s]', '', token)  # Remove all non-alphanumeric characters except spaces
            
            # Remove numeric characters and other unwanted patterns
            token = self.remove_leading_underscore(token)  # Clean leading/trailing underscores
            token = self.remove_numeric_characters(token) if self.contains_number(token) else token
            token = token.strip('-').lower()  # Remove leading dashes and convert to lowercase
            
            # Ensure token is not empty and not in punctuations
            if token and token not in punctuations:
                cleaned_tokens.append(token)

        return cleaned_tokens

    # Function to clean tokens for n-gram model
    def clean_tokens_n_gram(self, tokens):
        punctuations = self.get_punctuations()
        cleaned_tokens = []
        
        for token in tokens:
            # Remove URLs
            token = re.sub(r'http[s]?://\S+', '', token)
            token = re.sub(r'www\.\S+', '', token)
            
            # Remove special characters that don't form meaningful words
            token = re.sub(r'[^\w\s]', '', token)  # Remove all non-alphanumeric characters except spaces
            
            # Additional cleaning steps
            token = self.remove_leading_underscore(token)
            token = token.strip('-')  # Remove leading dashes
            token = token.strip('\'') if token != "'s" else token  # Keep possessive "'s"
            token = token.lower()  # Convert to lowercase
            
            # Ensure token is not empty and not in punctuations
            if token and token not in punctuations:
                cleaned_tokens.append(token)

        return cleaned_tokens
    
    # Function to clean input tokens
    def clean_input_tokens(self, tokens_map):
        
        punctuations = self.get_punctuations()
        cleaned_tokens_map = [(token, indexes) for (token, indexes) in tokens_map if token not in punctuations]
        cleaned_tokens_map = [(token.lower(), indexes) for (token, indexes) in cleaned_tokens_map]
        cleaned_tokens_map = [(token, indexes) for (token, indexes) in cleaned_tokens_map if token != '']
        
        return cleaned_tokens_map

    # Helper functions
    def contains_number(self, token):
        return bool(re.search(r'\d', token))
