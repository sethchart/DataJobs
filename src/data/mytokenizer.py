"""This module provides a custom tokenizer for use with CountVectorizer from
sklearn.feature_extraction.text. It implements lemmatization as part of the
tokenization process.
"""
__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

import string
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
        doc_tags = self.doc_tagger(doc)
        lemmatized_doc = [
            lemma.translate(str.maketrans('', '', string.punctuation)) for
            sentence_tags in doc_tags for
            lemma in self.sentence_lemmatizer(sentence_tags) if
            lemma.translate(str.maketrans('', '', string.punctuation)) != ''
        ]
        return lemmatized_doc

    def doc_tagger(self, doc: str) -> List[List[POS_Tag]]:
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
            self.sentence_tagger(sentence) for
            sentence in self.doc_tokenizer(doc)
        ]
        return pos_tags

    def sentence_tagger(self, sentence: List[str]) -> List[POS_Tag]:
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
            (treebank_tag[0], self.get_wordnet_pos(treebank_tag[1]))
            for treebank_tag in treebank_tags
        ]
        return wordnet_tags

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
        sentences = sent_tokenize(
            doc.lower().replace('\\n', '')
        )
        doc_tokens = [word_tokenize(sentence) for sentence in sentences]
        return doc_tokens

    def sentence_lemmatizer(self, sentence_tags: List[POS_Tag]) -> List[str]:
        """sentence_lemmatizer.

        Parameters
        ----------
        sentence_tags : List[POS_Tag]
            sentence_tags

        Returns
        -------
        List[str]

        """
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
            self.lemmatize(pos_tag) for pos_tag in sentence_tags
        ]
        return lemmatized_sentence

    @staticmethod
    def get_wordnet_pos(treebank_tag: POS_Tag) -> str:
        """get_wordnet_pos. Converts a treebank POS tag to a wordnet POS tag.

        Parameters
        ----------
        treebank_tag : POS_Tag
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

    def lemmatize(self, pos_tag: POS_Tag) -> str:
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
