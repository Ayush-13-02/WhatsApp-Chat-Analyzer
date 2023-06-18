from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()
def fetch_stats(selected_user,df):
    # 1. fetch number of messages
    # 2. number of words
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    links = []
    for message in df['message']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    return num_messages, len(words), num_media_messages, len(links)

def fetchMostBusy(df):
    x = df['user'].value_counts().head()
    df = round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'user':'Name','count':'Percentage'})

    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10,background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

def mostCommonWord(selected_user,df):
    F = open('stop_hinglish.txt', 'r', encoding='utf-8')
    d = F.read()
    stop_words = []
    for word in d.split("\n"):
        stop_words.append(word)

    df = df[df['user'] != 'group_notification']
    df = df[df['message'] != '<Media omitted>\n']

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    list = []

    for message in df['message']:
        for words in message.lower().split():
            if words not in stop_words:
                list.append(words)

    most_common_df = pd.DataFrame(Counter(list).most_common(20))

    return most_common_df

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    emojis = []

    for message in df['message']:
        for word in message:
            if emoji.emoji_count(word):
                emojis.append(word)

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(emojis)))
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month']).count()['message'].reset_index()
    time = []
    for i in range(len(timeline)):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    df['only_date'] = df['date'].dt.date
    d_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return d_timeline

def weekly_activity_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df['day_name'] = df['date'].dt.day_name()
    return df.groupby(['day_name']).count()['message'].reset_index()

def monthly_activity_analysis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df.groupby(['month']).count()['message'].reset_index()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)

    return user_heatmap

