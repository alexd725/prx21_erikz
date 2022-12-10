import streamlit as st
import altair as alt
import pandas as pd
from utils.variables import MAIN_DATA_TIME_VARS, MAIN_DATA_CATEGORICAL_VARS, MAIN_DATA_SUPPLEMENTAL_VARS
from utils.decryption import decrypt_data

st.title('Scatterplots')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()

@st.cache
def load_data():
    return decrypt_data('datasets/scatter/scatter.csv')


df = load_data()

st.info(
    '**Hold left-click and drag to make a selection.**'
    ' **Hold left-click again and drag it around to see a "cross-section" of where the data points inside the selection appear in other scatterplots.**'
)

available = MAIN_DATA_TIME_VARS + \
    MAIN_DATA_CATEGORICAL_VARS + MAIN_DATA_SUPPLEMENTAL_VARS

selected_axis = st.sidebar.selectbox('Y-axis', available)
idx = available.index(selected_axis)
x_remaining = available[:idx] + available[idx + 1:]

selected_scale = st.sidebar.selectbox(
    'Variable to use as a scale',
    MAIN_DATA_TIME_VARS,
    index=0)

selected_x = st.sidebar.multiselect("Select x",
                                    x_remaining,
                                    default=x_remaining[:3])

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
split_plots = [plot_list[x:x + 3] for x in range(0, len(plot_list), 3)]

aligned_plots = []

for n in range(len(split_plots)):
    aligned_plots.append(alt.hconcat(*split_plots[n]))

st.altair_chart(alt.vconcat(*aligned_plots))

with st.expander(
        'A note about data transformation for the plots above',
        expanded=True):
    st.markdown(
        'Prior to plotting this, I jittered all values in Excel with `x+((RAND()-0.5)*0.3)` to prevent overlap and make it more aesthetically pleasing.'
    )
