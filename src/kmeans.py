import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from sklearn.cluster import KMeans


def kmeans(prefix) -> None:

    '''
    Perform K-Means clustering on word vectors to create a sentiment dictionary.

    - Load a pre-trained Word2Vec model
    - Cluster words based on their vectors and assign sentiment scores to clusters
    - Calculates a sentiment coefficient for each word
    - Save the sentiment dictionary to a CSV file

    Returns:
        None
    '''

    # Load the pre-trained Word2Vec model
    word2vec_model = Word2Vec.load(f'./etc/word2vec_{prefix}.model')
    word_vectors = word2vec_model.wv
    
    # Step 1: Perform K-Means clustering on word vectors
    model = KMeans(n_clusters=5, max_iter=2000, random_state=True, n_init=50).fit(X=word_vectors.vectors)

    # Step 2: Create a DataFrame to store word vectors and cluster assignments
    words = pd.DataFrame(word_vectors.index_to_key, columns=['word'])
    words = words.rename(columns = {0:'word'})
    words['vectors'] = words['word'].apply(lambda x: word_vectors[f'{x}'])
    words['cluster'] = words['vectors'].apply(lambda x: model.predict(x.reshape(-1, 300)))
    words['cluster'] = words['cluster'].apply(lambda x: x[0])

    # Step 3: Assign sentiment scores based on cluster assignments
    for i in words['cluster']:
        if i == 0: # neutral
            words['cluster_value'] = 2
        elif i == 1: # positive
            words['cluster_value'] = 1
        elif i == 2: # very negative
            words['cluster_value'] = 4
        elif i == 3: # negative
            words['cluster_value'] = 3
        else: # very positive
            words['cluster_value'] = 5

    # Step 4: Calculate closeness score and sentiment coefficient
    words['closeness_score'] = words.apply(lambda x: 1/(model.transform([x.vectors]).min()), axis=1)
    words['sentiment_coeff'] = words['closeness_score'] * words['cluster_value']
    
    # Step 5: Save the sentiment dictionary to a CSV file
    words[['word', 'sentiment_coeff']].to_csv(f'./etc/sentiment_dictionary_{prefix}.csv', index=False)
