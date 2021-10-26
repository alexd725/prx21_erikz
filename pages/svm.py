import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
from pathlib import Path
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from io import BytesIO
from cryptography.fernet import Fernet


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    # import the main dataset
    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/main_data/main_data.csv', 'rb') as enc_file:
        enc = enc_file.read()
    dec = dkey_fernet.decrypt(enc)

    @st.cache(allow_output_mutation=True)
    def load_data():
        return pd.read_csv(BytesIO(dec))

    def spaces(size):
        return "&ensp;" * size

    df = load_data()
    st.markdown('# Support-vector machine (SVM)')
    st.success(
        '**SVMs are supervised learning models that can be employed for both classification and regression tasks.**'
        ' **Its objective is to find an optimal boundary (hyperplane) that separates (classifies) the data into distinct groups.**'
        ' **In 2D space, this boundary is simply a line. In 3D space, the boundary is a plane.**'
    )
    l_e, r_e = st.beta_columns(2)
    #explanatory figure 1
    with l_e:
        with st.beta_expander('Explanatory figure 1'):
            st.markdown(
                "> Red line = **hyperplane** | Orange rectangle  around hyperplane = **margin** | Data closest to the margin = **support vectors**"
            )
            st.image("images/svm_img/1_hyper.png",
                     caption="Figure 1",
                     width=560)

    #explanatory figure 2
    with r_e:
        with st.beta_expander('Explanatory figure 2'):
            st.markdown(
                "> Classification in cases where the target has multiple classes"
            )
            st.image(
                "images/svm_img/2_multiclass.png",
                caption="Figure 2",
                width=600,
            )

    sc = StandardScaler()
    left, right = st.beta_columns(2)

    features_available = df.columns[3:].tolist()

    chosen_col = st.sidebar.selectbox("Variable to predict",
                                      features_available[15:])

    features_available.remove(chosen_col)

    features_input = st.sidebar.multiselect("Model features",
                                            features_available,
                                            default=features_available)

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

    # kernels
    chosen_kernel = st.sidebar.selectbox("Kernel",
                                         ["rbf", "linear", "poly", "sigmoid"])

    with left:
        sp = spaces(19)
        st.warning(
            '**{} Explanation of model parameters on the sidebar**'.format(sp))
        with st.beta_expander("What are the differences between kernels?"):
            st.markdown(read_markdown_file("descriptions/svm/kernel.md"))
            st.image("images/svm_img/3_kernels.png", caption="Figure 3")
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
    with left:
        with st.beta_expander("What is the misclassification penalty?"):
            st.markdown(read_markdown_file("descriptions/svm/c_param.md"))
            st.image("images/svm_img/4_regularization.png", caption="Figure 4")

    # gamma
    gamma_default = 1 / len(features_input)
    gamma_input = st.sidebar.number_input("Gamma",
                                          min_value=0.0,
                                          max_value=1.0,
                                          value=gamma_default,
                                          step=0.01)

    with st.sidebar.beta_expander('Sources'):
        st.markdown(read_markdown_file('descriptions/svm/sources.md'))

    with left:
        with st.beta_expander("What is gamma?"):
            st.markdown(read_markdown_file("descriptions/svm/gamma.md"))
            st.image("images/svm_img/5_gamma.png", caption="Figure 5")
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
        sp = spaces(19)
        st.info("**{} The model's classification accuracy is {}%**".format(
            sp, testAcc))

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
