from scraper import init_scraper, get_tweets
from preprocessing import preprocessing, create_model
from kmeans import kmeans
from sentiment_analysis import sentiment_analysis

def scrape() -> None:
    scraper = init_scraper()
    for year in range(2011,2023):
        for month in range(1,13):
            print(month, year)
            try:
                get_tweets(scraper, terms=['climate change'], since=f'{year}-{str(month).zfill(2)}-01', until=f'{year}-{str(month+1).zfill(2)}-01')
            except:
                continue

def main() -> None:
    # Prefix for data files
    prefix = 'all'

    # Preprocess the data, create a model, perform clustering, and perform sentiment analysis
    # initial_df = preprocessing(prefix)
    # create_model(initial_df, prefix)
    # kmeans(prefix)
    result_df = sentiment_analysis(prefix)
    result_df.to_csv(f'./etc/sentiment_output_{prefix}.csv', index=False)


if __name__ == "__main__":
    main()