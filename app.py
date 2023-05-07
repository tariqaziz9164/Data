import streamlit as st
import pandas as pd
import plotly_express as px
from PIL import Image

container = st.container()
col1,col2 = st.columns(2)



@st.cache
def load_data(file):
    return pd.read_csv(file)



def sort_data(df):
    st.sidebar.header("Data Filtering")
    
    # Sort Data
    sort_column = st.sidebar.selectbox("Sort by", df.columns)
    df = df.sort_values(by=sort_column)
    return df

    
    
def group_by(df):
     # Group Data
    group_column = st.sidebar.selectbox("Group by Sum",df.columns)
    grouped_df = df.groupby(group_column).sum()
    return grouped_df

def group_by_mean(df):
     # Group Data
    group_column = st.sidebar.selectbox("Group by Mean",df.columns)
    grouped_df_mean = df.groupby(group_column).mean()
    return grouped_df_mean   
    

    

  
       
def analyze_data(data):
    # Perform basic data analysis
    container.write(" # Data Analysis # ")
    container.write("File Header")
    container.write(data.head())
    container.write("Description")
    container.write(data.describe())
    container.write("Data Corelation")
    container.write(data.corr())
    container.write("Data Rank")
    container.write(data.rank())
      
    
    st.empty()   
    with col1:
          
       st.write("Columns Names ", data.columns)
    with col1:
          
       st.write("Columns Data Types: ", data.dtypes)

    with col2:
       st.write("Missing Values: ", data.isnull().sum())
    
    
    with col2:
       st.write("Unique Values: ", data.nunique())
       
       
    with col2:   
       st.write("standerd deviation:", data.std())
       
       
    

    sorted_df = sort_data(data)
    
        
    container.write("Sort Data")
    container.write(sorted_df)
    
    with col1:
       st.write("Number of rows: ", data.shape[0])

       
    with col1:   
       st.write("Number of columns: ", data.shape[1])

    

    groupBySum = group_by(data)
        
    container.write("Group by sum")
    container.write(groupBySum)

    groupByMean = group_by_mean(data)
    container.write("Group by mean")
    container.write(groupByMean)

def create_chart(chart_type, data, x_column, y_column):

    container.write(" # Data Visualization # ")
    if chart_type == "Bar":
    
        st.header("Bar Chart")
        fig = px.bar(data, x=x_column, y=y_column)
        st.plotly_chart(fig)

    elif chart_type == "Line":
        st.header("Line Chart")
        fig = px.line(data, x=x_column, y=y_column)
        st.plotly_chart(fig)

    elif chart_type == "Scatter":
        st.header("Scatter Chart")
        fig = px.scatter(data, x=x_column, y=y_column)
        st.plotly_chart(fig)

    elif chart_type == "Histogram":
        st.header("Histogram Chart")

        fig = px.histogram(data, x=x_column, y=y_column,log_x = False,log_y = False)
        st.plotly_chart(fig)
        

    elif chart_type == "pie":
        st.header("Geo Chart")

        fig = px.pie(data,names = x_column,values = y_column)
        st.plotly_chart(fig)


    
    

def main():

    
    image = Image.open("pandasFuny.jpg")

    
    
    container.image(image,width = 100)
    container.write(" # Data Analysis and Visualization # ")
    
    st.sidebar.image(image,width = 50)
    file = st.sidebar.file_uploader("Upload a data set in CSV or EXCEL format", type=["csv","excel"])

    options = st.sidebar.radio('Pages',options = ['Data Analysis','Data visualization'])

    if file is not None:
        data = load_data(file)

        if options == 'Data Analysis':
           analyze_data(data)

        if options =='Data visualization':

            #Create a sidebar for user options
            st.sidebar.title("Chart Options")

            chart_type = st.sidebar.selectbox("Select a chart type", ["Bar", "Line", "Scatter", "Histogram","pie"])

            x_column = st.sidebar.selectbox("Select the X column", data.columns)

            y_column = st.sidebar.selectbox("Select the Y column", data.columns)

            create_chart(chart_type, data, x_column, y_column)
        
if __name__ == "__main__":
    main()
    

    

    





