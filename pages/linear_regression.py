import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from pathlib import Path
from io import BytesIO
from cryptography.fernet import Fernet
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error


def app():
    def read_markdown_file(markdown_file):
        return Path(markdown_file).read_text()

    st.markdown('# Introduction')
    with st.beta_expander("What is linear regression?"):
        a, b, c = st.beta_columns([1, 4, 1])
        with b:
            st.info(
                'The author of this excellent infographic is Avik Jain. Check him out [here](https://github.com/Avik-Jain).'
            )
            st.image("images/linreg/linreg.jpg", use_column_width="always")

    st.markdown('# Structure and explanation')
    with st.beta_expander('Target variables'):
        st.markdown(read_markdown_file('descriptions/linreg/targets.md'))
    with st.beta_expander('Features'):
        st.markdown(read_markdown_file('descriptions/linreg/features.md'))
    st.markdown('# Short QnA')
    with st.beta_expander(
            'Why can I set only the training data size and nothing else for the model?'
    ):
        st.markdown(read_markdown_file('descriptions/linreg/model.md'))
    with st.beta_expander(
            'Why does the x-axis in the chart of actual vs. predicted values have no labels?'
    ):
        st.markdown(read_markdown_file('descriptions/linreg/x_date.md'))
    with st.beta_expander(
            'Does using a multiple linear regression model on this data even make sense?'
    ):
        st.markdown(read_markdown_file('descriptions/linreg/comments.md'))
    with st.beta_expander(
            "The model's predicted values are suspiciously accurate. Why?"):
        st.markdown(read_markdown_file('descriptions/linreg/accuracy.md'))

    with st.beta_expander(
            'If this is a regression (as opposed to classification) model, why are ordinal variables available as targets?'
    ):
        st.markdown(read_markdown_file('descriptions/linreg/q_vars.md'))

    sc = StandardScaler()

    dkey = st.secrets['data_key']
    dkey_fernet = Fernet(dkey)
    with open('datasets/linreg/prx_seg_num.csv', 'rb') as enc_file:
        enc = enc_file.read()
    dec = dkey_fernet.decrypt(enc)

    @st.cache
    def load_data():
        return pd.read_csv(BytesIO(dec))

    df = load_data()
    available = [
        'Hobbies', 'Internet', 'Wasted', 'Restfulness', 'Mood', 'N:QT', 'N:QL',
        'N:QT'
    ]

    tf = [
        'Sleep', 'Work', 'Entertainment', 'Food', 'Social', 'Internet',
        'Hobbies', 'Fun', 'Wasted'
    ]
    qf = [
        'Breakfast', 'Breakfast-lunch', 'Lunch', 'Lunch-dinner', 'Dinner',
        'After dinner', 'Restfulness', 'Mood', 'SW:F', 'P:QL', 'P:QT', 'N:QL',
        'N:QT'
    ]
    sf = ['Caffeine', 'Iron', 'Zinc', 'Magnesium', 'Omega']

    with st.sidebar.beta_expander('Variable to predict', expanded=True):
        cc = st.selectbox('Select from the list below', available)
        if cc in tf:
            tf.remove(cc)
        elif cc in qf:
            qf.remove(cc)
        else:
            sf.remove(cc)

    with st.sidebar.beta_expander('Time features', expanded=True):
        time_f = st.multiselect('Select from below', tf, default=tf)

    with st.sidebar.beta_expander('QS features', expanded=True):
        quant_f = st.multiselect('Select from below', qf, default=qf)

    with st.sidebar.beta_expander('Supplements features', expanded=True):
        supps_f = st.multiselect('Select from below', sf, default=sf)

    with st.sidebar.beta_expander('A note about feature preprocessing'):
        st.markdown(
            "Since the features above are a combination of `time` and `qs` variables, they have been rescaled using sklearn's `StandardScaler`"
        )

    features_input = time_f + quant_f + supps_f

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

    X = df[features_input]
    y = df[cc]

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        y,
                                                        test_size=1 - ts_input,
                                                        random_state=30)

    X_train = sc.fit_transform(X_train)
    X_test = sc.fit_transform(X_test)

    try:
        model = LinearRegression(fit_intercept=True)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
    except ValueError:
        st.button('Click here to run the algorithm and create a model')
        st.stop()

    pepe = pd.DataFrame({'actual': y_test, 'predicted': y_pred})
    pepe.reset_index(inplace=True, drop=True)

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(pepe)
    ax.set_xticklabels('')
    ax.set_ylabel('Time amount')
    ax.set_title('Predicted vs. actual values')
    ax.legend(['actual', 'predicted'], prop={'size': 6})
    ax.grid(linestyle='--', linewidth=0.5)
    st.markdown('# Chart of predicted vs. actual values')
    with st.beta_expander('Expand to see...'):
        st.markdown(
            "_If the predicted values seem suspiciously accurate and you're wondering why, read the sections above._"
        )
        st.pyplot(fig)

    f_names = pd.DataFrame(model.coef_, X.columns, columns=['Coefficients'])
    plt.figure()
    coeffs_chart = (f_names['Coefficients'].sort_values(ascending=True).plot(
        kind='barh', xlabel='', figsize=(10, 5)))
    coeffs_chart.grid(linestyle="--", linewidth=0.5)
    coeffs_chart.set_title('Feature coefficients')

    st.markdown('# Chart of feature coefficients')
    with st.beta_expander('Expand to see...'):
        st.pyplot(coeffs_chart.figure)

    def mse():
        return np.round(mean_squared_error(y_test, y_pred, squared=True), 2)

    def rmse():
        return np.round(mean_squared_error(y_test, y_pred, squared=False), 2)

    def mae():
        return np.round(mean_absolute_error(y_test, y_pred), 2)

    st.markdown('# Model metrics')
    with st.beta_expander('Expand to see...'):
        a, b, c = st.beta_columns(3)
        with a:
            st.info('**Mean squared error:** {}'.format(mse()))
        with b:
            st.info('**Root mean squared error:** {}'.format(rmse()))
        with c:
            st.info('**Mean absolute error:** {}'.format(mae()))
