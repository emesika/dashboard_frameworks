import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/styles.css'])

data = pd.read_csv('data.csv')

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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            html.Img(src='/assets/logo.png', style={'width': '100px'}),
            html.H2("Navigation"),
            dbc.Nav([
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Employee Data", href="/employee-data", active="exact"),
                dbc.NavLink("Statistics", href="/statistics", active="exact"),
                dbc.NavLink("Department Tree View", href="/department-tree-view", active="exact"),
                dbc.NavLink("Interactive Map", href="/interactive-map", active="exact"),
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
        html.P("Welcome to the Dash Dashboard Example! Use the sidebar to navigate through different sections of the dashboard.")
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

def show_department_tree_view():
    department_tree = []
    for dept in data['Department'].unique():
        employees = data[data['Department'] == dept]['Name'].sort_values().tolist()
        department_tree.append({
            'label': dept,
            'value': dept,
            'children': [{'label': emp, 'value': f'{dept}_{emp}'} for emp in employees]
        })

    return html.Div([
        html.H1("Department Tree View"),
        dcc.Checklist(
            id='department-tree-view',
            options=[{'label': d['label'], 'value': d['value']} for d in department_tree],
            value=[]
        ),
        html.Div(id='tree-selected-nodes')
    ])

@app.callback(
    Output('tree-selected-nodes', 'children'),
    [Input('department-tree-view', 'value')]
)
def update_tree_selected_nodes(selected_nodes):
    return html.Div([html.P(f'Selected: {node}') for node in selected_nodes])

def show_interactive_map():
    return html.Div([
        html.H1("Interactive Map"),
        html.P("This page displays an interactive map with employee locations."),
        dcc.Dropdown(
            id='employee-dropdown',
            options=[{'label': f"{row['Name']} ({row['City']})", 'value': index} for index, row in data.iterrows()],
            placeholder='Select an Employee'
        ),
        dcc.Graph(id='employee-map')
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
                zoom=10
            )
        )

    return fig

# Ensure the correct URL path is updated
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.Row([
        dbc.Col([
            html.Img(src='/assets/logo.png', style={'width': '100px'}),
            html.H2("Navigation"),
            dbc.Nav([
                dbc.NavLink("Overview", href="/", active="exact"),
                dbc.NavLink("Employee Data", href="/employee-data", active="exact"),
                dbc.NavLink("Statistics", href="/statistics", active="exact"),
                dbc.NavLink("Department Tree View", href="/department-tree-view", active="exact"),
                dbc.NavLink("Interactive Map", href="/interactive-map", active="exact"),
            ], vertical=True, pills=True, style={'margin-top': '20px'})
        ], width=2, style={'background-color': '#161b22', 'min-width': '200px'}),
        dbc.Col(id='page-content', width=10)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
