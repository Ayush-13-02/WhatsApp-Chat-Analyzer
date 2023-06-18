import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import preprocessor,helper

st.sidebar.title("WhatsApp Chats Analyzer")
upload_file = st.sidebar.file_uploader("Choose a file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        mum_messages, words, media, links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.subheader("Total Messages")
            st.title(mum_messages)
        with col2:
            st.subheader("Total Words")
            st.title(words)
        with col3:
            st.subheader("Total Medias")
            st.title(media)
        with col4:
            st.subheader("Total Links")
            st.title(links)

        # Timeline
        st.title(" ")
        st.title(" ")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.header("Monthly Timeline")
            timeline = helper.monthly_timeline(selected_user,df)
            fig, ax = plt.subplots()
            ax.plot(timeline['time'],timeline['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Daily Timeline")
            daily_timeline = helper.daily_timeline(selected_user,df)
            plt.figure(figsize=(18, 10))
            fig, ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'])

            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Most Busy
        st.title(" ")
        col1, col2 = st.columns(2, gap="large")
        with col1:
            st.header("Most Busy Day")
            weekly_df = helper.weekly_activity_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(weekly_df['day_name'], weekly_df['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most Busy Month")
            monthly_df = helper.monthly_activity_analysis(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_df['month'], monthly_df['message'])

            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # finding busiest users in the group

        if selected_user == 'Overall':
            st.title(" ")

            st.title("Most Busy Users")
            x,new_df = helper.fetchMostBusy(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2, gap="large")

            with col1:
                ax.bar(x.index,x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        df_wc = helper.create_wordcloud(selected_user,df)
        st.title(" ")
        st.title("WordCloud")
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most Common Words

        most_common_df = helper.mostCommonWord(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title(" ")
        st.title("Most Common Words")
        st.pyplot(fig)

        # emoji analyzer

        emoji_df = helper.emoji_helper(selected_user,df)
        st.title(" ")
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax =plt.subplots()
            ax.pie(emoji_df[1].head(10),labels=emoji_df[0].head(10),autopct="%0.2f")
            st.pyplot(fig)

        # HeatMap

        st.title("")
        st.title("Weekly Activity Analysis")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)