import streamlit as st
from multipage import MultiPage
from pages import cn2, intro, line_chart, scatterplot, ridgeplot, heatmaps, kmeans, svm, knn, decision_tree, linear_regression

st.set_page_config(layout="wide",
                   page_title='ErikZ: Data analysis',
                   page_icon='🦊',
                   initial_sidebar_state='expanded')
s = f"""
<style>
.css-qbe2hs {{font-weight: bolder;border-radius: 0rem;color: rgb(255 255 255);width: inherit;background-color: rgb(0 0 0 / 80%);height: 3em;font-size: x-large;}}
<style>
"""
st.markdown(s, unsafe_allow_html=True)

st.markdown(""" <style>
footer {visibility: hidden;}
</style> """,
            unsafe_allow_html=True)


def main():
    app = MultiPage()
    app.add_page("Introduction", intro.app)
    app.add_page("Line charts", line_chart.app)
    app.add_page("Ridgeline plots", ridgeplot.app)
    app.add_page("Heatmaps", heatmaps.app)
    app.add_page("Scatterplots", scatterplot.app)
    app.add_page("K-means clustering", kmeans.app)
    app.add_page("Decision tree classifier", decision_tree.app)
    app.add_page("CN2 rule induction", cn2.app)
    app.add_page("Support-vector machine", svm.app)
    app.add_page('Multiple linear regression', linear_regression.app)
    app.add_page("K-nearest neighbors", knn.app)
    app.run()


if __name__ == '__main__':
    main()
