#!/usr/bin/env python3
"""
This module provides helper functions for visualization in notebooks and
reports.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

import inspect
from IPython.display import Markdown, display
from plotly import express as px
from pandas import DataFrame
from wordcloud import WordCloud
from matplotlib import pyplot as plt

def display_source(obj):
    """Summary of display_source. Get source code for the provided object and
    display in notebook as markdown.
    """
    source = inspect.getsource(obj)
    wrapped_source = f'```python\n{source}\n```'
    markdown_source = Markdown(wrapped_source)
    display(markdown_source)

def document_length_histogram(df: DataFrame, column_name: str):
    """document_length_histogram. Takes our raw data as a dataframe and returns
    a histogram of the lengths of stings in characters.
    """
    lengths = df[column_name].apply(len)
    median_length =lengths.median()
    fig = px.histogram(
        lengths,
        title = f'Distribution of Job {column_name.title()} Lengths (Medain {median_length})',
        width = 800,
        height = 600,
        labels = {
            'value': f'{column_name.title()} Length (characters)',
        },
        nbins = 45,
    )
    fig.layout.update(showlegend=False)
    fig.show()

def make_wordcloud(text):
    """Summary of make_wordcloud. Given a string produce a high definition 
    wordcloud of the contained words.
    """
    wordcloud = WordCloud(background_color='white', width=3200, height=2400)
    wordcloud.generate(text)
    fig = plt.figure(figsize = (16,12))
    plt.imshow(wordcloud)
    plt.axis("off")
    return fig
