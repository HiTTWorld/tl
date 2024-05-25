import pandas as pd
import streamlit as st
# pip install openpyxl

# Set the title of the main page
st.title("Movie Project")

# Add items to the sidebar
with st.sidebar:
    st.header("Getting started")
    st.write("Demo: Survey")
    st.write("Demo: User management")
   
df = pd.read_csv('Moive_Boxoffice.csv') # 

