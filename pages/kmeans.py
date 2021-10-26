import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans
from io import BytesIO
from cryptography.fernet import Fernet


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    st.markdown('# K-means clustering')
    left, right = st.beta_columns(2)
    with right:
        with st.beta_expander("What is k-means clustering?"):
            st.info(
                '_The author of this excellent infographic is Avik Jain. Check him out [here](https://github.com/Avik-Jain)._'
            )
            st.image("images/kmeans/kmeans.jpg", use_column_width="always")

    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/kmeans/kmeans_jittered.csv', 'rb') as enc_file:
        enc = enc_file.read()
    dec = dkey_fernet.decrypt(enc)

    @st.cache
    def load_data():
        return pd.read_csv(BytesIO(dec))

    dataset = load_data()

    available_cols = dataset.columns.tolist()

    x_axis = st.sidebar.selectbox("Choose x-axis", available_cols)
    y_axis = st.sidebar.selectbox("Choose y-axis", available_cols, index=3)

    X = dataset[[x_axis, y_axis]].values

    @st.cache
    def get_wcss():
        wcss = []
        for i in range(1, 11):
            kmeans = KMeans(n_clusters=i,
                            init="k-means++",
                            max_iter=300,
                            n_init=10,
                            random_state=0)
            kmeans.fit(X)
            wcss.append(kmeans.inertia_)
        return wcss

    wcss = get_wcss()

    with left:
        with st.beta_expander(
                'How do I choose the optimal number of clusters on the sidebar?'
        ):
            st.markdown(read_markdown_file('descriptions/kmeans/clusters.md'))
            st.image('images/kmeans/example_chart.jpg')

    clusters_input = st.sidebar.number_input('Select number of clusters',
                                             min_value=2,
                                             max_value=7,
                                             value=3,
                                             step=1)

    @st.cache
    def create_model():
        model = KMeans(
            n_clusters=clusters_input,
            init="k-means++",
            max_iter=300,
            n_init=10,
            random_state=0,
        )
        model.fit(X)
        return model

    try:
        kmeans = create_model()
    except Exception:
        st.button('Click here to run the algorithm and create a model')
        st.stop()

    with left:
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(np.arange(1, 11, 1), wcss)
        ax.set_title("The 'elbow' chart")
        ax.set_xlabel("Number of clusters")
        ax.set_ylabel("Within-cluster sum of square")
        st.pyplot(fig)

    y_kmeans = kmeans.predict(X)
    colors = ["red", "blue", "green", "cyan", "magenta", "black", "darkorange"]

    with right:
        fig, ax = plt.subplots(figsize=(12, 6))
        for k in range(0, clusters_input):
            ax.scatter(
                X[y_kmeans == k, 0],
                X[y_kmeans == k, 1],
                s=100,
                c=colors[k],
                label="Cluster {}".format(k),
                alpha=1 / 3,
            )

        ax.scatter(
            kmeans.cluster_centers_[:, 0],
            kmeans.cluster_centers_[:, 1],
            s=150,
            c="yellow",
            label="Centroids",
        )
        ax.set_title("Chart of clusters")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.grid(linestyle="--", linewidth=0.5)
        ax.legend()
        st.pyplot(fig)

    with right:
        with st.beta_expander(
                'A note about data transformation for the plot above'):
            st.markdown(
                'Prior to plotting this, I jittered all values in Excel with `x+((RAND()-0.5)*0.3)` to prevent overlap and make it more aesthetically pleasing.'
            )
