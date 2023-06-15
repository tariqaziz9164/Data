import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import requests
container = st.container()
col1,col2 = st.columns(2)



@st.cache_resource
def load_data(file):
    """
    Load data from a file (CSV or Excel).

    Parameters:
        file (File): The file to load.

    Returns:
        DataFrame: The loaded data.
    """
    file_extension = file.name.split(".")[-1]
    if file_extension == "csv":
        data = pd.read_csv(file)
    elif file_extension in ["xls", "xlsx"]:
        data = pd.read_excel(file)
    else:
        st.warning("Unsupported file format. Please upload a CSV or Excel file.")
        return None
    return data






def group_data(data, aggregation):
    def select_group_column(df):
        group_columns = st.sidebar.multiselect("Select columns for grouping", df.columns, key="group_cols")
        return group_columns

    def perform_grouping(df, group_column, aggregation):
        if not group_column:
            raise ValueError("Please select at least one column for grouping.")

        if aggregation in ["sum", "mean", "median", "min", "max", "count"]:
            try:
                numeric_df = pd.to_numeric(df[group_column], errors="coerce")
                if numeric_df.isnull().any():
                    raise ValueError("Non-numeric values found in the selected column. Unable to perform aggregation.")
                if numeric_df.dtype == "object":
                    raise ValueError("Selected column is of type 'object'. Unable to perform aggregation.")
                grouped_df = df.groupby(numeric_df).agg(aggregation)
            except TypeError:
                raise ValueError("Non-numeric values found in the selected column. Unable to perform aggregation.")
            except ValueError:
                raise ValueError(f"Error in column '{group_column}': {df[group_column]}")
        else:
            raise ValueError("Unsupported aggregation function. Please choose a valid statistical method.")

        return grouped_df

    def apply_additional_aggregation(grouped_df, df, aggregation):
        if aggregation in ["sum", "mean", "median", "min", "max"]:
            group_column = st.sidebar.selectbox(f"Select column for {aggregation}", df.columns, key=aggregation)
            if aggregation == "sum":
                grouped_df = grouped_df.groupby(group_column).sum()
            elif aggregation == "mean":
                grouped_df = grouped_df.groupby(group_column).mean()
            elif aggregation == "median":
                grouped_df = grouped_df.groupby(group_column).median()
            elif aggregation == "min":
                grouped_df = grouped_df.groupby(group_column).min()
            elif aggregation == "max":
                grouped_df = grouped_df.groupby(group_column).max()
        elif aggregation == "count":
            group_column = st.sidebar.selectbox("Select column for count", df.columns, key="count")
            grouped_df = grouped_df.groupby(group_column).size().reset_index(name='count')
        else:
            st.warning("Unsupported aggregation function. Please choose a valid statistical method.")
            return df

        return grouped_df

    group_column = select_group_column(data)
    grouped_df = perform_grouping(data, group_column, aggregation)
    final_grouped_df = apply_additional_aggregation(grouped_df, data, aggregation)
    return final_grouped_df


def select_columns(df):
    st.write("### Select Columns")
    all_columns = df.columns.tolist()
    options_key = "_".join(all_columns)
    selected_columns = st.multiselect("Select columns", options=all_columns)
    
    if selected_columns:
        sub_df = df[selected_columns]
        st.write("### Sub DataFrame")
        st.write(sub_df.head())
    else:
        st.warning("Please select at least one column.")

def select_and_rename_column(df):
    st.write("### Select and Rename Columns")
    
    # Select columns to rename
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to rename", options=all_columns)
    
    # Rename the selected columns
    for column in selected_columns:
        new_column_name = st.text_input(f"Enter new name for column '{column}'", value=column)
        if column != new_column_name:
            df.rename(columns={column: new_column_name}, inplace=True)
            st.write(f"Column '{column}' renamed as '{new_column_name}' successfully!")
    
    return df    

  
       
