import streamlit as st

from src.data_loader import load_dataset
from src.data_loader import get_record_count

st.title("Toronto Crime Indicators Analytics Tool")

try:
    df = load_dataset("data/Toronto_Crime_Indicators.csv")

    st.success("Dataset loaded successfully.")

    st.write(
        f"Total records loaded: {get_record_count(df):,}"
    )

    st.dataframe(df.head())

except FileNotFoundError as error:
    st.error(str(error))