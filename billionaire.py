import pandas as pd
from pandasql import sqldf
import queries
import streamlit as st

df=pd.read_csv('billionaire.csv')

query = queries.BILLIONAIRE_QUERY
result = sqldf(query)

def get_place(value):
    print("I am called")
    print("Received option", value)

st.write("""
# Simple SQL PROJECT

Shown are the stock closing price and volume of Google!
""")

native_place = st.selectbox("Place of Birth", options=[], key="place").on_change(get_place)

st.table(result)