def analyze_data(data):
    
    show_file_header(data)
    st.write("Columns in you file are ",data.columns)
    st.write("### Select Columns to make your Data Set for Analysis")
    all_columns = data.columns.tolist()
    options_key = "_".join(all_columns)
    selected_columns = st.multiselect("Select columns", options=all_columns)
    
    if selected_columns:
        sub_df = data[selected_columns]
        sub_df = select_and_rename_column(sub_df)
        st.write("### Sub DataFrame")
        st.write(sub_df.head())

        st.write("Description")
        st.write(sub_df.describe())
        st.write("Data Rank")
        st.write(sub_df.rank())

        st.sidebar.header("Data Sorted")
        sort_column = st.selectbox("Select column for sorting", sub_df.columns)
        sorted_df = sub_df.sort_values(by=sort_column)
        st.write(sorted_df)

        show_columns_info(sub_df)
        show_missing_values(sub_df)
        show_unique_values(sub_df)
        show_standard_deviation(sub_df)
        show_data_shape(sub_df)
        show_data_correlation(sub_df)
        filter_rows(sub_df)



    else:
        st.warning("Please select at least one column.")


    



def show_file_header(data):
    st.write("File Header")
    st.write(data.head())

def sort_data(data):
    # Sort the data by a selected column
    sort_column = st.selectbox("Select column to sort by", data.columns)
    sorted_df = data.sort_values(by=sort_column)
    return sorted_df


def show_sorted_data(sorted_df):
    st.write("Sort Data")
    st.write(sorted_df)

# Define select_group_column, perform_grouping, and apply_additional_aggregation functions here


def show_columns_info(data):
    #col1, col2 = st.columns(2)
    st.write("Columns Names")
    st.write(data.columns)
    st.write("Columns Data Types")
    st.write(data.dtypes)


def show_missing_values(data):
    #col1 = st.beta_column()
    st.write("Missing Values")
    st.write(data.isnull().sum())


def show_unique_values(data):
    #col2 = st.beta_column()
    st.write("Unique Values")
    st.write(data.nunique())


def show_standard_deviation(data):
    #col1 = st.beta_column()
    st.write("Standard Deviation")
    st.write(data.std(numeric_only=True))


def show_data_shape(data):
    #col1, col2 = st.beta_columns(2)
    st.write("Number of rows")
    st.write(data.shape[0])
    st.write("Number of columns")
    st.write(data.shape[1])


def show_data_correlation(data):
    #col1 = st.beta_column()
    st.write("Data Correlation")
    st.write(data.corr(numeric_only=True))


def filter_rows(data):
    
    column_name = st.selectbox("Select a column to filter", data.columns)
    value = st.text_input("Enter the filter value")
    # Filter the rows based on the converted column
    if value == "":
        filtered_data = data[data[column_name].isnull()]
    elif data[column_name].dtype == 'float':
          filtered_data = data[data[column_name] >= float(value)]
    else:      
        filtered_data = data[data[column_name].astype(str).str.contains(value, case=False)]
    st.write("Filtered Data")
    st.write(filtered_data)    


def create_chart(chart_type, data, x_column, y_column):

    container.write(" # Data Visualization # ")
    if chart_type == "Bar":
    
        st.header("Bar Chart")
        
        color_column = st.sidebar.selectbox("Select column for color ", data.columns,key="color_name")
        #pattern_column = st.sidebar.selectbox("Select column for pattern ", data.columns)
        if color_column:
           fig = px.bar(data, x=x_column, y=y_column,color=color_column,barmode="group")
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
            
           fig = px.scatter(data, x=x_column, y=y_column,color=color_column,size=size_column)

        else:
            fig = px.scatter(data, x=x_column, y=y_column) 
        st.plotly_chart(fig)        

    elif chart_type == "Histogram":
        st.header("Histogram Chart")
        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
        fig = px.histogram(data, x=x_column, y=y_column,color = color_column)
        st.plotly_chart(fig)
        

    elif chart_type == "Pie":
        st.header("Pie Chart")

        color_column = st.sidebar.selectbox("Select column for color ", data.columns)
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
            st.warning("No file or empty file")

    if options == 'Data visualization':
        if data is not None:
            # Create a sidebar for user options
            st.sidebar.title("Chart Options")


            st.write("### Select Columns")
            all_columns = data.columns.tolist()
            options_key = "_".join(all_columns)
            selected_columns = st.sidebar.multiselect("Select columns", options=all_columns)
            if selected_columns:
                sub_df = data[selected_columns]


                chart_type = st.sidebar.selectbox("Select a chart type", ["Bar", "Line", "Scatter", "Histogram", "Pie"])

                x_column = st.sidebar.selectbox("Select the X column", sub_df.columns)

                y_column = st.sidebar.selectbox("Select the Y column", sub_df.columns)

                create_chart(chart_type, sub_df, x_column, y_column)

    
       

if __name__ == "__main__":
    main()