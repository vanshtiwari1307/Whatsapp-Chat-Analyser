import streamlit as st
import transform,helper
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import sys

st.sidebar.title("Whatsapp Chat Analyser")




uploaded_file = st.sidebar.file_uploader("Choose a file")
# File uploder
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8") # Decode the data into string format
    df = transform.preprocess(data) # Transform the raw data into dataframe

    # Selectbox
    lst = df["Username"].unique().tolist()
    lst.remove("Group Notification")
    lst.sort()
    lst.insert(0,"Overall")
    select_user = st.sidebar.selectbox("Analysis wrt, ",lst)
    

    # Button
    if st.sidebar.button("Show Analysis"):

        # Top Stats
        total_msg,total_words,total_media,total_links= helper.top_stats(select_user,df)
        st.title(":gray[Top Statistics]📊")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.write("📱 Total Message")
            st.header(f":orange[{total_msg}]")
        with col2:
            st.write("💬 Total Words")
            st.header(f":orange[{total_words}]")
        with col3:
            st.write("📎Total Media")
            st.header(f":orange[{total_media}]")
        with col4:
            st.write("🔗 Total Links Shared")
            st.header(f":orange[{total_links}]")



        # Daily Timeline
        st.title(":gray[Daily Timeline 📈]")
        date = helper.daily_timeline(df,select_user)
        st.line_chart(data=date,x="Date",y="User_message")


        # Montly Timeline
        st.title(":gray[Monthly Timeline 📈]")
        time = helper.monthly_timeline(df,select_user)
        st.line_chart(data=time, x="Timeline", y="User_message")


        # Most busy uesr dataframe and bar chart
        if select_user == "Overall":
            st.title(":gray[📊 Most Busy Users]")
            x = helper.most_busy_user_bar(df)
            y = helper.most_busy_user_dataframe(df)
            col1,col2 = st.columns(2)
            with col1:
                st.bar_chart(x) 
            with col2:
                st.dataframe(y)


        col1,col2 = st.columns(2)
        with col1:
            # Most Busy Days
            st.header(":gray[📊 Most Busy Days]")
            busy_day = helper.busy_day(df,select_user)
            st.bar_chart(busy_day)
        with col2:
            # Most Busy Months
            st.header(":gray[📊 Most Busy Months]")
            busy_month = helper.busy_month(df,select_user)
            st.bar_chart(busy_month)


         # Weekly Activity
        st.title(":gray[Weekly Activity]")
        new_df = helper.weekly_activity(df,select_user)  
        fig,ax = plt.subplots()
        fig.patch.set_alpha(0)          # or fig.patch.set_facecolor("none")
        ax.set_facecolor("none")

        ax = sns.heatmap(new_df) 
        ax.set_xlabel("Time Periods", color="white")      # x‑axis label color
        ax.set_ylabel("Days", color="white")  
        ax.tick_params(axis="x", colors="white")     # x tick labels + ticks
        ax.tick_params(axis="y", colors="white")     # y tick labels + ticks
        st.pyplot(fig)




        # WordCloud
        st.title(":gray[WordCloud]")
        wc = helper.wordcloud(select_user,df)
        fig, ax = plt.subplots(figsize=(4,6))
        fig.patch.set_facecolor('#0E1117')
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig, use_container_width=True)




        # Most used words bar chart
        st.title(":gray[📊 Most used words]")
        new_df = helper.most_common_word(select_user,df)
        st.bar_chart(data=new_df, x="Words", y="Count")


        # Emoji Analysis
        st.title(":gray[Most used Emojis]")
        col1,col2 = st.columns(2)
        e_df = helper.emozi_data(df,select_user)
        with col1:
            import plotly.express as px
            fig = px.pie(e_df, values="Count", names="Emozi")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(e_df)
else:
    st.title("📂 Upload a WhatsApp Chat[.txt] File to Begin Analysis")
    st.image("bg-12.webp")

col1,col2,col3,col4 = st.columns(4)
    
with col1:
    st.sidebar.image("link.webp",width=30)
    st.sidebar.link_button("LinkedIn", "https://www.linkedin.com/in/vansh-tiwari-709094309/")
with col2:
    st.sidebar.image("insta.webp",width=30)
    st.sidebar.link_button("Instagram", "https://www.instagram.com/_vansh.tiwari13_?igsh=MWlwM2o5aTQzaGRlZg==")

        

        


    
        

        
