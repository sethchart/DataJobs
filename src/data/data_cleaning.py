"""
This module provides the full data cleaning pipeline.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

from nltk import pos_tag
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem.wordnet import WordNetLemmatizer
from gensim.models import Phrases
from typing import List, Tuple

lemmatizer = WordNetLemmatizer()


def doc_tokenizer(doc: str) -> List[List[str]]:
    """doc_tokenizer. Reads in a raw text document and returns a list of
    sentences each represented as a list of words. Text is converted to
    lower_case and newline characters are removed.

    Parameters
    ----------
    doc : str
        doc is a document encoded as a string.
    Returns
    -------
    List[List[str]]

    """
    doc = doc.replace('\\n', '').lower()
    sentences = sent_tokenize(doc)
    doc_tokens = [word_tokenize(sentence) for sentence in sentences]
    return doc_tokens


def get_wordnet_pos(treebank_tag: Tuple[str, str]) -> str:
    """get_wordnet_pos. Converts a treebank POS tag to a wordnet POS tag.

    Parameters
    ----------
    treebank_tag : Tuple[str, str]
        treebank_tag first position is the token, second position is the
        treebank POS tag.

    Returns
    -------
    str
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


def sentence_pos_tagger(sentence: List[str]) -> List[Tuple[str, str]]:
    """sentence_pos_tagger. Takes a sentence as a list of tokens and returns a
    list of wordnet POS tagged tokens.

    Parameters
    ----------
    sentence : List[str]
        sentence is a list of word tokens from a sentence.

    Returns
    -------
    List[Tuple[str, str]]

    """
    treebank_tags = pos_tag(sentence)
    wordnet_tags = [
        (treebank_tag[0], get_wordnet_pos(treebank_tag[1]))
        for treebank_tag in treebank_tags
    ]
    return wordnet_tags


def doc_pos_tagger(doc_tokens: List[List[str]]) -> List[List[Tuple[str, str]]]:
    """doc_pos_tagger. Takes a tokenized document and returns POS tagged
    tokens.

    Parameters
    ----------
    doc_tokens : List[List[str]]
        doc_tokens the output of doc_tokenizer.

    Returns
    -------
    List[List[Tuple[str, str]]]

    """
    pos_tags = [
        sentence_pos_tagger(sentence) for sentence in doc_tokens
    ]
    return pos_tags


def tag_lemmatizer(pos_tag: Tuple[str, str]) -> str:
    """tag_lemmatizer. Takes a POS tagged word and returns its Lemma.

    Parameters
    ----------
    pos_tag : Tuple[str, str]
        pos_tag first position is a word token, second position is a wordnet POS tag.

    Returns
    -------
    str
    """
    if pos_tag[1] != '':
        lemmatized_word = lemmatizer.lemmatize(pos_tag[0], pos_tag[1])
    else:
        lemmatized_word = pos_tag[0]
    return lemmatized_word


def sentence_lemmatizer(sentence_tags: List[Tuple[str, str]]) -> List[str]:
    """sentence_lemmatizer. Takes a POS tagged sentence and lemmatizes.

    Parameters
    ----------
    sentence_tags : List[Tuple[str, str]]
        sentence_tags list of POS tagged tokens that form a sentence.

    Returns
    -------
    List[str]

    """
    lemmatized_sentence = [
        tag_lemmatizer(pos_tag) for pos_tag in sentence_tags
    ]
    return lemmatized_sentence


def doc_lemmatizer(doc_tags: List[List[Tuple[str, str]]]) -> List[str]:
    """doc_lemmatizer. Lemmatize tagged words from a job doc and flatten
    sentence nesting.

    Parameters
    ----------
    doc_tags : List[List[Tuple[str, str]]]
        doc_tags output from doc_pos_tagger.

    Returns
    -------
    List[str]

    """
    lemmatized_doc = []
    for sentence_tags in doc_tags:
        lemmatized_sentence = sentence_lemmatizer(sentence_tags)
        lemmatized_doc.extend(lemmatized_sentence)
    return lemmatized_doc


def doc_clean(lemmatized_doc: List[str]) -> List[str]:
    """doc_clean. Takes a lemmatized document, drops special characters and
    stopwords.

    Parameters
    ----------
    lemmatized_doc : List[str]
        lemmatized_doc output from doc_lemmatizer.

    Returns
    -------
    List[str]

    """
    my_stopwords = stopwords.words('english')
    processed_doc = [
        word for word in lemmatized_doc
        if word.isalpha() and word not in my_stopwords and len(word)>1
    ]
    return processed_doc


def doc_processor(doc: str) -> List[str]:
    """doc_processor. Executes full data processing pipeline on a document with
    the exception of bigram and trigram grouping.

    Parameters
    ----------
    doc : str
        doc is a  string containing the full text of your document.

    Returns
    -------
    List[str]

    """
    doc_tokens = doc_tokenizer(doc)
    doc_tags = doc_pos_tagger(doc_tokens)
    lemmatized_doc = doc_lemmatizer(doc_tags)
    processed_doc = doc_clean(lemmatized_doc)
    return processed_doc


def data_processor(docs: List[str]) -> List[List[str]]:
    """data_processor. Takes a list of raw documents and executes full data
    processing pipeline for every document in the list.

    Parameters
    ----------
    docs : List[str]
        docs is a list of strings containing the full text of your documents.

    Returns
    -------
    List[List[str]]

    """
    processed_data = [
        doc_processor(doc) for doc in docs
    ]
    return processed_data


def data_combine_phrases(
    processed_data: List[List[str]], prefix: str
) -> List[List[str]]:
    """data_combine_phrases. Takes a corpus of cleaned documents and combines
    common phrases into bigrams, trigrams, and quadgrams.

    Parameters
    ----------
    processed_data : List[List[str]]
        processed_data output from data processor.
    prefix : str
        prefix to identify saved model.

    Returns
    -------
    List[List[str]]
    """
    phrase_model_1 = Phrases(processed_data)
    phrase_model_1.save(f'../model/{prefix}-phrase_model_1.pkl')
    phrase_model_2 = Phrases(phrase_model_1[processed_data], min_count=1)
    phrase_model_2.save(f'../model/{prefix}-phrase_model_2.pkl')
    data_phrases = list(phrase_model_2[phrase_model_1[processed_data]])
    return data_phrases


def doc_combine_phrases(processed_doc: List[str], prefix: str) -> List[str]:
    """doc_combine_phrases. Takes a processed document and combines common
    phrases into bigrams, trigrams, and quadgrams. data_combine_phrases must
    run before doc_combine_phrases.

    Parameters
    ----------
    processed_doc : List[str]
        processed_doc output from doc_processor,
    prefix : str
        prefix to identify saved model.

    Returns
    -------
    List[str]
    """
    try:
        phrase_model_1 = Phrases.load(f'../model/{prefix}-phrase_model_1.pkl')
        phrase_model_2 = Phrases.load(f'../model/{prefix}-phrase_model_2.pkl')
    except:
        print('Call `data_combine_phrases` on processed data to build a phrase model')
        pass
    doc_phrases = list(phrase_model_2[phrase_model_1[processed_doc]])
    return doc_phrases
