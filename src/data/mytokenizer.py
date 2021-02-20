"""This module provides a custom tokenizer for use with CountVectorizer from
sklearn.feature_extraction.text. It implements lemmatization as part of the
tokenization process.
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

POS_Tag = Tuple[str, str]


class LemmaTokenizer:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def __call__(self, doc):
        return self.doc_lemmatizer(doc)

    def doc_lemmatizer(self, doc: str) -> List[str]:
        """doc_lemmatizer. Lemmatize tagged words from a job doc and flatten
        sentence nesting.

        Parameters
        ----------
        doc : str
            doc is a document encoded as a string.

        Returns
        -------
        List[str]

        """
        doc_tags = doc_tagger(doc)
        lemmatized_doc = [
            lemma for lemma in sentence_lemmatizer(sentence_tags)
            for sentence_tags in doc_tags
        ]
        return lemmatized_doc

    def doc_tagger(doc: str) -> List[List[POS_Tag]]:
        """doc_tagger. Takes a document and returns POS tagged tokens.

        Parameters
        ----------
        doc : str
            doc is a document encoded as a string.

        Returns
        -------
        List[List[POS_Tag]]

        """
        pos_tags = [
            sentence_tagger(sentence) for sentence in doc_tokenizer(doc)
        ]
        return pos_tags

    def sentence_lemmatizer(sentence_tags: List[POS_Tag]) -> List[str]:
        """sentence_lemmatizer. Takes a POS tagged sentence and lemmatizes.

        Parameters
        ----------
        sentence_tags : List[POS_Tag]
            sentence_tags list of POS tagged tokens that form a sentence.

        Returns
        -------
        List[str]

        """
        lemmatized_sentence = [
            lemmatize(pos_tag) for pos_tag in sentence_tags
        ]
        return lemmatized_sentence

    def lemmatize(pos_tag: POS_Tag) -> str:
        """lemmatize. Takes a POS tagged word and returns its Lemma.

        Parameters
        ----------
        pos_tag : POS_Tag
            pos_tag first position is a word token, second position is a
            wordnet POS tag.

        Returns
        -------
        str
        """
        if pos_tag[1] != '':
            lemmatized_word = self.lemmatizer.lemmatize(pos_tag[0], pos_tag[1])
        else:
            lemmatized_word = pos_tag[0]
        return lemmatized_word

    def doc_tokenizer(self, doc: str) -> List[List[str]]:
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
        sentences = sent_tokenize(doc)
        doc_tokens = [word_tokenize(sentence) for sentence in sentences]
        return doc_tokens

    def sentence_tagger(sentence: List[str]) -> List[POS_Tag]:
        """sentence_tagger. Takes a sentence as a list of tokens and
        returns a list of wordnet POS tagged tokens.

        Parameters
        ----------
        sentence : List[str]
            sentence is a list of word tokens from a sentence.

        Returns
        -------
        List[POS_Tag]

        """
        treebank_tags = pos_tag(sentence)
        wordnet_tags = [
            (treebank_tag[0], get_wordnet_pos(treebank_tag[1]))
            for treebank_tag in treebank_tags
        ]
        return wordnet_tags
