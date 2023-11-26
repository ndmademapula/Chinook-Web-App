import streamlit as st
import pyodbc
import pandas as pd
# Initialize connection.
# Uses st.cache_resource to only run once.

def main():
    st.set_page_config(layout="wide")
    st.title("Chinook")
    st.subheader("Kichi's Data Warehouse and Intergration Final project")
    st.write("Viết giởi thiệu đồ án, nhóm, workflow, project evaluation")


if __name__ == "__main__":
    main()
