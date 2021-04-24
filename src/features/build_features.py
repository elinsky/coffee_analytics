# Script to turn interim data into features for modeling

import numpy as np
import pandas as pd
import os
import json
from keras.preprocessing.text import Tokenizer

def __insert_nans(df, field: str) -> None:
    """Given a pandas dataframe and a field, replace all 'NA' and 'NR' with np.nan.
    Make replacement inplace, and return None."""
    df[field].replace(to_replace=['NA', 'NR'], value=np.nan, inplace=True)


def __convert_to_float(df, field: str) -> None:
    """Given a pandas dataframe and a field name, convert the field to a float64, inplace."""
    df[field] = df[field].astype('float64')


def __remove_tabs(df, field: str) -> None:
    """Given a pandas dataframe and a field name, remove all tab characters inplace and return None."""
    df[field].replace(to_replace=r'\t', value='', regex=True, inplace=True)

def __get_dataset_path() -> str:
    """Returns the path to the ratings.jl interim datset."""
    src_features_path = os.path.join(os.path.dirname(__file__))
    src_path = os.path.dirname(src_features_path)
    coffee_analytics_path = os.path.dirname(src_path)
    dataset_path = coffee_analytics_path + '/data/interim/ratings.jl'
    return dataset_path



def __get_interim_dataset():
    """Return a dataframe of the data/interim/ratings.jl file"""
    line_list = []
    with open(__get_dataset_path()) as f:
        for line in f:
            a_dict = json.loads(line)
            df = pd.DataFrame(a_dict, index=[0])
            line_list.append(df)

    df = pd.concat(line_list)
    df = df.reset_index(drop=True)
    return df

def get_clean_dataset():
    """Loads the data/interim/ratings.jl dataset, cleans it, and returns it as a pandas dataframe."""
    df = __get_interim_dataset()
    df['with_milk'].replace(to_replace=r'Flavor in milk: ', value='', regex=True, inplace=True)
    for field in ['rating', 'aroma', 'acidity_structure', 'flavor', 'aftertaste', 'body', 'with_milk']:
        __remove_tabs(df, field)
        __insert_nans(df, field)
        __convert_to_float(df, field)

    # Convert roast type to a categorical variable
    __insert_nans(df, 'roast_level')
    df['roast_level'] = df['roast_level'].astype('category')

    # Set order for categories
    df['roast_level'] = df['roast_level'].cat.reorder_categories(
        ['Light', 'Medium-Light', 'Medium', 'Medium-Dark', 'Dark', 'Very Dark'], ordered=True)

    return df

def get_roast_classification_dataset():
    """Returns a dataset where blind assessment is used to classify roast levels.  Returns a tuple, where the first
    item is a pandas series that contains the blind assessments.  The second item in the tuple is a pandas series that
    contains the roast level classifications."""
    df = get_clean_dataset()
    # drop unused columns
    df = df.drop(
        ['roaster', 'bean', 'rating', 'roaster_location', 'coffee_origin', 'agtron', 'estimated_price', 'review_date',
         'aroma', 'acidity_structure', 'body', 'flavor', 'aftertaste', 'with_milk', 'notes', 'bottom_line',
         'who_should_drink_it'], axis=1)
    # drop rows with NaN roast level or NaN blind_assessment
    df = df.dropna()
    # after dropping rows, reset the index
    df = df.reset_index(drop=True)
    X = df['blind_assessment']
    y = df['roast_level']
    # convert y from categorical text to integers
    y = y.cat.codes
    return X, y

def get_vocab(docs, min_count=1):
    """Given a iterable of documents, return a list of unique vocab words where each word is present at least min_count
    times."""
    t = Tokenizer()
    t.fit_on_texts(docs)
    vocab = []
    for k in t.word_counts:
        if t.word_counts[k] >= min_count:
            vocab.append(k)
    return vocab


def tokenize_dataset(df):
    # TODO
    return
