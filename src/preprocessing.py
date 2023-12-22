import multiprocessing
import nltk
import os
import pandas as pd
import re
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser


def clean_text(text) -> [str]:

    '''
    Clean text data.

    - Remove URLs, mentions, hashtags, punctuations, extraneous spaces and stopwords
    - Converts original text string to lowercase word list

    Returns:
        text (list of str): A list of cleaned words.
    '''

    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE) # Remove URLs
    text = re.sub(r'\@\w+|\#','', text) # Remove mentions and hashtags
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuations
    text = re.sub(r'\s+', ' ', text) # Remove multiple spaces
    text = text.lower() # Convert to lowercase
    stopwords = nltk.corpus.stopwords.words('english') # Remove common stopwords
    text = [word for word in text.split() if word not in stopwords]
    return text

def preprocessing(prefix=None) -> pd.DataFrame:

    '''
    Preprocess CSV data.

    - Compile all CSV files containing the given prefix into a single dataframe
    - Drop unnecessary columns, remove null and duplicate columns
    - Clean text using clean_text function

    Returns:
        df (pandas.DataFrame): A DataFrame containing cleaned and preprocessed data.
    '''

    # Find CSV files in the current directory with a specific prefix
    if prefix is not None:
        filenames = [f'./etc/{file}' for file in os.listdir('./etc') if file.startswith(prefix) and file.endswith('.csv')]
    else: 
        filenames = [f'./etc/{file}' for file in os.listdir('./etc') if file.startswith('2') and file.endswith('.csv')]
    dataframes = []

    # Read each CSV file into a DataFrame and append to a list
    for filename in filenames:
        df = pd.read_csv(filename, index_col=None, header=0)
        dataframes.append(df)

    # Concatenate all DataFrames into one
    df = pd.concat(dataframes, axis=0, ignore_index=True)

    # Drop unnecessary columns
    df = df.drop(columns=['link', 'user', 'is-retweet', 'external-link', 'quoted-post', 
                          'stats', 'pictures', 'videos', 'gifs'])

    # Drop rows with missing values and duplicates, then reset the index
    df = df.dropna()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    # Filter rows containing the text 'climate change' (case-insensitive)
    # Scraper gets all tweets containing the words 'climate' and 'change' rather than 
    # the phrase 'climate change'. This is a fix
    df = df[df['text'].str.contains('climate change', case=False)]

    # Clean the text in the 'text' column
    df['text'] = df['text'].apply(lambda x: clean_text(x))

    return df

def create_model(df, prefix='all') -> None:

    '''
    Create Word2Vec model.

    - Create bigrams from the text
    - Export the cleaned DataFrame that uses the generated bigrams to a new CSV file
    - Define a Word2Vec model, build the vocabulary, train the model, and save it to a file

    Returns:
        None
    '''

    text = [row for row in df['text']]

    # Create phrases (bigrams) from the text
    phrases = Phrases(text, min_count=1)
    bigram = Phraser(phrases)
    sentences = bigram[text]

    # Create a copy of the DataFrame and join bigrams in the 'text' column
    export = df.copy()
    export['text'] = export['text'].apply(lambda x: ' '.join(bigram[x]))

    # Export the cleaned DataFrame to a new CSV file
    export[['text']].to_csv(f'./etc/cleaned_{prefix}.csv', index=False)

    # Parameters for Word2Vec model
    w2v_model = Word2Vec(min_count=2,      # Ignore words with low frequency
                        window=4,          # Context window size
                        vector_size=300,   # Dimensionality of word vectors
                        sample=1e-5,       # Threshold for word downsampling
                        alpha=0.03,        # Initial learning rate
                        min_alpha=0.0007,  # Minimum learning rate
                        negative=20,       # Number of negative samples for training
                        workers=multiprocessing.cpu_count()-1)  # Number of CPU cores for parallelization

    # Build the vocabulary
    w2v_model.build_vocab(sentences, progress_per=50000)

    # Train the Word2Vec model on the text data
    w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

    # Save the trained Word2Vec model to a file
    w2v_model.save(f'./etc/word2vec_{prefix}.model')