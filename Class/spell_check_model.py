"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 30/12/2024

Module to Build the Spelling Checker Model
"""

import nltk
from nltk.util import pad_sequence
from nltk import bigrams, trigrams
from nltk.corpus import wordnet

from metaphone import doublemetaphone
from textblob import Word

from Class.corpus_builder import CorpusBuilder
from Class.tokens_cleaning import TokenCleaner
from Class.dictionary_builder import DictionaryBuilder
from Class.n_gram_model import NGramModel


class SpellCheckModel:

    def __init__(self, dict, psy_dict, bi_weight, bi_right_weight, tri_weight, threshold,
                 edit_distance_weight=1, double_metaphone_weight=1, context_score_weight=0.5, n_candidate=10):
       
        # Initialize dictionary
        self.dict = dict
        self.psy_dict = psy_dict

        # Initialize N-Gram models
        n_gram_model = NGramModel()
        self.unigram_model, self.bigram_model, self.right_bigram_model, self.trigram_model = n_gram_model.n_gram_model()

        # Set hyperparameters
        self.bi_weight = bi_weight
        self.bi_right_weight = bi_right_weight
        self.tri_weight = tri_weight
        self.threshold = threshold
        self.edit_distance_weight = edit_distance_weight
        self.double_metaphone_weight = double_metaphone_weight
        self.context_score_weight = context_score_weight
        self.n_candidate = n_candidate

        # Token Cleaner
        self.token_cleaner = TokenCleaner()


    # Function to update the dictionary
    def update_dict(self, new_dict):
        self.dict = new_dict


    # Function to compute Damerau-Levenshtein
    def dl_dist(self, s1, s2):
        
        d = {}
        lenstr1, lenstr2 = len(s1), len(s2)

        # Initialize the distance matrix
        for i in range(-1, lenstr1 + 1):
            d[(i, -1)] = i + 1
        for j in range(-1, lenstr2 + 1):
            d[(-1, j)] = j + 1

        # Compute distances
        for i in range(lenstr1):
            for j in range(lenstr2):
                cost = 0 if s1[i] == s2[j] else 1
                d[(i, j)] = min(
                    d[(i - 1, j)] + 1,  # Deletion
                    d[(i, j - 1)] + 1,  # Insertion
                    d[(i - 1, j - 1)] + cost  # Substitution
                )
                if i and j and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                    d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # Transposition

        return d[lenstr1 - 1, lenstr2 - 1]
    
    
    # Compute double metaphone distance for candidates
    def get_double_metaphone_dist(self, error_token, candidates):

        error_token_encoding = doublemetaphone(error_token)

        for candidate in candidates:
            token_encoding = doublemetaphone(candidate["token"])

            candidate["double_metaphone_distance"] = sum(
                1 if token_encoding[i] != error_token_encoding[i] else 0
                for i in range(2)
            )

        return candidates
   
    # Formulate correction candidates
    def formulate_candidate(self, error_token, error_bigram, error_bigram_right, error_trigram):

        candidates = []

        for token in self.psy_dict:
            edit_dist = self.dl_dist(error_token, token)
            if edit_dist <= 3:  # Limit to an edit distance of 3
                candidates.append({"token": token, "edit_dist": edit_dist})

        filtered_candidates = []

        for candidate in candidates:

            token = candidate["token"]
            bigram = (error_bigram[0], token)
            bigram_right = (token, error_bigram_right[1])
            trigram = (error_trigram[0], error_trigram[1], token)

            bigram_prob = self.bigram_model(bigram)[1]
            bigram_right_prob = self.right_bigram_model(bigram_right)[1]
            trigram_prob = self.trigram_model(trigram)[1]

            weighted_prob = self.bi_weight * bigram_prob + \
                            self.bi_right_weight * bigram_right_prob + \
                            self.tri_weight * trigram_prob

            if weighted_prob >= self.threshold:
                candidate["context_score"] = weighted_prob
                filtered_candidates.append(candidate)

        # Calculate double metaphone distances for remaining candidates
        final_candidates = self.get_double_metaphone_dist(error_token, filtered_candidates)
        
        # Rank candidates based on combined weights
        final_candidates = sorted(

            final_candidates,

            key = lambda x: (
                self.double_metaphone_weight * x["double_metaphone_distance"] +
                self.edit_distance_weight * x["edit_dist"] -
                self.context_score_weight * x["context_score"]
            )
        )
        return [candidate["token"] for candidate in final_candidates[:self.n_candidate]]


    # Detect spelling errors in the text
    def error_detection(self, text):

        sentences = nltk.sent_tokenize(text)
        offset = 0
        non_word_errors = []
        real_word_errors = []
        id = 0

        # Process each sentence
        for sentence in sentences:
            tokens_with_positions = []
            tokens = nltk.word_tokenize(sentence)

            # Tokenization
            for token in tokens:    # Create token records with the position information
                start_pos = text.find(token, offset)
                end_pos = start_pos + len(token)
                tokens_with_positions.append((token, (start_pos, end_pos)))
                offset = end_pos

            # Clean tokens
            cleaned_tokens_with_positions = self.token_cleaner.clean_input_tokens(tokens_with_positions)

            # Padding for bigram and trigram context
            cleaned_tokens = [token for (token, indexes) in cleaned_tokens_with_positions]
            cleaned_tokens_pad_2 = list(nltk.pad_sequence(cleaned_tokens, 2, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))
            cleaned_tokens_pad_3 = list(nltk.pad_sequence(cleaned_tokens, 3, pad_left=True, pad_right=True, left_pad_symbol='<s>', right_pad_symbol='</s>'))

            # Create n-grams
            bigrams = list(nltk.bigrams(cleaned_tokens_pad_2))
            trigrams = list(nltk.trigrams(cleaned_tokens_pad_3))

            # Detect errors for each token
            for i in range(len(cleaned_tokens)):

                # get the token and position
                token = cleaned_tokens[i]
                start_pos = cleaned_tokens_with_positions[i][1][0]
                end_pos = cleaned_tokens_with_positions[i][1][1]

                # get the n-grams
                bigram = bigrams[i]
                bigram_next = bigrams[i + 1]
                trigram = trigrams[i]

                # check for non-word error with dictionary and != <numeric_token>:
                if token not in self.dict and token != "<numeric_token>":

                    # check for lemma
                    w = Word(token)
                    lemma = w.lemmatize()

                    if lemma not in self.dict:  # if word, lemma not in dictionary and its not a number

                        # non word error detected
                        candidates = self.formulate_candidate(token, bigram, bigram_next, trigram)
                        error = {
                            "id": "NON_WORD_" + str(id),
                            "error_token": token,
                            "position": (start_pos, end_pos),
                            "candidates": candidates
                        }
                        id += 1
                        non_word_errors.append(error)
                        continue

                # Check for real-word errors based on n-gram probabilities
                bigram_prob = self.bigram_model(bigram)[1]
                bigram_next_prob = self.right_bigram_model(bigram_next)[1]
                trigram_prob = self.trigram_model(trigram)[1]

                # weighted score
                weighted_prob = self.bi_weight * bigram_prob + self.bi_right_weight * bigram_next_prob + self.tri_weight * trigram_prob

                # if weighted probability is less than threshold
                if weighted_prob < self.threshold:
                    # real word error detected
                    candidates = self.formulate_candidate(token, bigram, bigram_next, trigram)

                    # print("\n")
                    # print("Token: ", token)
                    # print("Bigram:", str(bigram))
                    # print("Bigram Right: ", str(bigram_next))
                    # print("Trigram: ", str(trigram))

                    # # print all scores for debugging
                    # print("Bigram Score: ", str(bigram_prob))
                    # print("Bigram Right Score: ", str(bigram_next_prob))
                    # print("Trigram Score: ", str(trigram_prob))
                    # print("Weighted Score: ", str(weighted_prob))
                    # print("\n")

                    error = {
                        "id": "REAL_WORD_" + str(id),
                        "error_token": token,
                        "position": (start_pos, end_pos),
                        "candidates": candidates
                    }

                    id += 1
                    real_word_errors.append(error)

        return non_word_errors, real_word_errors