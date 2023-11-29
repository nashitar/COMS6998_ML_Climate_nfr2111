
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