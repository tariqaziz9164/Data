import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
container = st.container()
col1,col2 = st.columns(2)



@st.cache_resource
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
    df[group_column] = pd.to_numeric(df[group_column], errors='coerce')
    grouped_df_mean = df.groupby(group_column).mean()
    return grouped_df_mean   
    

    

  
       
def analyze_data(data):
    # Perform basic data analysis
    container.write(" # Data Analysis # ")
    container.write("File Header")
    container.write(data.head())
    container.write("Description")
    container.write(data.describe())
    #container.write("Data Corelation")
    #container.write(data.corr())
    container.write("Data Rank")
    container.write(data.rank())

    sorted_df = sort_data(data)

    container.write("Sort Data")
    container.write(sorted_df)

    groupBySum = group_by(data)

    container.write("Group by sum")
    container.write(groupBySum)

    groupByMean = group_by_mean(data)

    container.write("Group by mean")
    container.write(groupByMean)  
    
       
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
       
       
    
    with col1:
       st.write("Number of rows: ", data.shape[0])

       
    with col1:   
       st.write("Number of columns: ", data.shape[1])

    



def create_chart(chart_type, data, x_column, y_column):

    container.write(" # Data Visualization # ")
    if chart_type == "Bar":
    
        st.header("Bar Chart")
        
        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
        pattern_column = st.sidebar.selectbox("Select column for pattern ", data.columns)
        if color_column:
           fig = px.bar(data, x=x_column, y=y_column,color=color_column,pattern_shape=pattern_column,barmode="group")
           st.plotly_chart(fig)
        else:
           fig = px.bar(data, x=x_column, y=y_column,barmode="group")
           st.plotly_chart(fig)   

    elif chart_type == "Line":
        st.header("Line Chart")
        fig = px.line(data, x=x_column, y=y_column)
        st.plotly_chart(fig)

    elif chart_type == "Scatter":
        st.header("Scatter Chart")
        size_column = st.sidebar.selectbox("Select column for size ", data.columns)
        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
        if color_column:
           #if data[size_column].dtype in [int, float] and data[color_column].dtype in str: 
           fig = px.scatter(data, x=x_column, y=y_column,color=color_column,size=size_column)
              #st.plotly_chart(fig)
           #else:   
           #   st.warning("Selected columns must contain numeric data for color and size encoding.")
           #   fig = px.scatter(data, x=x_column, y=y_column)
        else:
            fig = px.scatter(data, x=x_column, y=y_column) 
        st.plotly_chart(fig)        

    elif chart_type == "Histogram":
        st.header("Histogram Chart")
        color_column = st.sidebar.selectbox("Select column for size ", data.columns)
        fig = px.histogram(data, x=x_column, y=y_column,color = color_column,log_x = False,log_y = False)
        st.plotly_chart(fig)
        

    elif chart_type == "Pie":
        st.header("Pie Chart")

        color_column = next((col for col in data.columns if data[col].dtype == "object"), None)
        if color_column:
            fig = px.pie(data, names=x_column, values=y_column, color=color_column)
            st.plotly_chart(fig)
        else:
            fig = px.pie(data, names=x_column, values=y_column)
            st.plotly_chart(fig)
    
    

def main():

    
    image = Image.open("pandasFuny.jpg")
    container.image(image, width=200)
    container.write(" # Data Analysis and Visualization # ")
    container.write("Please Upload a CSV file from sidebar or enter an online dataset")
    st.sidebar.image(image, width=50)
    file_option = st.sidebar.radio("Data Source", options=["Upload Local File", "Enter Online Dataset"])
    file = None
    data = None

    if file_option == "Upload Local File":
        file = st.sidebar.file_uploader("Upload a data set in CSV or EXCEL format", type=["csv", "excel"])

    elif file_option == "Enter Online Dataset":
        online_dataset = st.sidebar.text_input("Enter the URL of the online dataset")
        if online_dataset:
            try:
                response = requests.get(online_dataset)
                if response.ok:
                    data = pd.read_csv(online_dataset)
                else:
                    st.warning("Unable to fetch the dataset from the provided link.")
            except:
                st.warning("Invalid URL or unable to read the dataset from the provided link.")

    options = st.sidebar.radio('Pages', options=['Data Analysis', 'Data visualization'])

    if file is not None:
        data = load_data(file)

    if options == 'Data Analysis':
        if data is not None:
            analyze_data(data)
        else:
            st.warning("Please upload a file or enter an online dataset.")

    if options == 'Data visualization':
        if data is not None:
            # Create a sidebar for user options
            st.sidebar.title("Chart Options")

            chart_type = st.sidebar.selectbox("Select a chart type", ["Bar", "Line", "Scatter", "Histogram", "Pie"])

            x_column = st.sidebar.selectbox("Select the X column", data.columns)

            y_column = st.sidebar.selectbox("Select the Y column", data.columns)

            create_chart(chart_type, data, x_column, y_column)
        else:
            st.warning("Please upload a file or enter an online dataset.")
        
if __name__ == "__main__":
    main()