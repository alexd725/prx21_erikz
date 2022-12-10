import streamlit as st
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib import cm
from utils.variables import MAIN_DATA_TIME_VARS
from utils.decryption import decrypt_data

st.title('Heatmaps')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


@st.cache
def load_monthly():
    monthly_pre = decrypt_data('datasets/heatmaps/monthly.csv')
    monthly_pre['Month'] = pd.to_datetime(
        monthly_pre['Date']).dt.month_name()
    return monthly_pre


@st.cache
def load_weekly():
    return decrypt_data('datasets/heatmaps/weekly.csv')


df_monthly = load_monthly()
df_weekly = load_weekly()

with st.expander('Explanation of the heatmaps below'):
    st.markdown(read_markdown_file('descriptions/heatmaps/overview.md'))

# monthly heatmap target variable: user inuput
st.markdown('## Monthly heatmap')
selected_col = st.selectbox("Choose a variable to plot",
                            options=MAIN_DATA_TIME_VARS,
                            key='monthly')
# pivoting monthly data


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

# weekly heatmap target variable: user inuput

st.markdown('## Weekly heatmap')
selected_col = st.selectbox("Choose a variable to plot",
                            MAIN_DATA_TIME_VARS,
                            key='weekly')

# pivoting weekly data


@st.cache
def get_weekly():
    weekly = pd.pivot_table(df_weekly,
                            values=selected_col,
                            index=["Weeknum"],
                            columns="Time")
    return weekly


heatmap_weekly = get_weekly()

# weekly heatmap plot
plt.figure(figsize=(15, 4))
ax = sns.heatmap(heatmap_weekly, cmap=cm.viridis)
ax.set_ylabel("")
ax.set_xlabel("")
ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=6)
ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=6)
st.pyplot(ax.figure)
