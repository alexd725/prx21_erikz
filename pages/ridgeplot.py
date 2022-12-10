import streamlit as st
import pandas as pd
import joypy
from matplotlib import cm
from joypy import joyplot
from pathlib import Path
from utils.decryption import decrypt_data

st.title('Ridgeline plot')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()

@st.cache
def load_data():
    return decrypt_data('datasets/ridgeline/ridgeline.csv')


ridge = load_data()

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


st.markdown(read_markdown_file('descriptions/ridgeplot/ridgeplot.md'))
whoops = st.sidebar.container()

selected_cols = st.sidebar.selectbox(
    "Choose a variable to plot",
    ['Sleep', 'Internet', 'Hobbies', 'Wasted time'])

col_min = int(ridge[selected_cols].min())
col_max = int(ridge[selected_cols].max())

custom_min = st.sidebar.number_input("X minimum",
                                     col_min,
                                     col_max,
                                     value=1,
                                     key='custom min')

custom_max = st.sidebar.number_input("X maximum",
                                     col_min,
                                     col_max,
                                     value=col_max,
                                     key='custom max')

date_view = st.sidebar.selectbox('Select data granularity',
                                 ['Month', 'Week'])


@st.cache
def get_labels():
    monthly = [y for y in list(ridge.Month.unique())]
    weekly = [y for y in list(ridge.Week.unique())]
    if date_view == 'Month':
        return monthly
    else:
        return weekly


labels = get_labels()

overlap_input = st.sidebar.number_input(
    'Overlap of plots',
    min_value=1,
    max_value=5,
    value=3 if date_view == 'Month' else 3,
    step=1,
    key='overlap')

f_width = st.sidebar.number_input('Figure width',
                                  min_value=8,
                                  max_value=16,
                                  step=1,
                                  value=10,
                                  key='width')

f_height = st.sidebar.number_input('Figure height',
                                   min_value=5,
                                   max_value=11,
                                   value=6 if date_view == 'Month' else 9,
                                   step=1,
                                   key='height')

tails_input = st.sidebar.number_input("Plots' tails",
                                      min_value=0.,
                                      max_value=2.,
                                      step=0.1,
                                      value=0.1,
                                      key='tails')

fig, axes = joypy.joyplot(
    ridge,
    by=date_view,
    column=selected_cols,
    labels=labels,
    range_style="own",
    grid=True,
    linewidth=0.5,
    x_range=[custom_min, custom_max],
    legend=False,
    linecolor="white",
    fade=True,
    figsize=(f_width, f_height),
    title="Ridgeline plot of {}".format(selected_cols.lower()),
    overlap=overlap_input,
    alpha=0.6,
    tails=tails_input,
    colormap=cm.cool,
)


n_bins = st.sidebar.number_input("X-axis grid interval",
                                 min_value=col_min,
                                 max_value=col_max,
                                 value=1,
                                 step=1,
                                 key='grid')

try:
    x_bins = list(range(custom_min, custom_max, n_bins))
    axes[-1].set_xticks(x_bins)
    st.pyplot(fig)
except (ValueError, TypeError):
    whoops.button("Click here to graph the ridgeplot")
