import streamlit as st
import pandas as pd
import pyodbc
from PIL import Image
# Initialize connection.
# Uses st.cache_resource to only run once.
st.set_page_config(layout="wide")
st.title("Chinook Dataset Overview")
st.warning("Viết giới thiệu datasets cách ETL, tạo cube, và description cho từng table, visualize table (nếu t siêng)")
@st.cache_resource
def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + st.secrets["server"]
        + ";DATABASE="
        + st.secrets["database"]
        + ";UID="
        + st.secrets["username"]
        + ";PWD="
        + st.secrets["password"]
    )

conn = init_connection()
# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    data = pd.read_sql(query, conn)
    return data

img_cube = Image.open('Images\Cube.png')
st.image(img_cube, caption='Chinook Cube', output_format='PNG')
col1, col2, col3 = st.columns(3)

with col1: 
    img_cube = Image.open('Images\FactGenre_Cube.png')
    st.image(img_cube, caption='Fact Genre Cube', use_column_width='auto')
with col2: 
    img_cube = Image.open('Images\FactListen_Cube.png')
    st.image(img_cube, caption='Fact Listen Cube', use_column_width='auto')
with col3: 
    img_cube = Image.open('Images\FactSales_Cube.png')
    st.image(img_cube, caption='Fact Sales Cube', use_column_width='auto')

st.subheader('Fact Tables')

st.write("Fact Sales Table")
sql = "select * from star.FactSales;"
df_factSales = run_query(sql)
st.dataframe(df_factSales)

st.write("Fact Listen Table")
sql = "select * from star.FactListen;"
df_factListen = run_query(sql)
st.dataframe(df_factListen)

st.write("Fact Genre Table")
sql = "select * from star.FactGenre;"
df_factGenre = run_query(sql)
st.dataframe(df_factGenre)

st.subheader('Dimensions Tables')

st.write("Customer Dimension Table")
sql = "select * from star.DimCustomer;"
df_DimCustomer = run_query(sql)
st.dataframe(df_DimCustomer)

st.write("Employee Dimension Table")
sql = "select * from star.DimEmployee;"
df_DimEmployee = run_query(sql)
st.dataframe(df_DimEmployee)

st.write("Track Dimension Table")
sql = "select * from star.DimTrack;"
df_DimTrack = run_query(sql)
st.dataframe(df_DimTrack)

st.write("Date Dimension Table")
sql = "select * from star.DimDate;"
df_DimDate = run_query(sql)
st.dataframe(df_DimDate)

st.write("Genre Dimension Table")
sql = "select * from star.DimGenre;"
df_DimGenre = run_query(sql)
st.dataframe(df_DimGenre)

st.write("Album Dimension Table")
sql = "select * from star.DimAlbum;"
df_DimAlbum = run_query(sql)
st.dataframe(df_DimAlbum)