import pandas as pd
import matplotlib.pyplot as plt

color_dict = {
    'Very Negative': 'red',
    'Negative': 'orange',
    'Neutral': 'yellow',
    'Positive': 'lightgreen',
    'Very Positive': 'darkgreen'
}

years = ['2007', '2008', '2009', '2013', '2016', '2019']

for year in years:
    df = pd.read_csv(f'etc/sentiment_output_{year}.csv')

    labels = dict(df['pred'].value_counts()).keys()
    colors = [color_dict[label] for label in labels]

    plt.pie(dict(df['pred'].value_counts()).values(), colors=colors)
    plt.legend(labels=labels)
    plt.savefig(f'sentiment_output_{year}.png')

# df = pd.read_csv('etc/sentiment_output_2008.csv')

# plt.pie(dict(df['pred'].value_counts()).values(), colors=['red', 'orange', 'yellow', 'lightgreen', 'darkgreen'])
# plt.legend(labels=dict(df['pred'].value_counts()).keys())
# plt.savefig('sentiment_output_2008.png')


# df = pd.read_csv('etc/sentiment_output_2009.csv')
# df = df.sort_values(by='pred')

# plt.pie(dict(df['pred'].value_counts()).values(), colors=['red', 'orange', 'yellow', 'lightgreen', 'darkgreen'])
# plt.legend(labels=dict(df['pred'].value_counts()).keys())
# plt.savefig('sentiment_output_2009.png')

# df = pd.read_csv('etc/sentiment_output_2013.csv')
# df = df.sort_values(by='pred')

# plt.pie(dict(df['pred'].value_counts()).values(), colors=['red', 'orange', 'yellow', 'lightgreen', 'darkgreen'])
# plt.legend(labels=dict(df['pred'].value_counts()).keys())
# plt.savefig('sentiment_output_2013.png')

# print(df.pred.value_counts())

# df = pd.read_csv('etc/sentiment_output_2016.csv')
# df = df.sort_values(by='pred')

# plt.pie(dict(df['pred'].value_counts()).values(), colors=['red', 'orange', 'yellow', 'lightgreen', 'darkgreen'])
# plt.legend(labels=dict(df['pred'].value_counts()).keys())
# plt.savefig('sentiment_output_2016.png')

# print(df.pred.value_counts())

# df = pd.read_csv('etc/sentiment_output_2019.csv')
# df = df.sort_values(by='pred')

# plt.pie(dict(df['pred'].value_counts()).values(), colors=['red', 'orange', 'yellow', 'lightgreen', 'darkgreen'])
# plt.legend(labels=dict(df['pred'].value_counts()).keys())
# plt.savefig('sentiment_output_2019.png')

# print(df.pred.value_counts())