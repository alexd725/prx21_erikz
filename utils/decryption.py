import streamlit as st
import pandas as pd
from cryptography.fernet import Fernet
import io

def decrypt_data(filepath):
    key = st.secrets['key']

    fernet = Fernet(key)
    with open(filepath, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    df = pd.read_csv(io.StringIO(decrypted.decode('utf-8')))
    return df