from src.features.mytokenizer import LemmaTokenizer
from sklearn.feature_extraction.text import CountVectorizer

description_vectorizer = CountVectorizer(
            encoding='utf-8',
            decode_error='ignore',
            strip_accents='unicode',
            lowercase=True,
            preprocessor=None,
            tokenizer=LemmaTokenizer(),
            stop_words='english',
            ngram_range=(1,4),
            analyzer='word',
            max_df=0.95,
            min_df=0.05,
            max_features=None
)
title_vectorizer = CountVectorizer(
            encoding='utf-8',
            decode_error='ignore',
            strip_accents='unicode',
            lowercase=True,
            preprocessor=None,
            tokenizer=LemmaTokenizer(),
            stop_words='english',
            ngram_range=(1,4),
            analyzer='word',
            max_df=0.95,
            min_df=0.05,
            max_features=None
)

