import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from utils.variables import MAIN_DATA_TIME_VARS, MAIN_DATA_CATEGORICAL_VARS, MAIN_DATA_SUPPLEMENTAL_VARS
from utils.decryption import decrypt_data

st.title('Decision Tree Classifier')
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
left, right = st.columns([1, 1])
cb = st.sidebar.container()

st.sidebar.markdown('# `Model parameters`')
chosen_col = st.sidebar.selectbox("Variable to predict",
                                  MAIN_DATA_CATEGORICAL_VARS)


with right:
    time_features_input = st.multiselect("Time features",
                                         MAIN_DATA_TIME_VARS,
                                         default=MAIN_DATA_TIME_VARS)

    chosen_col_index = MAIN_DATA_CATEGORICAL_VARS.index(chosen_col)
    available_categorical_features = MAIN_DATA_CATEGORICAL_VARS[:chosen_col_index] + \
        MAIN_DATA_CATEGORICAL_VARS[chosen_col_index + 1:]
    categorical_features_input = st.multiselect("Categorical features",
                                                available_categorical_features,
                                                default=available_categorical_features)

    supplemental_features_input = st.multiselect("Supplemental features",
                                                 MAIN_DATA_SUPPLEMENTAL_VARS,
                                                 default=MAIN_DATA_SUPPLEMENTAL_VARS[1:4])


features_input = time_features_input + \
    categorical_features_input + supplemental_features_input
# test/train split input
ts_input = st.sidebar.number_input(
    "Training data size",
    min_value=0.5,
    max_value=0.9,
    step=0.05,
    value=0.75,
)


# critertion function input
crit_input = st.sidebar.selectbox(
    "Function to measure the quality of a split",
    ["gini", "entropy"],
)

# split strategy input
splitter_input = st.sidebar.selectbox(
    "Strategy used to choose the split at each node",
    ["best", "random"],
)

# tree depth input
depth_input = st.sidebar.selectbox(
    "Maximum tree depth",
    [None, 2, 3, 4, 5, 6],
)

# internal node split ipnut
sample_split_input = st.sidebar.number_input(
    'Min. #n of node samples to split internal node',
    min_value=2,
    max_value=10,
    step=1,
    value=2)

# leaf node samples input
leaf_samples_input = st.sidebar.number_input(
    'Min. #n of samples needed for a leaf node',
    min_value=1,
    max_value=10,
    step=1,
    value=1)


def spaces(size):
    return "&ensp;" * size


X = df[features_input]
y = df[chosen_col]

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=1 - ts_input,
                                                    random_state=30)

# model function


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

# confusion matrix


@st.cache
def get_confusion_matrix():
    return confusion_matrix(y_test, y_pred)

# accuracy score


def calculate_accuracy():
    return np.round((model.score(X_test, y_test) * 100), 2)


# creating the model; running predictions
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

# dataframe of feature importances
importances_data = {
    "Feature name": features_input,
    "Feature importance": model.feature_importances_,
}
feature_importances = pd.DataFrame(data=importances_data)

# feature chart
feature_chart = alt.Chart(feature_importances).mark_bar().encode(
    x=alt.X("Feature name:N", sort="-y"),
    y="Feature importance:Q",
    tooltip=['Feature name', 'Feature importance']).properties(height=500)


# visualizing the decision tree
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
