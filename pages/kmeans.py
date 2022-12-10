import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans
from utils.decryption import decrypt_data

st.title('K-means clustering')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()


def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


@st.cache
def load_data():
    return decrypt_data('datasets/kmeans/kmeans_jittered.csv')


dataset = load_data()

available_cols = dataset.columns.tolist()

left1, mid1, right1 = st.columns(3)

x_axis = left1.selectbox("Choose x-axis", available_cols)
y_axis = mid1.selectbox("Choose y-axis", available_cols, index=3)

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


clusters_input = right1.number_input('Select number of clusters',
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

left, right = st.columns(2)
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
