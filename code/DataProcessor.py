"""
This module provides the full data cleaning pipeline.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

import numpy as np
from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
from gensim import corpora, models

lemmatizer = WordNetLemmatizer()

def doc_tokenizer(doc):
    """doc_tokenizer. Reads in a raw text document and returns a list of
    sentences each represented as a list of words. Text is converted to
    lower_case and newline characters are removed.

    Parameters
    ----------
    doc : str
       A raw string document. 
    """
    doc = doc.replace('\\n','').lower()
    sentences = sent_tokenize(doc)
    doc_tokens = [word_tokenize(sentence) for sentence in sentences]
    return doc_tokens

def get_wordnet_pos(treebank_tag):
    """get_wordnet_pos. Converts a treebank POS tag to a wordnet POS tag.

    Parameters
    ----------
    treebank_tag : (str, str)
        First position is the token, second position is the treebank POS tag.
    """
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
    """sentence_pos_tagger. Takes a sentence as a list of tokens and returns a
    list of wordnet POS tagged tokens.

    Parameters
    ----------
    sentence : list of strings
        list of word tokens that form a sentence.
    """
    treebank_tags = pos_tag(sentence)
    wordnet_tags = [
        (treebank_tag[0], get_wordnet_pos(treebank_tag[1])) for treebank_tag in treebank_tags
    ]
    return wordnet_tags

def doc_pos_tagger(doc_tokens):
    """doc_pos_tagger. Takes a tokenized document and returns POS tagged
    tokens.

    Parameters
    ----------
    doc_tokens : list of list of strings
        doc_tokens should be the output of doc_tokenizer.
    """
    pos_tags = [
        sentence_pos_tagger(sentence) for sentence in doc_tokens
    ]
    return pos_tags

def tag_lemmatizer(pos_tag):
    """tag_lemmatizer. Takes a POS tagged word and returns its Lemma.

    Parameters
    ----------
    pos_tag : (str, str)
        First position is a word token, second position is a wordnet POS tag.
    """
    if pos_tag[1] != '':
        lemmatized_word = lemmatizer.lemmatize(pos_tag[0], pos_tag[1])
    else:
        lemmatized_word = pos_tag[0]
    return lemmatized_word

def sentence_lemmatizer(sentence_tags):
    """sentence_lemmatizer. Takes a POS tagged sentence and lemmatizes.

    Parameters
    ----------
    sentence_tags : list of tuples (str, str)
        List of POS tagged tokens that form a sentence.
    """
    lemmatized_sentence = [
        tag_lemmatizer(pos_tag) for pos_tag in sentence_tags
    ]
    return lemmatized_sentence

def doc_lemmatizer(doc_tags):
    """doc_lemmatizer. Lemmatize tagged words from a job doc and flatten sentence nesting.

    Parameters
    ----------
    doc_tags : list of list of tuples (str, str)
        Takes output from doc_pos_tagger.
    """
    lemmatized_doc = []
    for sentence_tags in doc_tags:
        lemmatized_sentence = sentence_lemmatizer(sentence_tags) 
        lemmatized_doc.extend(lemmatized_sentence)
    return lemmatized_doc    

def doc_clean(lemmatized_doc):
    """doc_clean. Takes a lemmatized document, drops special characters and
    stopwords.

    Parameters
    ----------
    lemmatized_doc : list of strings
        Takes output from doc_lemmatizer.
    """
    my_stopwords = stopwords.words('english')
    processed_doc = [
        word for word in lemmatized_doc
        if word.isalpha() and word not in my_stopwords
        and len(word)>1
    ]
    return processed_doc

def doc_processor(doc):
    """doc_processor. Executes full data processing pipeline on a document with
    the exception of bigram and trigram grouping.

    Parameters
    ----------
    doc : str
        string containing the full text of your document.
    """
    doc_tokens = doc_tokenizer(doc)
    doc_tags = doc_pos_tagger(doc_tokens)
    lemmatized_doc = doc_lemmatizer(doc_tags)
    processed_doc = doc_clean(lemmatized_doc)
    return processed_doc

def data_processor(docs):
    """data_processor. Takes a list of raw documents and executes full data
    processing pipeline for every document in the list.

    Parameters
    ----------
    docs : list of str
        List of strings containing the full text of your documents.
    """
    processed_data = [
        doc_processor(doc) for doc in docs
    ]
    return processed_data

def data_combine_phrases(processed_data):
    """data_combine_phrases. Takes a corpus of cleaned documents and combines common phrases into
    bigrams, trigrams, and quadgrams.

    Parameters
    ----------
    processed_data : list of strings
        Takes output from data_processor.
    """
    bigram_model = Phrases(processed_data)
    phrase_model_1= bigram_model.freeze()
    phrase_model_1.save('../model/phrase_model_1.pkl')
    quadgram_model = Phrases(phrase_model_1[processed_data], min_count=1)
    phrase_model_2 = quadgram_model.freeze()
    phrase_model_2.save('../model/phrase_model_2.pkl')
    data_phrases = list(phrase_model_2[phrase_model_1[processed_data]])
    return data_phrases

def doc_combine_phrases(processed_doc):
    """doc_combine_phrases. Takes a processed document and combines common
    phrases into bigrams, trigrams, and quadgrams. data_combine_phrases must
    run before doc_combine_phrases.

    Parameters
    ----------
    processed_doc : list of strings
        Takes output from doc_processor.
    """
    try:
        phrase_model_1 = Phrases.load('../model/phrase_model_1.pkl')
        phrase_model_2 = Phrases.load('../model/phrase_model_2.pkl')
    except:
        print('Call `data_combine_phrases` on processed data to build a phrase model')
        pass
    doc_phrases = list(phrase_model_2[phrase_model_2[processed_doc]])
    return doc_phrases

