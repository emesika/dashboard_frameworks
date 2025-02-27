import os
import dash
from dash import dcc, html, Input, Output, State, dash_table, MATCH
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Define the base directory
base_dir = os.path.abspath(os.path.dirname(__file__))
assets_dir = os.path.join(base_dir, '..', 'assets')

# Update paths to be relative to the script's directory
external_stylesheets = [dbc.themes.BOOTSTRAP, '/assets/styles.css']
data_path = os.path.join(base_dir, '..', 'data.csv')
logo_path = '/assets/logo.png'

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, assets_folder=assets_dir)
app.config.suppress_callback_exceptions = True  # Add this line

data = pd.read_csv(data_path)

header_colors = {
    'Name': '#333333',
    'Age': '#FFDD44',
    'Department': '#FF6F61',
    'Salary': '#6B5B95',
    'City': '#88B04B',
    'lat': '#009879',
    'lon': '#ff6347',
    'Age Interval': '#4682b4'
}

def generate_table(dataframe):
    return dash_table.DataTable(
        columns=[
            {'name': col, 'id': col, 'type': 'text', 'presentation': 'markdown'} 
            for col in dataframe.columns
        ],
        data=dataframe.to_dict('records'),
        style_header_conditional=[
            {
                'if': {'column_id': col},
                'backgroundColor': header_colors.get(col, '#333'),
                'color': 'white',
                'fontWeight': 'bold'
            } for col in dataframe.columns
        ],
        style_data={
            'color': 'black',
            'backgroundColor': 'white'
        },
        filter_action='native',
        sort_action='native'
    )

def build_tree(data):
    tree = []
    departments = data['Department'].unique()
    for dept in departments:
        employees = data[data['Department'] == dept]['Name'].sort_values().tolist()
        tree.append({
            'department': dept,
            'employees': [{'name': emp} for emp in employees]
        })
    return tree

department_tree = build_tree(data)

def show_department_tree_view():
    departments = data['Department'].unique()
    tree_layout = []

    for dept in departments:
        dept_data = data[data['Department'] == dept].sort_values(by='Name')
        children_layout = []
        for _, emp in dept_data.iterrows():
            emp_id = f"emp-{emp['Name'].replace(' ', '-')}"
            emp_details = html.Div([
                html.P(f"Age: {emp['Age']}"),
                html.P(f"City: {emp['City']}")
            ], style={'padding-left': '40px', 'display': 'none'}, id={'type': 'emp-details', 'index': emp_id})

            emp_button = dbc.Button(emp['Name'], color="secondary", size="sm",
                                    style={'margin': '2px', 'width': '200px', 'margin-left': '20px'},  # Adjusted width and added indentation
                                    id={'type': "emp-button", 'index': emp_id})
            children_layout.extend([emp_button, emp_details])

        dept_button = dbc.Button(
            f"Department: {dept}", color="primary",
            id={'type': "dept-button", 'index': dept},
            className="mb-1",
            style={'width': '250px'}
        )
        dept_collapse = dbc.Collapse(
            children_layout, id={'type': 'dept-collapse', 'index': dept}, is_open=False,
            style={'margin-left': '20px'}  # Added indentation
        )

        tree_layout.extend([dept_button, dept_collapse])

    return html.Div([
        html.H1("Department Tree View"),
        html.Div(tree_layout)
    ])

