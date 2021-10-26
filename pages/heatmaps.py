import streamlit as st
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import cm
from io import BytesIO
from cryptography.fernet import Fernet


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    #loading data
    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/heatmaps/monthly.csv', 'rb') as enc_m_file:
        enc_m = enc_m_file.read()
    dec_m = dkey_fernet.decrypt(enc_m)

    with open('datasets/heatmaps/weekly.csv', 'rb') as enc_w_file:
        enc_w = enc_w_file.read()
    dec_w = dkey_fernet.decrypt(enc_w)

    @st.cache
    def load_monthly():
        monthly_pre = pd.read_csv(BytesIO(dec_m))
        monthly_pre['Month'] = pd.to_datetime(
            monthly_pre['Date']).dt.month_name()
        return monthly_pre

    @st.cache
    def load_weekly():
        return pd.read_csv(BytesIO(dec_w))

    df_monthly = load_monthly()
    df_weekly = load_weekly()

    st.markdown(read_markdown_file('descriptions/heatmaps/overview.md'))

    #monthly heatmap target variable: user inuput
    monthly_heatmap = st.beta_expander("Show monthly heatmap")

    with monthly_heatmap:
        selected_col = st.selectbox("",
                                    ['Sleep', 'Internet', 'Hobbies', 'Wasted'],
                                    key='monthly')
        #pivoting monthly data
        @st.cache
        def get_monthly():
            monthly = pd.pivot_table(df_monthly,
                                     values=selected_col,
                                     index=['Month'],
                                     columns="Time")
            m = df_monthly.Month.unique().tolist()
            monthly = monthly.loc[m]
            return monthly

        heatmap_monthly = get_monthly()
        plt.figure(figsize=(12, 3))
        ax = sns.heatmap(
            heatmap_monthly,
            square=True,
            cmap=cm.viridis,
        )
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=6)
        ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=6)
        st.pyplot(ax.figure)

    #weekly heatmap target variable: user inuput
    weekly_heatmap = st.beta_expander("Show weekly heatmap")

    with weekly_heatmap:
        selected_col = st.selectbox("",
                                    df_weekly.columns[2:].tolist(),
                                    key='weekly')

        #pivoting weekly data
        @st.cache
        def get_weekly():
            weekly = pd.pivot_table(df_weekly,
                                    values=selected_col,
                                    index=["Weeknum"],
                                    columns="Time")
            return weekly

        heatmap_weekly = get_weekly()

        #weekly heatmap plot
        plt.figure(figsize=(15, 4))
        ax = sns.heatmap(heatmap_weekly, cmap=cm.viridis)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=6)
        ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=6)
        st.pyplot(ax.figure)