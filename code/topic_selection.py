"""
This module collects measures for trained LDA models to facilitate model
selection.
"""

__author__ = "Seth Chart"
__version__ = "0.1.0"
__license__ = "MIT"

import pandas as pd
import numpy as np
np.random.seed(42)
import pickle
from tqdm import tqdm
from gensim.models import LdaModel, CoherenceModel
from itertools import combinations

def get_model(num_topics):
    """get_model. Retrieves a saved trained LDA model from the `model` folder
    with the specified number of topics.

    Parameters
    ----------
    num_topics : int
        number of topics for the selected LDA model.
    """
    file_path = f'../model/LDA-{num_topics}topics'
    try:
        lda_model = LdaModel.load(file_path)
    except:
        print(
            f'Model not found. Train a model with {num_topics} and try again.'
        )
        pass
    return lda_model

def get_topics(lda_model):
    """get_topics. Extract list of topics with top twenty words.

    Parameters
    ----------
    lda_model : gensim.models.ldamulticore.LdaMulticore
        Trained LDA model. Takes output from get_model.
    """
    topics = lda_model.show_topics(num_topics = -1, num_words=20, formatted=False)
    return topics

def jaccard_similarity(set1, set2):
    """jaccard_similarity. Computes the Jaccard similarity between two sets.
    This function is symmetric in its inputs. Jaccard similarity is the
    proportion of the union of two sets that is contained in their
    intersection. Values range from zero to one. A value of one indicates that
    sets are equal and a value of zero indicates that sets are disjoint.

    Parameters
    ----------
    set1 : set
        Any set.
    set2 : set
        Any set.
    """
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = len(intersection)/len(union)
    return similarity

def topic_word_set(topic):
    """topic_word_set. Takes a topic from an LDA model and returns a set of top
    words for the topic.

    Parameters
    ----------
    topic : (int, [ (str, float)])
        A topic from a LDA model. Input should be one element of the list
        returned by get_topics.
    """
    word_tuple_list = topic[1]
    word_set = {word_tuple[0] for word_tuple in word_tuple_list}
    return word_set

def mean_jaccard_similarity(topics):
    """mean_jaccard_similarity. Computes the mean Jaccard similarity between
    pairs of topics from a LDA model. Lower mean Jaccard similarity generally
    indicates a better model.

    Parameters
    ----------
    topics : [(int, [(str, float)])]
        Takes output from get_topics.
    """
    N = len(topics)
    similarity_list = []
    combs = combinations(topics, 2)
    for topic1, topic2 in combs:
        set1 = topic_word_set(topic1)
        set2 = topic_word_set(topic2)
        similarity_list.append(jaccard_similarity(set1, set2))
    mean_similarity = np.mean(similarity_list)
    return mean_similarity

def get_coherence(model, texts, dictionary):
    """get_coherence. Get a coherence score for the provided model. Generally,
    a higher value of coherence indicates a better model.

    Parameters
    ----------
    model :
        A trained LDA model. Takes input from get_model.
    texts :
        texts
    dictionary :
        dictionary
    """
    coherence_model = CoherenceModel(
        model=model, 
        texts=texts, 
        dictionary=dictionary, 
        coherence='c_v')
    coherence = coherence_model.get_coherence()
    return coherence

def get_measures(texts, dictionary):
    """get_measures. Collects Jaccard similarity and coherence for all trained
    LDA models.

    Parameters
    ----------
    model:
        A trained LDA model. Takes input from get_model.
    texts :
        texts
    dictionary :
        dictionary
    """
    measures_list = {
        'n': [],
        'mean_jaccard': [],
        'coherence': []        
    }
    for n in tqdm(range(2,31)):
        model = get_model(n)
        topics = get_topics(model)
        measures_list['n'].append(n)
        measures_list['mean_jaccard'].append(mean_jaccard_similarity(topics)),
        measures_list['coherence'].append(get_coherence(model, texts, dictionary))
    return measures_list
