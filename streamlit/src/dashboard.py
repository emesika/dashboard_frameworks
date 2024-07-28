import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_tree_select import tree_select

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

# Load custom CSS for dark mode and other styles from a file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load sample data
@st.cache_data
def load_data():
    """
    Load data from CSV file and cache it for performance.
    """
    data = pd.read_csv('data.csv')
    return data


def render_html_table(dataframe):
    """
    Render a DataFrame as an HTML table with custom styling.
    """
    return dataframe.to_html(classes='custom-table', index=False, escape=False)

def show_overview():
    """
    Display the overview section of the dashboard.
    """
    st.title("Overview")
    st.write("Welcome to the Streamlit Dashboard Example!")
    st.write("Use the sidebar to navigate through different sections of the dashboard.")

def show_employee_data(data):
    """
    Display the employee data section of the dashboard.
    """
    st.title("Employee Data")

    # Dropdown for selecting department, narrower width
    departments = data['Department'].unique()
    selected_department = st.selectbox("Select Department", departments)

    # Filter data based on the selected department
    filtered_data = data[data['Department'] == selected_department].sort_values(by='Name')

    # Display a table with the filtered data
    st.subheader("Filtered Employee Data")
    st.markdown(render_html_table(filtered_data), unsafe_allow_html=True)

    # Search functionality for the table
    search_term = st.text_input("Search by Name")
    if search_term:
        search_results = data[data['Name'].str.contains(search_term, case=False)].sort_values(by='Name')
        st.markdown(render_html_table(search_results), unsafe_allow_html=True)

    # Checkbox for showing/hiding the raw data table, selected by default
    if st.checkbox("Show Raw Data", value=True):
        st.subheader("Raw Data")
        st.markdown(render_html_table(data.sort_values(by='Name')), unsafe_allow_html=True)

def show_statistics(data):
    """
    Display the statistics section of the dashboard.
    """
    st.title("Statistics")

    # Display a 2D graph
    st.subheader("Salary Distribution")
    fig_2d = px.bar(data, x='Department', y='Salary', color='Department', barmode='group', title='Salary Distribution by Department')
    st.plotly_chart(fig_2d, use_container_width=True)

    # Display a 3D graph
    st.subheader("3D Salary Distribution")
    fig_3d = px.scatter_3d(data, x='Department', y='Salary', z='Age', color='Department', title='3D Salary Distribution by Department and Age')
    st.plotly_chart(fig_3d, use_container_width=True)

    # Salary by Age Intervals Cross Departments
    st.subheader("Salary by Age Intervals (10 years) Cross Departments")
    bins = [20, 30, 40, 50, 60]
    labels = ["20-30", "30-40", "40-50", "50-60"]
    data['Age Interval'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)
    data['Age Interval'] = pd.Categorical(data['Age Interval'], categories=labels, ordered=True)
    data = data.sort_values('Age Interval')  # Ensure data is sorted by Age Interval
    fig_age_salary = px.box(data, x='Age Interval', y='Salary', color='Department', title='Salary by Age Intervals Cross Departments')
    st.plotly_chart(fig_age_salary, use_container_width=True)

    # Display a summary statistics table
    st.subheader("Summary Statistics")
    summary_stats = data.groupby('Department')['Salary'].describe().reset_index().sort_values(by='Department')
    st.markdown(render_html_table(summary_stats), unsafe_allow_html=True)

    # Radio buttons for selecting a summary statistic
    stat = st.radio("Summary Statistic", ('Mean', 'Median', 'Sum'))
    if stat == 'Mean':
        summary_mean = data.groupby('Department')['Salary'].mean().reset_index().sort_values(by='Department')
        st.markdown(render_html_table(summary_mean), unsafe_allow_html=True)
    elif stat == 'Median':
        summary_median = data.groupby('Department')['Salary'].median().reset_index().sort_values(by='Department')
        st.markdown(render_html_table(summary_median), unsafe_allow_html=True)
    else:
        summary_sum = data.groupby('Department')['Salary'].sum().reset_index().sort_values(by='Department')
        st.markdown(render_html_table(summary_sum), unsafe_allow_html=True)

def show_department_tree_view(data):
    """
    Display the department tree view section of the dashboard.
    """
    st.title("Department Tree View")

    # Create nodes to display
    nodes = []
    for dept in data['Department'].unique():
        children = [{"label": f"Employee: {row['Name']}", "value": f"{dept}_{row['Name']}_{index}"} for index, row in data[data['Department'] == dept].sort_values(by='Name').iterrows()]
        nodes.append({"label": f"Department: {dept}", "value": dept, "children": children})

    # Display tree select
    return_select = tree_select(nodes)
    st.write("Selected node(s):", return_select)

def show_interactive_map(data):
    """
    Display the interactive map page with employee locations.
    """
    st.title("Interactive Map")
    st.write("This page displays an interactive map with employee locations.")

    # Extract latitude and longitude data
    map_data = data[['lat', 'lon', 'City', 'Name', 'Department']]

    # Reorder columns for display and sort the data by employee name
    display_data = map_data[['Name', 'Department', 'City', 'lat', 'lon']].sort_values(by='Name')
    
    st.write("Employee Locations:")
    selected_employee = st.selectbox("Select an Employee", display_data['Name'].unique(), format_func=lambda x: f"{x} ({display_data.loc[display_data['Name'] == x, 'City'].values[0]})")

    # Process click on dataframe row
    if selected_employee:
        selected_row = display_data[display_data['Name'] == selected_employee].iloc[0]
        selected_lat = selected_row['lat']
        selected_lon = selected_row['lon']
        st.session_state['selected_lat'] = selected_lat
        st.session_state['selected_lon'] = selected_lon

    # Create Plotly figure
    fig = go.Figure(go.Scattermapbox(
        lat=map_data['lat'],
        lon=map_data['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        text=map_data.apply(lambda row: f"{row['Name']} ({row['City']})", axis=1)
    ))

    fig.update_layout(
        mapbox=dict(
            center=dict(
                lat=st.session_state.get('selected_lat', map_data['lat'].mean()),
                lon=st.session_state.get('selected_lon', map_data['lon'].mean())
            ),
            zoom=5,
            style="open-street-map"
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    # Highlight selected location
    if 'selected_lat' in st.session_state and 'selected_lon' in st.session_state:
        fig.add_trace(go.Scattermapbox(
            lat=[st.session_state['selected_lat']],
            lon=[st.session_state['selected_lon']],
            mode='markers+text',
            marker=dict(size=12, color='red'),
            text=["Selected Location"],
            textposition="top right"
        ))

    # Display map with Streamlit
    st.plotly_chart(fig, use_container_width=True)


# Main content based on sidebar selection
local_css("styles.css")
data = load_data()
st.sidebar.image("logo.png", width=100)
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Employee Data", "Statistics", "Department Tree View", "Interactive Map"])

if page == "Overview":
    show_overview()
elif page == "Employee Data":
    show_employee_data(data)
elif page == "Statistics":
    show_statistics(data)
elif page == "Department Tree View":
    show_department_tree_view(data)
elif page == "Interactive Map":
    show_interactive_map(data)

# Button for downloading a document (dummy action)
if st.button("Download Report"):
    st.write("Report downloaded!")

# Add some useful links
st.sidebar.markdown("[Streamlit Documentation](https://docs.streamlit.io)")
st.sidebar.markdown("[Plotly Documentation](https://plotly.com/python/)")

# Add a footer
st.markdown("***")
st.markdown("© 2024 Redhat Dashboard Example")

# Run this with `streamlit run dashboard.py`

