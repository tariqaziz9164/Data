import pandas as pd
import streamlit as st
import plotly_express as px
#from PIL import Image



def colsType(df):
    st.header("Columns Data Types")
    st.dataframe(df.dtypes)

def missing(df):
    st.header("Missing Values in Your Data Set")
    st.dataframe(df.isnull().sum())

def columnsNames(df):
    st.header("Columns in your Data Set")
    st.dataframe(df.columns)

def statistics(df):
    st.header('Data Statistics')
    st.dataframe(df.describe())



def plot_data(df):
    st.header('Customize your plots from sidebar')

    st.sidebar.title("Plot options")

    x_col = st.sidebar.selectbox("Select X axis column", df.columns)

    y_col = st.sidebar.selectbox("Select Y axis column", df.columns)

    chart_type = st.sidebar.selectbox("Select chart type", ["scatter", "bar", "line"])

    

    if chart_type == 'scatter':
        st.plotly_chart(px.scatter(df, x=x_col, y=y_col))

    elif chart_type == 'bar':
        st.plotly_chart(px.bar(df, x=x_col, y=y_col))

    elif chart_type == 'line':
        st.plotly_chart(px.line(df, x=x_col, y=y_col))
    
    
    
def main():
    
    #col1, col2 = st.columns(2)
    
    
    st.image('./pandasFuny.jpg', caption='Data is Fun', width=100, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
    st.title("Financial Dashboard")

    st.sidebar.header("Upload your Data File")

    uploaded_file = st.sidebar.file_uploader("upload File")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

    else:
        st.error("Please upload a file")
        return


    st.header("Head Lines of Uploaded File")
    st.dataframe(df.head())
    options = st.sidebar.radio('Pages',options=['Data Statistic','Columns','Columns Types','Missing Values','Plots'])
    if options == "Data Statistic":
        statistics(df)
    
    elif options == "Plots":
        plot_data(df)

    elif options == "Columns":
        columnsNames(df)

    elif options == "Missing Values":
        missing(df) 


    elif options == "Columns Types":
        colsType(df)           
   
    
    
    

   
    
if __name__ == "__main__":
    main()
    

    

    





