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


def select_columns(df):
    st.write("### Select Columns")
    all_columns = df.columns.tolist()
    #options_key = "_".join(all_columns)
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


def show_missing_values_percentage(df):
    st.write("### Missing Values Percentage")
    
    # Calculate the percentage of missing values for each column
    missing_percentage = df.isnull().sum() / len(df) * 100
    
    # Create a DataFrame to store the missing values percentage
    missing_df = pd.DataFrame({'Column': missing_percentage.index, 'Missing Percentage': missing_percentage.values})
    
    # Display the missing values percentage DataFrame
    st.write("Percentage of missing values",missing_df)


#aggregation funtion
def agg(df):
    # Allow the user to select columns for aggregation
    aggregation_columns = st.multiselect("Select columns for aggregation", options=df.columns)
    
    # Allow the user to select an aggregation function
    aggregation_function = st.selectbox("Select an aggregation function", options=["Sum", "Mean", "Median"])
    
    # Perform the aggregation
    if aggregation_columns:
        if aggregation_function == "Sum":
            aggregated_values = sub_df[aggregation_columns].sum()
        elif aggregation_function == "Mean":
            aggregated_values = sub_df[aggregation_columns].mean()
        elif aggregation_function == "Median":
            aggregated_values = sub_df[aggregation_columns].median()
        
        # Display the aggregated values
        st.write(f"Aggregated {aggregation_function} for {aggregation_columns}")
        st.write(aggregated_values)    

#remove duplicats
def remove_duplicates(df):
    st.write("### Remove Duplicates")
    
    # Select columns for identifying duplicates
    columns = st.multiselect("Select columns for identifying duplicates", options=df.columns)
    
    if columns:
        # Remove duplicates based on selected columns
        df.drop_duplicates(subset=columns, inplace=True)
        
        st.write("Duplicates removed successfully!")
        
    return df
#search and replace a value in column
def search_and_replace(df):
    st.write("### Search and Replace")
    
    # Select a column to search and replace
    column = st.selectbox("Select a column", options=df.columns)
    
    if column:
        # Get the search string from the user
        search_string = st.text_input("Enter the search string")
        
        # Get the replace value from the user
        replace_value = st.text_input("Enter the replace value")
        
        # Perform the search and replace operation
        if search_string in df[column].values:
            df[column] = df[column].replace(search_string, replace_value)
            st.write("Search and replace completed!")
            st.write(df[column])

        else:
            st.warning("The search string is not present in the selected column.")
        

#Change columns datatypes 
import streamlit as st
import pandas as pd

def change_column_data_types(df):
    st.write("### Change Column Data Types")
    
    # Select columns to change data types
    all_columns = df.columns.tolist()
    selected_columns = st.multiselect("Select columns to change data types", options=all_columns)
    
    # Get the new data types from the user
    new_data_types = {}
    for column in selected_columns:
        st.write(f"Column: {column}")
        current_data_type = df[column].dtype
        st.write(f"Current Data Type: {current_data_type}")
        new_data_type = st.selectbox("Select new data type", options=['object', 'int', 'float', 'datetime', 'boolean'])
        new_data_types[column] = new_data_type
    
    # Create a copy of the DataFrame to modify
    modified_df = df.copy()
    
    # Change the data types of selected columns
    for column, data_type in new_data_types.items():
        try:
            if data_type == 'object':
                modified_df[column] = modified_df[column].astype(str)
            elif data_type == 'int':
                modified_df[column] = pd.to_numeric(modified_df[column], errors='coerce', downcast='integer')
            elif data_type == 'float':
                modified_df[column] = pd.to_numeric(modified_df[column], errors='coerce', downcast='float')
            elif data_type == 'datetime':
                modified_df[column] = pd.to_datetime(modified_df[column], errors='coerce')
            elif data_type == 'boolean':
                modified_df[column] = modified_df[column].astype(bool)
            
            st.write(f"Column '{column}' data type changed to '{data_type}' successfully!")
        except Exception as e:
            st.error(f"Error occurred while changing data type of column '{column}': {str(e)}")
    
    return modified_df
def groupby_aggregate_data(sub_df):
    st.write("### Grouping and Aggregating Data")
    st.write(sub_df.head())
    
    # Get the list of columns from the DataFrame
    columns = sub_df.columns.tolist()

    # Get the categorical columns for grouping
    group_columns = st.multiselect("Select categorical columns for grouping", columns)

    # Get the numerical columns for aggregation
    numerical_columns = st.multiselect("Select numerical columns for aggregation", columns)

    # Get the aggregation functions from the user
    #aggregation_functions = st.multiselect("Select aggregation functions", ['sum', 'mean', 'median', 'min', 'max'])
    
    # Create the aggregation dictionary
    #aggregation = {col: func for col in numerical_columns for func in aggregation_functions}

    # Perform grouping and aggregation
    if group_columns and numerical_columns:
        grouped_dff = sub_df.groupby(group_columns)[numerical_columns].agg(['sum', 'mean', 'median', 'min', 'max'])
        grouped_df = grouped_dff.reset_index()  # Reset index to display category names
       
        st.write("### Grouped and Aggregated Data")
        st.write(grouped_df)
        #fig = px.bar(grouped_df, x=grouped_df.index, y=['sum'], barmode='group')
    else:
        st.warning("Please select at least one categorical column, one numerical column, and one aggregation function.")
  
       
def analyze_data(data):

    container = st.container()
    col1,col2 = st.columns(2)
    
    with container:
         st.write("File Header",data.head())
    with col1:
         st.write("Columns in you file are ",data.columns)
    st.write("### Select Columns to make your Data Set for Analysis")
    
    with col2:
        st.write("Data Types " ,data.dtypes)

        all_columns = [str(col) for col in data.columns]
        options_key = "_".join(all_columns)
        selected_columns = st.multiselect("Select columns", options=all_columns)    
    if selected_columns:
        sub_df = data[selected_columns]
        sub_df = select_and_rename_column(sub_df)
        st.write("### Sub DataFrame")
        st.write(sub_df.head())

        remove_duplicates(sub_df)
        
        change_column_type_df = change_column_data_types(sub_df)
        st.write("Columns Types are changed",change_column_type_df)
        st.write("Description")
        st.write(change_column_type_df.describe().T)
        st.write("Data Rank")
        st.write(change_column_type_df.rank())

        st.subheader("Sort Data")
        sort_column = st.selectbox("Select column for sorting", change_column_type_df.columns)
        sorted_df = change_column_type_df.sort_values(by=sort_column)
        st.write(sorted_df)

        #show_missing_values_percentage(sub_df)

        st.write(corr(change_column_type_df))
        
        show_missing_values(change_column_type_df)
        show_percent_missing(change_column_type_df)
        show_unique_values(change_column_type_df)
        show_standard_deviation(change_column_type_df)
        show_data_shape(change_column_type_df)
        show_data_correlation(change_column_type_df)
        filter_rows(change_column_type_df)
    
        groupby_aggregate_data(sub_df)
    
        

        search_and_replace(sub_df)



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


def show_missing_values(data):
    #col1 = st.beta_column()
    st.write("Missing Values")
    st.write(data.isnull().sum())

def show_percent_missing(data):
    st.write("Missing Percentage")
    st.write(data.isna().mean().mul(100))



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

def corr(data):
    st.write("Data correlation")
    st.write(data.corr(numeric_only=True).style.background_gradient(cmap='RdBu', vmin=-1, vmax=1))  


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

    elif options == 'Data visualization':
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