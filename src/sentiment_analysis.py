import math
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def create_dictionary(x, transformed_file, features) -> dict:

    '''
    Create a TF-IDF dictionary for a given row of text data.

    Returns:
        dict: A dictionary mapping words to their TF-IDF scores for the input row.
    '''

    # Convert the TF-IDF vector to a coordinate format
    vector = transformed_file[x.name].tocoo()
    
    # Map the feature indices to their corresponding words
    vector.col = features.iloc[vector.col].values
    
    # Return a dictionary from the coordinate format
    return dict(zip(vector.col, vector.data))

def replace_words(x, transformed_file, features) -> list:

    '''
    Replaces words in a text with their corresponding TF-IDF scores.

    Returns:
        list: A list of TF-IDF scores for words in the input text.
    '''

    # Create a TF-IDF dictionary for the current row
    dictionary = create_dictionary(x, transformed_file, features)   
    
    # Split the text and replace words with TF-IDF scores
    return list(map(lambda y: dictionary[f'{y}'], x['text'].split()))

def sentiment_rate(df) -> pd.DataFrame:

    '''
    Calculates sentiment rates for each row in the DataFrame.

    Returns:
        df (pandas.DataFrame): DataFrame with added 'sentiment_rate' and 'normalized_sentiment_rate' columns.
    '''

    # Calculate the sentiment rate by performing a dot product of sentiment coefficients and TF-IDF scores
    df['sentiment_rate'] = df.apply(lambda x: np.array(x.loc['sentiment_coeff']) @ np.array(x.loc['tfidf_scores']), axis=1)

    # Define the min and max values of your desired five-point scale
    min_scale_value = 1  # Minimum value on the scale
    max_scale_value = 5  # Maximum value on the scale

    # Min-Max scaling
    min_value = df['sentiment_rate'].min()
    max_value = df['sentiment_rate'].max()

    # Apply Min-Max scaling formula to normalize sentiment rates
    df['normalized_sentiment_rate'] = min_scale_value + ((df['sentiment_rate'] - min_value) / (max_value - min_value)) * (max_scale_value - min_scale_value)

    return df

def cluster_prediction(df) -> pd.DataFrame:
    
    '''
    Maps cluster predictions to sentiment categories based on normalized sentiment rates.

    Returns:
        df (pd.DataFrame): DataFrame with added 'pred' column containing sentiment category predictions.
    '''

    # Create a new column 'pred' to store predicted sentiment categories
    df = df.assign(pred=pd.Series([None] * len(df)))

    for index, row in df.iterrows():

        rate = math.floor(row['normalized_sentiment_rate'])
        rate_map = {
            1: 'Very Negative',
            2: 'Negative',
            3: 'Neutral',
            4: 'Positive',
            5: 'Very Positive'
        }

        # Assign the predicted sentiment category based on the normalized sentiment rate
        df.at[index, 'pred'] = rate_map[rate]

    return df

def sentiment_analysis(prefix) -> pd.DataFrame:

    '''
    Performs sentiment analysis on text data using TF-IDF and sentiment coefficients.

    Returns:
        pd (pd.DataFrame): DataFrame with sentiment analysis results.
    '''

    # Read cleaned text data and sentiment map
    text = pd.read_csv(f'./etc/cleaned_{prefix}.csv')
    sentiment_map = pd.read_csv(f'./etc/sentiment_dictionary_{prefix}.csv')

    # Create a dictionary for sentiment coefficients
    sentiment_dict = dict(zip(sentiment_map['word'].values, sentiment_map['sentiment_coeff'].values))

    # Create a TF-IDF vectorizer
    tfidf = TfidfVectorizer(tokenizer=lambda y: y.split(), norm=None)
    tfidf.fit(text['text'])
    features = pd.Series(tfidf.get_feature_names_out())
    text_tfidf = tfidf.transform(text['text'])

    # Replace words in text with their TF-IDF scores
    replaced_tfidf_scores = text.apply(lambda x: replace_words(x, text_tfidf, features), axis=1)
    replaced_closeness_scores = text['text'].apply(lambda x: list(map(lambda y: sentiment_dict.get(y, 0), x.split())))

    # Create a DataFrame to store sentiment data
    df = pd.DataFrame(data=[replaced_closeness_scores, replaced_tfidf_scores, text['text']]).T
    df.columns = ['sentiment_coeff', 'tfidf_scores', 'text']

    # Calculate sentiment rate and normalize it
    df = sentiment_rate(df)
    
    # Map sentiment rates to sentiment categories
    df = cluster_prediction(df)
    return df
