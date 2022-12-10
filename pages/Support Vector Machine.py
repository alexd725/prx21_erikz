import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from utils.variables import MAIN_DATA_TIME_VARS, MAIN_DATA_CATEGORICAL_VARS, MAIN_DATA_SUPPLEMENTAL_VARS
from utils.decryption import decrypt_data

st.title('Support-vector machine (SVM)')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()


@st.cache(allow_output_mutation=True)
def load_data():
    return decrypt_data('datasets/main_data/main_data.csv')


df = load_data()

sc = StandardScaler()
left, right = st.columns(2)


chosen_col = st.sidebar.selectbox("Variable to predict",
                                  MAIN_DATA_CATEGORICAL_VARS)


with left:
    time_features_input = st.multiselect("Time features",
                                         MAIN_DATA_TIME_VARS,
                                         default=MAIN_DATA_TIME_VARS)

    chosen_col_index = MAIN_DATA_CATEGORICAL_VARS.index(chosen_col)
    available_categorical_features = MAIN_DATA_CATEGORICAL_VARS[:chosen_col_index] + \
        MAIN_DATA_CATEGORICAL_VARS[chosen_col_index + 1:]
    categorical_features_input = st.multiselect("Categorial features",
                                                available_categorical_features,
                                                default=available_categorical_features)

    supplemental_features_input = st.multiselect("Supplemental features",
                                                 MAIN_DATA_SUPPLEMENTAL_VARS,
                                                 default=MAIN_DATA_SUPPLEMENTAL_VARS[1:4])

features_input = time_features_input + \
    categorical_features_input + supplemental_features_input

X = df[features_input]
y = df[chosen_col]

ts_input = st.sidebar.number_input(
    "Training data size",
    min_value=0.5,
    max_value=0.9,
    step=0.05,
    value=0.75,
)


X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=1 - ts_input,
                                                    random_state=30)

X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

# kernels
chosen_kernel = st.sidebar.selectbox("Kernel",
                                     ["rbf", "linear", "poly", "sigmoid"])


poly_degree = 3

if chosen_kernel == "poly":
    poly_degree = st.sidebar.number_input(
        "Degree for the polynomial kernel",
        min_value=2,
        max_value=6,
        value=3,
        step=1,
    )

# regularization parameter
c_input = st.sidebar.number_input(
    "Misclassification penalty",
    min_value=0.25,
    max_value=3.0,
    value=1.0,
    step=0.25,
)


# gamma
gamma_default = 1 / len(features_input)
gamma_input = st.sidebar.number_input("Gamma",
                                      min_value=0.0,
                                      max_value=1.0,
                                      value=gamma_default,
                                      step=0.01)


if gamma_default == 1:
    st.button(
        "Confirm the parameters set above and re-calculate the model")

# training and fitting the model


@st.cache(allow_output_mutation=True)
def create_model():
    model = SVC(C=c_input,
                degree=poly_degree,
                kernel=chosen_kernel,
                gamma=gamma_input)
    model.fit(X_train, y_train)
    return model


try:
    model = create_model()
except Exception:
    st.button('Click here to run the algorithm and create a model')
    st.stop()
y_pred = model.predict(X_test)


def calculate_accuracy():
    return np.round((model.score(X_test, y_test) * 100), 2)


@st.cache
def get_confusion_matrix():
    return confusion_matrix(y_test, y_pred)


# confusion matrix of actual vs. predicted, accuracy metric
with right:
    testAcc = calculate_accuracy()
    st.info("**The model's classification accuracy is {}%**".format(
        testAcc))

    # confusion matrix
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
