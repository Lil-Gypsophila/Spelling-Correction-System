"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 30/12/2024

Module to Extract Text from the Corpus

link to the corpus:
https://archive.org/download/psychology_collection_202309
"""

import os
import re
import logging

class CorpusBuilder:

    # Initialisation to avoid potential undefined variable errors
    def __init__(self):
        self.text = ""
        self.corpus_dir = os.path.join("Corpora", "raw")    # Directory for raw text
        self.processed_dir = os.path.join("Corpora", "processed")   # Directory for processed text
        os.makedirs(self.processed_dir, exist_ok = True)
        logging.basicConfig(level = logging.INFO)   # Logging for debugging


    # Function to read the text from corpus
    def read_text(self):

        self.text = ""

        # Defining all the books
        files = [
            "INTRODUCTION TO PSYCHOLOGY.txt",
            "HOW TO ANALYZE PEOPLE WITH DARK PSYCHOLOGY.txt",
            "MOH.txt"
        ]

        # Reading all the defined books
        for file_name in files:
            
            # Define the file path
            file_path = os.path.join(self.corpus_dir, file_name)
            
            try:
                with open(file_path, 'r', encoding = 'UTF-8') as f:
                    self.text += f.read() + "\n"  # Append contents with a separator
            
            except FileNotFoundError:
                
                logging.warning(f"File {file_name} not found in {self.corpus_dir}. Skipping.")

            except Exception as e:

                logging.error(f"Error reading {file_name}: {e}. Skipping.")


    # Extracts main content between specified start and end markers
    def extract_main_content(self, start_marker, end_marker):

        # Find all occurrences of the start marker
        start_matches = list(re.finditer(start_marker, self.text, re.IGNORECASE))
    
        # Check if at least two occurrences exist
        if len(start_matches) < 2:

            logging.error("Second occurrence of the start marker not found.")

            return "Second occurrence of the start marker not found."

        # Find the start position
        start_pos = start_matches[1].start()
       
        # Find the end position
        end_pos = self.text.find(end_marker)
    
        if end_pos == -1:
            logging.error("End marker not found.")
            return "End marker not found."
    
        # Extract contents between start and end position
        body_text = self.text[start_pos:end_pos].strip()

        return body_text


    # Function to clean the text in the corpus
    def text_cleaning(self, body_text):
        
        # Clean ED
        cleaned_text = re.sub(r'\s*--\s*ED\s*\.\s*', '', body_text)

        # Replace '-' with space
        cleaned_text = re.sub(r'-', ' ', cleaned_text)

        # Remove extra spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

        return cleaned_text


    # Get clean main contents and save to a file
    def get_clean_contents(self, start_marker, end_marker, cache_file = 'cleaned_main_contents.txt'):

        cache_file_path = os.path.join(self.processed_dir, cache_file)

        if os.path.exists(cache_file_path) and os.path.getsize(cache_file_path) > 0:
            logging.info(f"Using cached file: {cache_file_path}")
            with open(cache_file_path, 'r', encoding='UTF-8') as f:
                return f.read()

        self.read_text()
        body_text = self.extract_main_content(start_marker, end_marker)
        if "not found" in body_text:
            return body_text

        cleaned_body_text = self.text_cleaning(body_text)
        with open(cache_file_path, 'w', encoding='UTF-8') as f:
            f.write(cleaned_body_text)

        return cleaned_body_text


    # Function to merge cleaned corpus
    def merge_cleaned_corpora(self):
        
        # Get cleaned contents for each corpus
        contents = [
            
            # Corpus 1
            self.get_clean_contents(
                start_marker = r'Chapter 1: What is Manipulation?',
                end_marker = "END OF INTRODUCTION TO PSYCHOLOGY",
                cache_file = "corpus1_cleaned.txt"
            ),

            # Corpus 2
            self.get_clean_contents(
                start_marker = r'Chapter 1: The Dark Side of Psychology',
                end_marker = "END OF HOW TO ANALYZE PEOPLE WITH DARK PSYCHOLOGY",
                cache_file = "corpus2_cleaned.txt"
            ),

            # Corpus 3
            self.get_clean_contents(
                start_marker = r'Chapter 1: Delving into Dark Psychology',
                end_marker = "END OF MOH",
                cache_file = "corpus3_cleaned.txt"
            ),
        ]

        # Merge all 3 corpus into a single corpus
        merged_corpus = "\n".join(contents)
        merged_file_path = os.path.join(self.processed_dir, "merged_cleaned_corpus.txt")

        with open(merged_file_path, 'w', encoding='UTF-8') as f:
            f.write(merged_corpus)

        logging.info(f"Merged corpus saved at {merged_file_path}")

        return merged_corpus
        