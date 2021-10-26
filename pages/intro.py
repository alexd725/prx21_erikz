import streamlit as st
from pathlib import Path


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    st.warning(
        "**{}To have the best viewing experience, head over to the menu in the upper right corner -> Settings -> Set 'Theme' to 'Light' and make sure 'Wide mode' is checked**"
        .format('&ensp;' * 11))

    # intro expander:
    st.markdown(read_markdown_file('descriptions/intro/prx21.md'))
    st.info(
        "If you'd like to see what exactly I tracked, how I tracked it, and just the general approach of data collection, have a look at some of the sections at the bottom of this page."
    )
    st.markdown(read_markdown_file('descriptions/intro/structure.md'))

    #TIME TRACKING SECITON
    st.markdown("# Time tracking")
    ##methods expander
    with st.beta_expander("Methods"):
        st.markdown(
            read_markdown_file("descriptions/intro/tt_methods_expander.md"))

    ##excel layout images expander
    with st.beta_expander("Excel layout images"):
        st.image("images/intro/tt_layout/tt_empty.png", caption="Base layout")
        st.image("images/intro/tt_layout/tt_vals.png",
                 caption="Layout filled with sample values")
        st.image("images/intro/tt_layout/tt_colors.png",
                 caption="Color coding for easy navigation")

    ##data transformation expander
    with st.beta_expander('Data transformation'):
        st.markdown(read_markdown_file('descriptions/intro/segmented.md'))
        st.image(
            'images/intro/segmented/normal.png',
            caption='The original structure as tracked in the Excel sheet')
        st.image('images/intro/segmented/seg.png',
                 caption='Segmented data structure')

    #QS SECITON
    st.markdown("# Qunatified self")
    ## methods expander
    with st.beta_expander("Methods: general structure"):
        st.markdown(read_markdown_file("descriptions/intro/qt_methods.md"))

    with st.beta_expander("Methods: health & self-related variables"):
        st.markdown(read_markdown_file("descriptions/intro/qt_healthself.md"))

    with st.beta_expander("Methods: food variables"):
        st.markdown(read_markdown_file("descriptions/intro/qt_food_vars.md"))

    with st.beta_expander("Methods: supplement variables"):
        st.markdown(read_markdown_file("descriptions/intro/qt_supps.md"))

    with st.beta_expander(
            "Possible causes of distortion in tracking the data"):
        st.markdown(read_markdown_file("descriptions/intro/qt_distortion.md"))

    with st.beta_expander("A list of everything I tracked"):
        st.markdown(read_markdown_file("descriptions/intro/qt_all_vars.md"))
