#!/usr/bin/env python
# coding: utf-8

import numpy as np
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
from gensim import corpora, models

lemmatizer = WordNetLemmatizer()

def doc_tokenizer(doc):
    doc = doc.replace('\\n','').lower()
    sentences = sent_tokenize(doc)
    doc_tokens = [word_tokenize(sentence) for sentence in sentences]
    return doc_tokens

def get_wordnet_pos(treebank_tag):
    """Converts a treebank POS tag to a wordnet POS tag."""
    if treebank_tag.startswith('J'):
        tag = wordnet.ADJ
    elif treebank_tag.startswith('V'):
        tag = wordnet.VERB
    elif treebank_tag.startswith('N'):
        tag = wordnet.NOUN
    elif treebank_tag.startswith('R'):
        tag = wordnet.ADV
    else:
        tag = ''
    return tag

def sentence_pos_tagger(sentence):
    """Takes a sentence as a list of tokens and returns a list of wordnet POS tagged tokens"""
    treebank_tags = pos_tag(sentence)
    wordnet_tags = [
        (treebank_tag[0], get_wordnet_pos(treebank_tag[1])) for treebank_tag in treebank_tags
    ]
    return wordnet_tags

def doc_pos_tagger(doc_tokens):
    pos_tags = [
        sentence_pos_tagger(sentence) for sentence in doc_tokens
    ]
    return pos_tags

def tag_lemmatizer(pos_tag):
    """Lemmatized a POS tagged word."""
    if pos_tag[1] != '':
        lemmatized_word = lemmatizer.lemmatize(pos_tag[0], pos_tag[1])
    else:
        lemmatized_word = pos_tag[0]
    return lemmatized_word

def sentence_lemmatizer(sentence_tags):
    """Lemmatize POS tagged words from a tagged sentence."""
    lemmatized_sentence = [
        tag_lemmatizer(pos_tag) for pos_tag in sentence_tags
    ]
    return lemmatized_sentence

def doc_lemmatizer(doc_tags):
    """Lemmetize tagged words from a job doc and flatten sentence nesting."""
    lemmatized_doc = []
    for sentence_tags in doc_tags:
        lemmatized_sentence = sentence_lemmatizer(sentence_tags) 
        lemmatized_doc.extend(lemmatized_sentence)
    return lemmatized_doc    

def clean_doc(lemmatized_doc):
    my_stopwords = stopwords.words('english')
    cleaned_doc = [
        word for word in lemmatized_doc
        if word.isalpha() and word not in my_stopwords
        and len(word)>1
    ]
    return cleaned_doc

def combine_grams(cleaned_doc):
    bigram_model = Phrases(cleaned_doc)
    trigram_model = Phrases(bigram_model[cleaned_doc], min_count=1)
    processed_doc = list(trigram_model[bigram_model[cleaned_doc]])
    return processed_doc

def doc_processor(doc):
    doc_tokens = doc_tokenizer(doc)
    doc_tags = doc_pos_tagger(doc_tokens)
    lemmatized_doc = doc_lemmatizer(doc_tags)
    cleaned_doc = clean_doc(lemmatized_doc)
    processed_doc = combine_grams(cleaned_doc)
    return processed_doc

def data_processor(docs):
    processed_data = [
        doc_processor(doc) for doc in docs
    ]
