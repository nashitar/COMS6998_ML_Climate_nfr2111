import csv
from ntscraper import Nitter


def init_scraper() -> Nitter:

    '''
    Initialize the Nitter scraper.

    - Create Nitter scraper object.
    - Configure logging levels and instance check settings.

    Source: https://app.soos.io/research/packages/Python/-/ntscraper
    Source: https://github.com/bocchilorenzo/ntscraper/

    Returns:
        Nitter: Initialized Nitter scraper object.
    '''

    # The valid logging levels are:
    # - None = no logs
    # - 0 = only warning and error logs
    # - 1 = previous + informational logs (default)

    # The skip_instance_check parameter is used to skip the check of the Nitter instances 
    # altogether during the execution of the script. If you use your own instance or trust 
    # the instance you are relying on, then you can skip set it to 'True', otherwise it's 
    # better to leave it to false.
    
    return Nitter(log_level=0, skip_instance_check=False)

def get_tweets(scraper, terms, since, until) -> None:

    '''
    Get tweets matching specified terms within a date range.

    Args:
        scraper (Nitter): Initialized Nitter scraper object.
        terms (str): Search terms.
        since (str): Start date in 'YYYY-MM-DD' format.
        until (str): End date in 'YYYY-MM-DD' format.

    Returns:
        None
    '''

    # Get tweets
    results = scraper.get_tweets(terms, number=10000, mode='term',
                                 since=since, until=until,
                                 language='en')

    # Get keys - Information from each of the tweets
    # link,text,user,date,is-retweet,external-link,quoted-post,stats,pictures,videos,gifs
    keys = results['tweets'][0].keys()

    # Write tweets to csv
    with open(f'./etc/{since[:-3]}.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(results['tweets'])
