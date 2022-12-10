import streamlit as st
import altair as alt
import pandas as pd
from utils.decryption import decrypt_data

st.title('Line charts')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()

@st.cache
def load_data():
    return decrypt_data('datasets/main_data/main_data.csv')


df = load_data()

st.markdown(
    '# Interactive line chart visualization of selected time variables')

left, middle, right = st.columns(3)

with left:
    selected_cols = st.multiselect(
        "Select columns to plot",
        ['Sleep', 'Internet', 'Hobbies', 'Wasted time'],
        default="Sleep")

with middle:
    # select data granularity
    granularity_options = ["Monthly", "Weekly", "Daily"]
    granularity_radio = st.radio("Choose date view", granularity_options)
    gran = df.copy()
    gran.index = pd.to_datetime(gran["Date"])
    if granularity_radio == "Monthly":
        gran = gran.resample(rule="M").mean().round(1)
        gran.reset_index(inplace=True)
    elif granularity_radio == "Weekly":
        gran = gran.resample(rule="W").mean().round(1)
        gran.reset_index(inplace=True)
    elif granularity_radio == "Daily":
        gran = gran.resample(rule="D").mean().round(1)
        gran.reset_index(inplace=True)

with right:
    # axes scaling
    line_chart_options = ["X", "Y", "Both"]
    line_radio = st.radio("Enable scaling on axes:", line_chart_options)
    zoom_x = False
    zoom_y = False
    if line_radio == "X":
        zoom_x = True
    elif line_radio == "Y":
        zoom_y = True
    else:
        zoom_x = True
        zoom_y = True

# creating line chart

st.info(
    '**Interactive elements**: mousewheel to zoom; hold left click+drag to move around; double-click to reset zoom'
)

nearest = alt.selection(type='single',
                        nearest=True,
                        on='mouseover',
                        fields=['Date'],
                        empty='none')

line_chart = alt.Chart(gran).transform_fold(
    selected_cols).mark_line().encode(
        x=alt.X('Date:T',
                scale=alt.Scale(zero=False),
                axis=alt.Axis(titleFontSize=16)),
        y=alt.Y('value:Q',
                scale=alt.Scale(domain=(0, 16)),
                axis=alt.Axis(title="Time spent (hours)",
                              titleFontSize=16)),
        color=alt.Color('key:N',
                        legend=alt.Legend(title='Variable',
                                          titleFontSize=16,
                                          labelFontSize=16)))

selectors = alt.Chart(gran).transform_fold(
    selected_cols).mark_point().encode(
        x="Date:T",
        opacity=alt.value(0),
).add_selection(nearest)

points = line_chart.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0)))

text = line_chart.mark_text(
    align='left', dx=5,
    dy=-5).encode(text=alt.condition(nearest, 'value:Q', alt.value(' ')))

label = line_chart.mark_text(
    align='left', dx=0,
    dy=-20).encode(text=alt.condition(nearest, 'key:N', alt.value(' ')))

date_ = line_chart.mark_text(
    align='left', dx=0,
    dy=20).encode(text=alt.condition(nearest, 'Date:T', alt.value(' ')))

rules = alt.Chart(gran).transform_fold(selected_cols).mark_rule(
    color='gray').encode(x='Date:T', ).transform_filter(nearest)

chart = alt.layer(line_chart, selectors, points, rules, text, label,
                  date_).properties(width=1400,
                                    height=600).interactive(bind_x=zoom_x,
                                                            bind_y=zoom_y)

st.altair_chart(chart)
