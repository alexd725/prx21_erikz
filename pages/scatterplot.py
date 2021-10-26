import streamlit as st
import altair as alt
import pandas as pd
from io import BytesIO
from cryptography.fernet import Fernet


def app():
    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/scatter/scatter.csv', 'rb') as enc_file:
        enc = enc_file.read()
    dec = dkey_fernet.decrypt(enc)

    @st.cache
    def load_data():
        return pd.read_csv(BytesIO(dec))

    df = load_data()

    st.info(
        '**Hold left-click and drag to make a selection.**'
        ' **Hold left-click again and drag it around to see a "cross-section" of where the data points inside the selection appear in other scatterplots.**'
    )

    available = df.columns[1:].tolist()

    selected_axis = st.sidebar.selectbox('Y-axis', available, index=1)
    idx = available.index(selected_axis)
    x_remaining = available[:idx] + available[idx + 1:]

    selected_scale = st.sidebar.selectbox(
        'Variable to use as a scale',
        ['Sleep', 'Hobbies', 'Internet', 'Wasted time'],
        index=0)

    selected_x = st.sidebar.multiselect("Select x",
                                        x_remaining,
                                        default=x_remaining)

    brush = alt.selection_interval()
    scatter_chart = (alt.Chart(df).mark_point(color="purple").encode(
        y="{}:Q".format(selected_axis),
        color=alt.condition(
            brush,
            "{}:Q".format(selected_scale),
            alt.value("lightgray"),
            scale=alt.Scale(scheme="viridis"),
        ),
    ).properties(width=350, height=350).add_selection(brush))

    plot_list = []
    for i in selected_x:
        to_plot = scatter_chart.encode(x="{}:Q".format(i))
        plot_list.append(to_plot)
    split_plots = [plot_list[x:x + 4] for x in range(0, len(plot_list), 4)]

    aligned_plots = []

    for n in range(len(split_plots)):
        aligned_plots.append(alt.hconcat(*split_plots[n]))

    st.altair_chart(alt.vconcat(*aligned_plots))

    with st.beta_expander(
            'A note about data transformation for the plots above',
            expanded=True):
        st.markdown(
            'Prior to plotting this, I jittered all values in Excel with `x+((RAND()-0.5)*0.3)` to prevent overlap and make it more aesthetically pleasing.'
        )
