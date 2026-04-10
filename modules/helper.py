from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import streamlit as st

extract = URLExtract()

@st.cache_data
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # 1. Total Messages
    num_messages = df.shape[0]

    # 2. Total Words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # 3. Total Media Shared
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # 4. Total Links Shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

@st.cache_data
def most_busy_users(df):
    if df.empty or df.shape[0] == 0: 
        return pd.Series(), pd.DataFrame(columns=['Name', 'Percent'])
    x = df['user'].value_counts().head()
    df_percent = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    df_percent.columns = ['Name', 'Percent']
    return x, df_percent

@st.cache_data
def create_wordcloud(selected_user, df):
    if df.empty: return None
    try:
        with open('data/stop_hinglish.txt', 'r') as f:
            stop_words = f.read()
    except:
        stop_words = ""

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    from wordcloud import WordCloud
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].apply(remove_stop_words).str.cat(sep=" "))
    return df_wc

@st.cache_data
def most_common_words(selected_user, df):
    if df.empty: return pd.DataFrame()
    try:
        with open('data/stop_hinglish.txt', 'r') as f:
            stop_words = f.read()
    except:
        stop_words = ""

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    from collections import Counter
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

@st.cache_data
def emoji_helper(selected_user, df):
    if df.empty: return pd.DataFrame()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    res = df['day_name'].value_counts().reset_index()
    res.columns = ['Day', 'Count']
    return res

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    res = df['month'].value_counts().reset_index()
    res.columns = ['Month', 'Count']
    return res

@st.cache_data
def activity_heatmap(selected_user, df):
    if df.empty: return pd.DataFrame()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    try:
        if df.empty: return pd.DataFrame()
        # 1. Pivot with period columns
        user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
        
        if user_heatmap.empty: return pd.DataFrame()

        # 2. Reorder Days chronologically
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        user_heatmap = user_heatmap.reindex(days_order).fillna(0)
        
        # 3. Reorder Periods (0-23)
        def sort_key(col):
            try:
                return int(str(col).split('-')[0])
            except:
                return 99
        
        sorted_columns = sorted(user_heatmap.columns, key=sort_key)
        user_heatmap = user_heatmap[sorted_columns]
        
        return user_heatmap
    except Exception as e:
        print(f"Heatmap error: {e}")
        return pd.DataFrame()

def generate_report_data(selected_user, df):
    num_messages, words, num_media_messages, num_links = fetch_stats(selected_user, df)
    report_dict = {
        "Metric": ["Total Messages", "Total Words", "Media Shared", "Links Shared"],
        "Value": [num_messages, words, num_media_messages, num_links]
    }
    return pd.DataFrame(report_dict)
