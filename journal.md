
## Trial 1: Using Twint

Twint is a Python package designed for scraping and collecting data from Twitter, offering an alternative to the official Twitter API. This versatile tool is commonly used for various applications such as research, social media analysis, and data mining. It stands out for its ability to bypass API restrictions, enabling users to access Twitter data without requiring API keys or worrying about rate limits. Twint supports advanced search queries, allowing users to filter tweets based on keywords, usernames, locations, languages, and date ranges. It can also retrieve user information, including followers, following, and profile details. Twint offers flexibility with output formats, such as CSV, JSON, and Pandas DataFrames, making data analysis and visualization more accessible. Thanks to its asynchronous scraping capabilities, it can efficiently handle large-scale data retrieval tasks. Furthermore, Twint respects Twitter's terms of service, only collecting publicly available data. As an open-source project with an active community, it provides a valuable resource for those in need of Twitter data for various purposes. 

I was hoping to use Twint originally to get all tweets that used certain hashtags referencing natural disasters in the months following said disasters (ex.: all tweets in the two months following hurricane Sandy that were tagged #HurricaneSandy) while avoiding the rate limits of the Twitter API. Over the course of a week working with TWINT, various challenges and issues were encountered across different computing environments, including Jupyter Notebook, a local machine, and Google Colab. These issues spanned both technical and configuration-related aspects. One of the technical hurdles faced was an import issue involving the aiohttp library, which TWINT relies on for its functionality. The community-driven platform GitHub proved to be a valuable resource, as a solution to this problem was found and implemented, helping to resolve the aiohttp import issue (https://github.com/twintproject/twint/issues/1297). In addition to technical obstacles, configuration problems also surfaced during the project. These configuration challenges encompassed defining the hashtags to track, specifying the desired time frame for data collection (e.g., the two months following a natural disaster), and setting various other relevant parameters. Despite resolving some of these technical challenges, the project encountered a significant roadblock in the form of an error that could not be resolved. The error message, "RefreshTokenException: Could not find the Guest token in HTML," indicated that there was an issue related to obtaining a Guest token, and this error persisted without a clear solution. Despite my analysis of the available online resources (https://github.com/twintproject/twint/issues/1114 https://github.com/twintproject/twint/issues/1061) and my reaching out to people who had solved this error I could not come to a successful conclusion to the issue, so I began looking into alternatives.

The following is my installation attempt and an example run. 

```
pip install aiohttp==3.7.0
!pip3 install --user --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
```

```
import os

from google.colab import drive
drive.mount('/content/drive')

path_to_twint_directory = "./src/twint"
token_file_path = os.path.join(path_to_twint_directory, "token.py")

# Write the modified content back to token.py
with open(token_file_path, 'w') as file:
    file.write(token_content) # token content being the corrected file contents
```

```
import twint
import pandas
import datetime

# Set the date range from the start of Hurricane Ian to two months later
start_date = datetime.datetime(year=2023, month=1, day=1)  # Update with the actual start date of Hurricane Ian
end_date = start_date + datetime.timedelta(days=60)  # Two months later

# Configure Twint to search for tweets with the hashtag #HurricaneIan within the date range
c = twint.Config()
c.User_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Chrome/99.0.9999.999 Safari/605.1.15"

c.User_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0'

c.Search = "#HurricaneIan"
c.Since = start_date.strftime('%Y-%m-%d')
c.Until = end_date.strftime('%Y-%m-%d')
c.Store_csv = True
c.Output = "hurricane_ian_tweets.csv"  # Output file name
c.Limit = 10

# Run the Twint search
twint.run.Search(c)
```

## Trial 2: Using Stweet

Documentation:
- https://www.reddit.com/r/Python/comments/vb8cmu/twint_python_twitter_crawler_no_longer_being/
- https://www.reddit.com/r/OSINT/comments/wx1qba/tools_for_twitter_like_twint_that_actually_are/

Stweet is an advanced Python library used for scraping tweets and user information from Twitter's unofficial API. It provides a modern, fast, and user-friendly approach to collect tweets using various search parameters. Stweet was developed to offer a simpler and more reliable alternative to other scraping tools like Twint, addressing issues like complexity and error frequency. It allows users to conduct detailed searches for tweets, export data in various formats, and is designed with an emphasis on simplicity and flexibility in its codebase. The motivation behind the creation of Stweet was the challenges faced with Twint, another tweet scraping tool, which had many errors and a complex codebase. The creator aimed to provide a simpler, more reliable alternative​​​​. Stweet stood out with its user-friendly design and simplicity, making it easier to understand and modify. This was a notable improvement from Twint, which I had previously found to be error-prone and complex. The ability to contribute to Stweet and its flexibility in data export options, such as JSON lines and CSV, made my data scraping tasks more efficient and adaptable to different project requirements.

However, my journey with Stweet was not without challenges. I encountered an issue with the `JsonLineFileRawOutput` attribute, which threw an `AttributeError`, which I realized was a compatibility issue with my Python version (https://github.com/markowanga/stweet/issues/96). Stweet version 2.0 required Python versions above 3.8, and once I upgraded my Python environment, this issue was resolved. Despite these resolved issues, I faced a significant obstacle that seemed beyond resolution. The `ScrapBatchBadResponse` error, with a status code of 404, indicated that Stweet was unable to fetch data from Twitter. This issue persisted and appeared to be linked to changes in Twitter's API or efforts to restrict scraping activities. This irresolvable problem posed a major limitation to Stweet's functionality, highlighting the inherent challenges in relying on unofficial APIs and the dynamic nature of web scraping tools (https://github.com/markowanga/stweet/issues/112). The one thing I thought to try to resolve this error was reverting back to an older version of Stweet that didn’t seem to experience it. Unfortunately, I ran into the same error message I received with Twint, "RefreshTokenException: Could not find the Guest token in HTML," which indicated that there was an issue related to obtaining a Guest token, and this error persisted without a clear solution. This time, I found no documentation to reference on the issue and resolved that recent changes to Twitters API (https://www.engadget.com/twitter-shut-off-its-free-api-and-its-breaking-a-lot-of-apps-222011637.html) were the root cause of the issues and were realistically unresolvable. I spent time playing around with alternatives like Scweet (https://github.com/Altimis/Scweet) but found that they were either too buggy or the owners were too unresponsive for them to be reliable resources.

```
pip install -U stweet
```

```
import stweet as st
search_tweets_task = st.SearchTweetsTask(
    all_words='#HurricaneSandy'
)
tweets_collector = st.CollectorTweetOutput()
st.TweetSearchRunner(
    search_tweets_task=search_tweets_task,
    tweet_outputs=[tweets_collector, st.CsvTweetOutput('output_file.csv')]
).run()
tweets = tweets_collector.get_scrapped_tweets()
```

```
import stweet as st
search_tweets_task = st.SearchTweetsTask(all_words='#HurricaneSandy')
    output_jl_tweets = st.JsonLineFileRawOutput('output_raw_search_tweets.jl')
    output_jl_users = st.JsonLineFileRawOutput('output_raw_search_users.jl')
    output_print = st.PrintRawOutput()
    st.TweetSearchRunner(search_tweets_task=search_tweets_task,
                         tweet_raw_data_outputs=[output_print, output_jl_tweets],
                         user_raw_data_outputs=[output_print, output_jl_users]).run()
```