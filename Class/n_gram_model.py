"""
NAME: CHEAH WENG HOE
TP NUMBER: TP055533
Date Created: 24/12/2024
Date Modified: 30/12/2024

Module to Build n-gram Model
"""

import collections
import math
import nltk

from Class.corpus_builder import CorpusBuilder
from Class.tokens_cleaning import TokenCleaner

class NGramModel:

    def __init__(self):
        self.corpus_builder = CorpusBuilder()
        self.token_cleaner = TokenCleaner()
        
    # Build Unigram Model
    def build_unigram_model(self, cleaned_tokens, smoothing = 1):

        # Unigram Counter
        unigram_counter = collections.Counter(cleaned_tokens)

        # Total Number of Tokens
        total_tokens = len(cleaned_tokens)

        # Vocabulary Size
        vocab_size = len(unigram_counter)

        # Building Unigram Model
        unigram_model = {}

        for token, count in unigram_counter.items():
            smoothed_count = count + smoothing
            smoothed_total = total_tokens + (smoothing * vocab_size)
            prob = smoothed_count / smoothed_total
            log_prob = math.log(prob)
            unigram_model[token] = (prob, log_prob)

        # Unknown Token Probability
        unknown_prob = smoothing / (total_tokens + (smoothing * vocab_size))
        unknown_log_prob = math.log(unknown_prob)

        def unigram_model_func(token):
            return unigram_model.get(token, (unknown_prob, unknown_log_prob))

        return unigram_model_func, unigram_counter

    # Build Counter for N-Grams
    def build_counter(self, cleaned_body_text, n):

        sentences = nltk.sent_tokenize(cleaned_body_text)
        counter = collections.Counter()

        for sentence in sentences:

            tokens = nltk.word_tokenize(sentence)
            cleaned_tokens = self.token_cleaner.clean_tokens_n_gram(tokens)

            padded_tokens = list(
                nltk.pad_sequence(
                    cleaned_tokens, n, pad_left = True, pad_right = True,
                    left_pad_symbol = "<s>", right_pad_symbol = "</s>"
                )
            )
            ngrams_tuples = list(nltk.ngrams(padded_tokens, n))
            counter.update(ngrams_tuples)

        return counter

    # Build Bigram Model
    def build_bigram_model(self, cleaned_body_text, unigram_counter, unigram_model, back_off_factor = 0.4):

        bigram_counter = self.build_counter(cleaned_body_text, 2)

        def bigram_model(bigram):
            prev = bigram[0]
            bigram_count = bigram_counter[bigram]
            unigram_count = unigram_counter[prev]

            if unigram_count > 0:
                prob = bigram_count / unigram_count
            else:
                prob = 0

            if prob == 0:
                unigram_prob = unigram_model(bigram[1])[0]
                prob = back_off_factor * unigram_prob

            return prob, math.log(prob)

        return bigram_model, bigram_counter


    # Build Right Bigram Model
    def build_bigram_model_right(self, cleaned_body_text, unigram_counter, unigram_model, back_off_factor = 0.4):

        bigram_counter = self.build_counter(cleaned_body_text, 2)

        def right_bigram_model(bigram):
            next_word = bigram[1]
            bigram_count = bigram_counter[bigram]
            unigram_count = unigram_counter[next_word]

            if unigram_count > 0:
                prob = bigram_count / unigram_count
            else:
                prob = 0

            if prob == 0:
                unigram_prob = unigram_model(bigram[1])[0]
                prob = back_off_factor * unigram_prob

            return prob, math.log(prob)

        return right_bigram_model, bigram_counter

    # Build Trigram Model
    def build_trigram_model(self, cleaned_body_text, bigram_counter, bigram_model, back_off_factor = 0.4):

        trigram_counter = self.build_counter(cleaned_body_text, 3)

        def trigram_model(trigram):
            bigram_prev = (trigram[0], trigram[1])
            bigram_curr = (trigram[1], trigram[2])

            trigram_count = trigram_counter[trigram]
            bigram_count = bigram_counter[bigram_prev]

            if bigram_count > 0:
                prob = trigram_count / bigram_count
            else:
                prob = 0

            if prob == 0:
                bigram_prob = bigram_model(bigram_curr)[0]
                prob = back_off_factor * bigram_prob

            return prob, math.log(prob)

        return trigram_model, trigram_counter

    
    # Build N-Gram Models
    def n_gram_model(self):

        # Get the corpus
        cleaned_body_text = self.corpus_builder.merge_cleaned_corpora()

        # Get Clean Tokens
        tokens = nltk.word_tokenize(cleaned_body_text)
        cleaned_tokens = self.token_cleaner.clean_tokens_n_gram(tokens)

        # Building the model
        # Get the unigram model
        unigram_model, unigram_counter = self.build_unigram_model(cleaned_tokens)
        # Get the bigram model
        bigram_model, bigram_counter = self.build_bigram_model(cleaned_body_text, unigram_counter, unigram_model)
        # Get the right bigram model
        right_bigram_model, _ = self.build_bigram_model_right(cleaned_body_text, unigram_counter, unigram_model)
        # Get the trigram model
        trigram_model, _ = self.build_trigram_model(cleaned_body_text, bigram_counter, bigram_model)

        return unigram_model, bigram_model, right_bigram_model, trigram_model