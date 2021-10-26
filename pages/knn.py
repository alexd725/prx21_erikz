import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from pathlib import Path
from io import BytesIO
from cryptography.fernet import Fernet
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    def spaces(size):
        return "&ensp;" * size

    left, right = st.beta_columns(2)

    # import the main dataset
    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/main_data/main_data.csv', 'rb') as enc_file:
        enc = enc_file.read()
    dec = dkey_fernet.decrypt(enc)

    @st.cache
    def load_data():
        return pd.read_csv(BytesIO(dec))

    df = load_data()
    sc = StandardScaler()

    with right:
        sp = spaces(19)
        st.success('**{} K Nearest Neighbors Algorithm: Overview**'.format(sp))
        st.image(
            "images/knn_img/knn_exp.jpg",
            use_column_width="always",
            caption='The author of this excellent infographic is Avik Jain')

    # preprocessing and setting some model parameters
    features_available = df.columns[3:].tolist()
    chosen_col = st.sidebar.selectbox("Variable to predict",
                                      features_available[15:])
    features_available.remove(chosen_col)

    features_input = st.sidebar.multiselect("Model features",
                                            features_available,
                                            default=features_available)
    with st.sidebar.beta_expander('A note about feature preprocessing'):
        st.markdown(
            "Since the features above are a combination of `time` and `qs` variables, they have been rescaled using _sklearn's_ `StandardScaler`"
        )

    X = df[features_input]
    y = df[chosen_col]

    ts_input = st.sidebar.number_input(
        "Training data size",
        min_value=0.5,
        max_value=0.9,
        step=0.05,
        value=0.75,
    )
    with st.sidebar.beta_expander('What is this parameter?'):
        st.markdown(
            'A number defining the ratio of how much data to use for training and testing the model. The typical training dataset size is 70&ndash;75%.'
        )

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=1 - ts_input,
                                                        random_state=30)

    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    n_input = st.sidebar.number_input(
        "Number of neighbors",
        min_value=2,
        max_value=10,
        value=3,
        step=1,
    )

    if not n_input:
        with st.sidebar:
            st.warning("Please select the number of neighbors to use above")
            st.stop()

    weights_input = st.sidebar.selectbox("Weight function used in prediction",
                                         ["uniform", "distance"])

    with st.sidebar.beta_expander(
            "What are the differences between these two weight functions?"):
        st.markdown(read_markdown_file("descriptions/knn/weight_funcs.md"))

    # training and fitting the model
    @st.cache(allow_output_mutation=True)
    def create_model():
        model = KNeighborsClassifier(
            n_neighbors=n_input,
            metric="minkowski",
            p=2,
            weights=weights_input,
        )
        model.fit(X_train, y_train)
        return model

    try:
        model = create_model()
    except Exception:
        st.button('Click here to run the algorithm and create a model')
        st.stop()
    y_pred = model.predict(X_test)

    #accuracy
    def calculate_accuracy():
        return np.round((model.score(X_test, y_test) * 100), 2)

    # confusion matrix of actual vs. predicted
    @st.cache
    def get_confusion_matrix():
        return confusion_matrix(y_test, y_pred)

    testAcc = calculate_accuracy()

    #displaying the accuracy metric and confusion matrix
    with left:
        sp = spaces(19)
        st.info("**{} The model's classification accuracy is {}%**".format(
            sp, testAcc))
        labelY, labelX = np.unique(y_test), np.unique(y_pred)
        cm = get_confusion_matrix()
        labels = [1, 2, 3, 4, 5]
        labelY, labelX = cm.shape[0], cm.shape[1]
        ax = sns.heatmap(cm, annot=True, fmt="g")
        ax.set_title("Confusion matrix of predicted vs. actual values")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_xticklabels(labels[:labelX])
        ax.set_yticklabels(labels[:labelY])
        st.pyplot(ax.figure)
