import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from io import BytesIO
from cryptography.fernet import Fernet
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    with st.beta_expander("What is the decision tree algorithm?"):
        st.info(
            '_The author of this excellent infographic is Avik Jain. Check him out [here](https://github.com/Avik-Jain)._'
        )
        a, b, c = st.beta_columns([1, 3, 1])
        with b:
            st.image("images/dtree/decision_tree.jpg",
                     use_column_width="always")

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
    left, right = st.beta_columns([1, 1])
    cb = st.sidebar.beta_container()

    st.sidebar.markdown('# &ensp;&ensp;&ensp;`Model parameters`')
    # preprocessing and setting some model parameters
    features_available = df.columns[3:].tolist()

    chosen_col = st.sidebar.selectbox("Variable to predict",
                                      features_available[15:])

    features_available.remove(chosen_col)

    #model features user input
    with right:
        features_input = st.multiselect("Model features",
                                        features_available,
                                        default=features_available)

    #test/train split input
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

    #critertion function input
    crit_input = st.sidebar.selectbox(
        "Function to measure the quality of a split",
        ["gini", "entropy"],
    )

    #split strategy input
    splitter_input = st.sidebar.selectbox(
        "Strategy used to choose the split at each node",
        ["best", "random"],
    )

    #tree depth input
    depth_input = st.sidebar.selectbox(
        "Maximum tree depth",
        [None, 2, 3, 4, 5, 6],
    )

    #internal node split ipnut
    sample_split_input = st.sidebar.number_input(
        'Min. #n of node samples to split internal node',
        min_value=2,
        max_value=10,
        step=1,
        value=2)

    #leaf node samples input
    leaf_samples_input = st.sidebar.number_input(
        'Min. #n of samples needed for a leaf node',
        min_value=1,
        max_value=10,
        step=1,
        value=1)

    with st.sidebar.beta_expander('Sources'):
        st.markdown(read_markdown_file('descriptions/dtree/sources.md'))

    #a bad solution to center the text st.info/success/warning/error
    def spaces(size):
        return "&ensp;" * size

    #explanation of model parameters (expanders)
    with left:
        sp = spaces(19)
        st.success(
            '**{}Explanation of model parameters on the sidebar**'.format(sp))
        with st.beta_expander('Gini vs. entropy'):
            st.image('images/dtree/idk.png', caption='Figure 1')
            st.markdown(
                read_markdown_file('descriptions/dtree/gini_v_entropy.md'))

        with st.beta_expander(
                'Strategies used to decide the split at each node'):
            st.markdown(read_markdown_file('descriptions/dtree/splitter.md'))
        with st.beta_expander('Maximum tree depth; internal and leaf nodes'):
            st.image('images/dtree/dgram.png', caption='Figure 2')
            st.markdown(read_markdown_file('descriptions/dtree/3params.md'))

    X = df[features_input]
    y = df[chosen_col]

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=1 - ts_input,
                                                        random_state=30)

    #model function
    @st.cache(allow_output_mutation=True)
    def create_model():
        model = DecisionTreeClassifier(criterion=crit_input,
                                       random_state=0,
                                       max_depth=depth_input,
                                       splitter=splitter_input,
                                       min_samples_split=sample_split_input,
                                       min_samples_leaf=leaf_samples_input)

        model.fit(X_train, y_train)
        return model

    #confusion matrix
    @st.cache
    def get_confusion_matrix():
        return confusion_matrix(y_test, y_pred)

    #accuracy score
    def calculate_accuracy():
        return np.round((model.score(X_test, y_test) * 100), 2)

    #creating the model; running predictions
    try:
        model = create_model()
    except ValueError:
        st.button('Click here to run the algorithm and create a model')
        st.stop()
    y_pred = model.predict(X_test)
    # confusion matrix of actual vs. predicted
    with left:
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

    # model metrics
    testAcc = calculate_accuracy()
    with right:
        sp = spaces(19)
        st.info("**{} The model's classification accuracy is {}%**".format(
            sp, testAcc))

    #dataframe of feature importances
    importances_data = {
        "Feature name": features_input,
        "Feature importance": model.feature_importances_,
    }
    feature_importances = pd.DataFrame(data=importances_data)

    #feature chart
    feature_chart = alt.Chart(feature_importances).mark_bar().encode(
        x=alt.X("Feature name:N", sort="-y"),
        y="Feature importance:Q",
        tooltip=['Feature name', 'Feature importance']).properties(height=500)

    #feature importances expander
    with right:
        st.altair_chart(feature_chart, use_container_width=True)
        with st.beta_expander('What are feature importances?'):
            st.markdown(
                read_markdown_file('descriptions/dtree/importances.md'))

    #visualizing the decision tree
    if cb.button('Click here to visualize the decision tree'):
        try:
            st.info(
                "**I've re-written the variable classes for easier readibility:** 1=Very low; 2=Low; 3=Medium; 4=High; 5=Very high"
            )
            fig = plt.figure()
            _ = tree.plot_tree(
                model,
                feature_names=features_input,
                class_names=["Very low", "Low", "Medium", "High", "Very high"],
                filled=True,
                max_depth=3,
                fontsize=3)
            st.pyplot(fig)
        except AttributeError:
            st.warning('Initialize the model again')