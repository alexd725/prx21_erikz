import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from utils.variables import MAIN_DATA_TIME_VARS, MAIN_DATA_CATEGORICAL_VARS, MAIN_DATA_SUPPLEMENTAL_VARS
from utils.decryption import decrypt_data

st.title('Linear regression')
st.markdown('---')

try:
    logged_user = st.session_state['logged_user']
except KeyError:
    st.error('You must be logged in to access this page')
    st.stop()

sc = StandardScaler()


@st.cache
def load_data():
    return decrypt_data('datasets/linreg/segmented.csv')


df = load_data()

available = MAIN_DATA_CATEGORICAL_VARS + \
    MAIN_DATA_TIME_VARS + MAIN_DATA_SUPPLEMENTAL_VARS

with st.sidebar.expander('Variable to predict', expanded=True):
    chosen_variable = st.selectbox(
        'Select from the list below', available, index=15)
    if chosen_variable in MAIN_DATA_CATEGORICAL_VARS:
        MAIN_DATA_CATEGORICAL_VARS.remove(chosen_variable)
    elif chosen_variable in MAIN_DATA_TIME_VARS:
        MAIN_DATA_TIME_VARS.remove(chosen_variable)
    else:
        MAIN_DATA_SUPPLEMENTAL_VARS.remove(chosen_variable)

with st.sidebar.expander('Time features', expanded=True):
    time_f = st.multiselect('Select from below',
                            MAIN_DATA_TIME_VARS, default=MAIN_DATA_TIME_VARS)

with st.sidebar.expander('QS features', expanded=True):
    quant_f = st.multiselect(
        'Select from below', MAIN_DATA_CATEGORICAL_VARS, default=MAIN_DATA_CATEGORICAL_VARS)

with st.sidebar.expander('Supplements features', expanded=True):
    supps_f = st.multiselect(
        'Select from below', MAIN_DATA_SUPPLEMENTAL_VARS, default=MAIN_DATA_SUPPLEMENTAL_VARS)

with st.sidebar.expander('A note about feature preprocessing'):
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
with st.sidebar.expander('What is this parameter?'):
    st.markdown(
        'A number defining the ratio of how much data to use for training and testing the model. The typical training dataset size is 70&ndash;75%.'
    )

X = df[features_input]
y = df[chosen_variable]

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
st.markdown('## Chart of predicted vs. actual values')

st.pyplot(fig)

f_names = pd.DataFrame(model.coef_, X.columns, columns=['Coefficients'])
plt.figure()
coeffs_chart = (f_names['Coefficients'].sort_values(ascending=True).plot(
    kind='barh', xlabel='', figsize=(10, 10)))
coeffs_chart.grid(linestyle="--", linewidth=0.5)
coeffs_chart.set_title('Feature coefficients')

st.markdown('## Chart of feature coefficients')
st.pyplot(coeffs_chart.figure)


def mse():
    return np.round(mean_squared_error(y_test, y_pred, squared=True), 2)


def rmse():
    return np.round(mean_squared_error(y_test, y_pred, squared=False), 2)


def mae():
    return np.round(mean_absolute_error(y_test, y_pred), 2)


st.markdown('## Model metrics')
a, b, c = st.columns(3)
with a:
    st.info('**Mean squared error:** {}'.format(mse()))
with b:
    st.info('**Root mean squared error:** {}'.format(rmse()))
with c:
    st.info('**Mean absolute error:** {}'.format(mae()))
