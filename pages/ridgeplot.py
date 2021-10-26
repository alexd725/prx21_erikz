import streamlit as st
import pandas as pd
import joypy
from matplotlib import cm
from joypy import joyplot
from pathlib import Path
from io import BytesIO
from cryptography.fernet import Fernet


def app():
    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/main_data/main_data.csv', 'rb') as enc_file:
        enc = enc_file.read()
    dec = dkey_fernet.decrypt(enc)

    @st.cache
    def load_data():
        return pd.read_csv(BytesIO(dec))

    ridge = load_data()

    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    st.markdown(read_markdown_file('descriptions/ridgeplot/ridgeplot.md'))
    whoops = st.sidebar.beta_container()

    selected_cols = st.sidebar.selectbox(
        "Choose a variable to plot",
        ['Sleep', 'Internet', 'Hobbies', 'Wasted time'])

    col_min, col_max = ridge[selected_cols].min().astype(
        int), ridge[selected_cols].max().astype(int)

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

    with st.beta_expander(
            "A note about the density plots for the 'sleep' variable"):
        st.markdown(
            "If you're wondering why the plots in most months for 'sleep' reach extreme values, it's because I sometimes stay awake for a "
            "very long time (mild version of all-nighters), which greatly increases how long I'll need to sleep the next day. Healthy? _Nope._"
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
