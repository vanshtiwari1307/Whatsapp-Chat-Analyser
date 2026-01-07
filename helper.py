from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji as emj
from collections import Counter
e = URLExtract()

# TOP STATS
def top_stats(select_user,df):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]
    
    # Total Messages
    total_msg = df.shape[0] 

    # Total Words
    w = []
    for msg in df["User_message"]:
        w.extend(msg.split())
    total_words = len(w)

    # Total Media
    total_media = df[df['User_message'] == "<Media omitted>\n"].shape[0]

    # Total Links
    link = []
    for msg in df["User_message"]:
        link.extend(e.find_urls(msg))
    total_link = len(link)

    return total_msg,total_words,total_media,total_link

# MOST BUSY USER:
def most_busy_user_bar(df):
    x = df["Username"].value_counts().head()
    return x
def most_busy_user_dataframe(df):
    y = round((df["Username"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"Username":"User","count":"Percentage"})
    return y

# WordCloud
def wordcloud(select_user,df):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]

    temp = df[(df["Username"] != "Group Notification") & (df["User_message"] != "<Media omitted>\n")]
    we = WordCloud(width=1000,height=1000,stopwords=set(['media', 'omitted']),background_color="#0E1117",colormap="viridis")

    wc = we.generate(temp["User_message"].str.cat(sep=""))
    return wc

def most_common_word(select_user,df):
    from collections import Counter
    if select_user != "Overall":
        df = df[df["Username"]==select_user]
    temp = df[(df["Username"] != "Group Notification") & (df["User_message"] != "<Media omitted>\n")]
    f = open("stop_hinglish.txt")
    stopwords = f.read()
    w = []
    for line in temp["User_message"]:
        for word in line.lower().split():
            if word not in stopwords:
                w.append(word)
        
    new_df = pd.DataFrame(Counter(w).most_common(20),columns=["Words","Count"])
    return new_df

#  Monthly Timeline
def monthly_timeline(df,select_user):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]   

    timeline = []
    time = df.groupby(["Year","Month","Month_Name"]).count()["User_message"].reset_index()
    for i in range(time.shape[0]):
        timeline.append(str(time["Year"][i])+"-"+time["Month_Name"][i])
    time["Timeline"] = timeline
    return time 

# Daily Timeline
def daily_timeline(df,select_user):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]   

    df["Date_only"] = df["Date"].dt.date
    dt = df.groupby("Date_only").count()["User_message"].reset_index().rename(columns={"Date_only":"Date"})
    return dt


# Busy Days
def busy_day(df,select_user):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]
    bd = df.groupby("Day_Name").count()["User_message"]
    return bd

# Busy Months
def busy_month(df,select_user):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]
    bm = df.groupby("Month_Name").count()["User_message"]
    return bm

# Weekly Activity
def weekly_activity(df,select_user):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]
    periods = []
    for i in df["Hour"]:
        if i == 23:
            periods.append(str(i)+"-"+(str(00)))
        elif i == 00:
            periods.append(str(i)+"-"+(str(i+1)))
        else:
            periods.append(str(i)+"-"+(str(i+1)))
    df["Periods"] = periods
    new = df.pivot_table(index="Day_Name",columns="Periods",values="User_message",aggfunc="count").fillna(0)
    return new



# Emozi Analysis
def emozi_data(df,select_user):
    if select_user != "Overall":
        df = df[df["Username"]==select_user]
    emozi = [
        c
        for msg in df["User_message"]
        for c in msg
        if emj.is_emoji(c)
    ]

    e_df = pd.DataFrame(Counter(emozi).most_common(10),columns=["Emozi","Count"])
    return e_df