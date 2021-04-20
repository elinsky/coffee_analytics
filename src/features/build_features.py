# Script to turn interim data into features for modeling

import numpy as np
import pandas as pd
import os
import json

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