@app.callback(
    Output({'type': 'dept-collapse', 'index': MATCH}, 'is_open'),
    [Input({'type': 'dept-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'dept-collapse', 'index': MATCH}, 'is_open')]
)
def toggle_department_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

@app.callback(
    Output({'type': 'emp-details', 'index': MATCH}, 'style'),
    [Input({'type': 'emp-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'emp-details', 'index': MATCH}, 'style')]
)
def toggle_employee_details(n_clicks, style):
    if n_clicks:
        return {'display': 'block' if style['display'] == 'none' else 'none'}
    return style

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            html.Img(src=logo_path, style={'width': '100px'}),
            html.H2("Navigation"),
            dbc.Nav([
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Employee Data", href="/employee-data", active="exact"),
                dbc.NavLink("Statistics", href="/statistics", active="exact"),
                dbc.NavLink("Department Tree View", href="/department-tree-view", active="exact"),
                dbc.NavLink("Interactive Map", href="/interactive-map", active="exact"),
                html.Br(),
                html.Hr(),
                html.H3("External Links"),
                dbc.NavLink("Streamlit Documentation", href="https://streamlit.io", external_link=True),
                dbc.NavLink("Dash Documentation", href="https://dash.plotly.com", external_link=True),
                dbc.NavLink("React Documentation", href="https://reactjs.org", external_link=True),
                html.Br(),
                dbc.Button("Download Reports", id="download-reports-button", className="btn"),
                html.Div(id='download-reports-output')
            ], vertical=True, pills=True, style={'margin-top': '20px'})
        ], width=2, style={'background-color': '#161b22'}),
        dbc.Col(id='page-content', width=10)
    ])
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return show_overview()
    elif pathname == '/employee-data':
        return show_employee_data()
    elif pathname == '/statistics':
        return show_statistics()
    elif pathname == '/department-tree-view':
        return show_department_tree_view()
    elif pathname == '/interactive-map':
        return show_interactive_map()
    else:
        return "404 Page Not Found"

def show_overview():
    return html.Div([
        html.H1("Overview"),
        html.P("Welcome to the Dash Dashboard Example!"),
        html.P("Use the sidebar to navigate through different sections of the dashboard."),
        html.Hr(),  # Adds a horizontal line
        html.P("© 2024 Redhat Dashboard Example")
    ])

def show_employee_data():
    departments = data['Department'].unique()
    return html.Div([
        html.H1("Employee Data"),
        dcc.Dropdown(
            id='department-dropdown',
            options=[{'label': dept, 'value': dept} for dept in departments],
            value=departments[0],
            style={'width': '50%'}
        ),
        html.Div(id='filtered-employee-data')
    ])

@app.callback(
    Output('filtered-employee-data', 'children'),
    [Input('department-dropdown', 'value')]
)
def update_filtered_employee_data(selected_department):
    filtered_data = data[data['Department'] == selected_department].sort_values(by='Name')
    return html.Div([
        generate_table(filtered_data),
        dcc.Input(id='search-name', type='text', placeholder='Search by Name', debounce=True),
        html.Div(id='search-results'),
        dbc.Checkbox(id='show-raw-data', label='Show Raw Data', value=True),
        html.Div(id='raw-data')
    ])

@app.callback(
    Output('search-results', 'children'),
    [Input('search-name', 'value')]
)
def update_search_results(search_term):
    if search_term:
        search_results = data[data['Name'].str.contains(search_term, case=False)].sort_values(by='Name')
        return generate_table(search_results)
    return ""

@app.callback(
    Output('raw-data', 'children'),
    [Input('show-raw-data', 'value')]
)
def update_raw_data(show_raw):
    if show_raw:
        raw_data_sorted = data.sort_values(by='Name')
        return generate_table(raw_data_sorted)
    return ""

def show_statistics():
    return html.Div([
        html.H1("Statistics"),
        html.H3("Salary Distribution"),
        dcc.Graph(id='salary-distribution-2d'),
        html.H3("3D Salary Distribution"),
        dcc.Graph(id='salary-distribution-3d'),
        html.H3("Salary by Age Intervals Cross Departments"),
        dcc.Graph(id='salary-age-intervals'),
        html.H3("Summary Statistics"),
        html.Div(id='summary-statistics-table'),
        dcc.RadioItems(
            id='summary-statistic-radio',
            options=[
                {'label': 'Mean', 'value': 'mean'},
                {'label': 'Median', 'value': 'median'},
                {'label': 'Sum', 'value': 'sum'}
            ],
            value='mean'
        ),
        html.Div(id='selected-summary-statistic')
    ])

@app.callback(
    Output('salary-distribution-2d', 'figure'),
    [Input('url', 'pathname')]
)
def update_salary_distribution_2d(_):
    fig = px.bar(data, x='Department', y='Salary', color='Department')
    return fig

@app.callback(
    Output('salary-distribution-3d', 'figure'),
    [Input('url', 'pathname')]
)
def update_salary_distribution_3d(_):
    fig = px.scatter_3d(data, x='Department', y='Salary', z='Age', color='Department')
    return fig

@app.callback(
    Output('salary-age-intervals', 'figure'),
    [Input('url', 'pathname')]
)
def update_salary_age_intervals(_):
    bins = [20, 30, 40, 50, 60]
    labels = ["20-30", "30-40", "40-50", "50-60"]
    data['Age Interval'] = pd.cut(data['Age'], bins=bins, labels=labels, right=False)
    data['Age Interval'] = pd.Categorical(data['Age Interval'], categories=labels, ordered=True)
    data_sorted = data.sort_values('Age Interval')
    fig = px.box(data_sorted, x='Age Interval', y='Salary', color='Department')
    return fig

@app.callback(
    Output('summary-statistics-table', 'children'),
    [Input('url', 'pathname')]
)
def update_summary_statistics_table(_):
    summary_stats = data.groupby('Department')['Salary'].describe().reset_index()
    return generate_table(summary_stats)

@app.callback(
    Output('selected-summary-statistic', 'children'),
    [Input('summary-statistic-radio', 'value')]
)
def update_summary_statistic(stat):
    if stat == 'mean':
        summary_mean = data.groupby('Department')['Salary'].mean().reset_index().sort_values(by='Department')
        return generate_table(summary_mean)
    elif stat == 'median':
        summary_median = data.groupby('Department')['Salary'].median().reset_index().sort_values(by='Department')
        return generate_table(summary_median)
    elif stat == 'sum':
        summary_sum = data.groupby('Department')['Salary'].sum().reset_index().sort_values(by='Department')
        return generate_table(summary_sum)

@app.callback(
    [Output(f"dept-{node['department']}-collapse", "is_open") for node in department_tree],
    [Input(f"dept-{node['department']}-toggle", "n_clicks") for node in department_tree],
    [State(f"dept-{node['department']}-collapse", "is_open") for node in department_tree]
)
def toggle_collapse(*args):
    ctx = dash.callback_context
    if not ctx.triggered:
        return [False] * len(department_tree)
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    is_open_states = args[len(department_tree):]
    toggle_states = []
    for i, node in enumerate(department_tree):
        if button_id == f"dept-{node['department']}-toggle":
            toggle_states.append(not is_open_states[i])
        else:
            toggle_states.append(is_open_states[i])
    return toggle_states

def show_interactive_map():
    return html.Div([
        html.H1("Interactive Map"),
        html.P("This page displays an interactive map with employee locations."),
        dcc.Dropdown(
            id='employee-dropdown',
            options=[{'label': f"{row['Name']} ({row['City']})", 'value': index} for index, row in data.iterrows()],
            placeholder='Select an Employee'
        ),
        dcc.Graph(id='employee-map', style={'height': '750px'})  # Adjust the height as needed
    ])

@app.callback(
    Output('employee-map', 'figure'),
    [Input('employee-dropdown', 'value')]
)
def update_map(selected_index):
    fig = go.Figure(go.Scattermapbox(
        lat=data['lat'],
        lon=data['lon'],
        mode='markers',
        marker=go.scattermapbox.Marker(size=9),
        text=data.apply(lambda row: f"{row['Name']} ({row['City']})", axis=1)
    ))

    fig.update_layout(
        mapbox=dict(
            center=dict(
                lat=data['lat'].mean(),
                lon=data['lon'].mean()
            ),
            zoom=3,
            style="open-street-map"
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    if selected_index is not None:
        selected_row = data.iloc[selected_index]
        fig.add_trace(go.Scattermapbox(
            lat=[selected_row['lat']],
            lon=[selected_row['lon']],
            mode='markers+text',
            marker=dict(size=12, color='red'),
            text=["Selected Location"],
            textposition="top right"
        ))
        fig.update_layout(
            mapbox=dict(
                center=dict(
                    lat=selected_row['lat'],
                    lon=selected_row['lon']
                ),
                zoom=6
            )
        )

    return fig

@app.callback(
    Output('download-reports-output', 'children'),
    [Input('download-reports-button', 'n_clicks')]
)
def download_reports(n_clicks):
    if n_clicks:
        return html.Div("Reports were downloaded successfully!", style={'color': 'green'})
    return ""

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
   

