import pandas as pd
import re

def preprocess(data):
    pattern = r"\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{2,4}\s[a-z]+\s-\s"

    msg = re.split(pattern,data)[1:]
    date = re.findall(pattern,data)

    df = pd.DataFrame({
        "Date":date,
        "Message":msg
    })

    df['Date'] = pd.to_datetime(
        df['Date']
        .str.split(' -').str[0]
        .str.replace('\u202f', ' ', regex=False)
        .str.strip(),
        format='%d/%m/%y, %I:%M %p'
    )

    username = []
    user_message = []

    for message in df["Message"]:
        entry = re.split(r"([\w\W]+?):\s",message)
        if entry[1:]: # List items more than 1
            username.append(entry[1])
            user_message.append(entry[2])
        else:
            username.append("Group Notification")
            user_message.append(entry[0])
            
    df["User_message"] = user_message  
    df["Username"] = username  

    df.drop(columns=["Message"],inplace=True)

    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.month_name()
    df["Day"] = df["Date"].dt.day
    df["Day_Name"] = df["Date"].dt.day_name()
    df["Hour"] = df["Date"].dt.hour
    df["Minute"] = df["Date"].dt.minute 

    return df