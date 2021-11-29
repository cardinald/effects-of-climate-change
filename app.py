# -------------------------------------------------------
# The Effects of Climate Change Interactive Application
# CMPT 450 Winter 2021
# Author: Desiree Cardinal
# April 9, 2021
# ------------------------------------------------------

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go


SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "17rem",
    "padding": "0rem 0rem",
    "background-color": "#303030",
    "font-family": "ui-monospace",
    "color": "#ffffff"
}
CONTENT_STYLE = {
    "margin-left": "17rem",
    "font-family": "ui-monospace",
    "background-color": "#f2f3f4",

}
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Load data
df = pd.read_csv('data/idmc_disaster_all_dataset.csv')
dfs = pd.read_excel('data/emdat.xlsx')

df.dropna(subset=["Hazard_Type"], inplace=True)
df.dropna(subset=["New Displacements"], inplace=True)
dfs.dropna(subset=["Disaster Type"], inplace=True)
df_temp = pd.read_csv('data/temperature.csv')

nat_dis_slider = html.Div([daq.Slider(
    id='dis_slider',
    min=dfs['Year'].min(),
    max=dfs['Year'].max() - 1,
    value=dfs['Year'].min(),
    handleLabel={"showCurrentValue": True, "label": "YEAR"},
    color="MediumVioletRed",
    size=210,

)], style={"margin-left": "1.5rem", "padding": "0.5rem 0.5rem"})
pop_slider = html.Div([daq.Slider(
    id='pop_slider',
    min=df['Year'].min(),
    max=df['Year'].max(),
    value=df['Year'].min(),
    handleLabel={"showCurrentValue": True, "label": "YEAR"},
    color="MediumVioletRed",
    size=210,

)], style={"margin-left": "1.5rem", "padding": "0.5rem 0.5rem"}),

pop_country_filter = html.Div([

    dcc.Dropdown(
        id='pop_country_dropdown',
        options=[{'label': ' ' + i, 'value': i} for i in list(df['Name'].unique())],
        value=[],
        placeholder="Select a country",
        style={
            "background-color": "grey",
            "font-family": "ui-monospace",
        },

    ),

], style={"margin-left": "0.5rem", "margin-right": "0.5rem ", "font-size": 15, "color": "black"}),
dis_country_filter = html.Div([
    dcc.Dropdown(
        id='dis_country_dropdown',
        options=[{'label': ' ' + i, 'value': i} for i in list(dfs['Country'].unique())],
        value=[],
        placeholder="Select a country",
        style={
            "background-color": "grey",
            "font-family": "ui-monospace",
        },

    ),

], style={"margin-left": "0.5rem", "margin-right": "0.5rem ", "font-size": 15, "color": "black"}),
pop_checkbox = html.Div([

    dcc.Checklist(
        id="all-dis-checklist",
        options=[{"label": " All", "value": "All"}],
        value=["All"],
        labelStyle={"display": "inline-block"},
    ),
    dcc.Checklist(
        id='dis-checklist',
        options=[{'label': ' ' + i, 'value': i} for i in list(df['Hazard_Type'].unique())],
        value=[],
        labelStyle=dict(display='block')
    ),

], style={"margin-left": "0.5rem", "font-size": 15, "maxHeight": 120, "overflow": "scroll"})

dis_checkbox = html.Div([

    dcc.Checklist(
        id="all-dis-checklist1",
        options=[{"label": " All", "value": "All"}],
        value=["All"],
        labelStyle={"display": "inline-block"},
    ),
    dcc.Checklist(
        id='dis-checklist1',
        options=[{'label': ' ' + i, 'value': i} for i in list(dfs['Disaster Type'].unique())],
        value=[],
        labelStyle=dict(display='block')
    ),

], style={"margin-left": "0.5rem", "font-size": 15, "maxHeight": 120, "overflow": "scroll"})

temp_label_pop = html.Div([

    html.Label('0.31°C', id="update-temp-by-year")

], style={"margin-left": "4rem",
          "padding": "0.5rem 0.5rem",
          "font-size": 33}),
temp_label_dis = html.Div([

    html.Label('0.31°C', id="update-temp-by-year-dis")

], style={"margin-left": "4rem",
          "padding": "0.5rem 0.5rem",
          "font-size": 33}),

# SIDEBAR--------------------------------------------------------------------------
sidebar = html.Div(
    [
        html.Div([html.H1("The Effects of Climate Change", className="display-4")], style={"background": "#000039",
                                                                                           "padding": "0.5rem 0.5rem",
                                                                                           "font-size": 15}),
        html.Div([html.Label(' Global Temperature')], style={"background": "black", "padding": "0.5rem 0.5rem"}),
        html.Br(),
        html.Div(id='sidebar-temp'),
        html.Br(),

        html.Div(id='sidebar-content'),

        # year slider
        html.Div([html.Label(' Change Year ')], style={"background": "black", "padding": "0.5rem 0.5rem"}),
        html.Br(),
        html.Br(),
        html.Br(),
        html.Div(id='slider'),
        html.Br(),
        html.Div([html.Label(' Filter by Country ')], style={"background": "black", "padding": "0.5rem 0.5rem"}),
        html.Br(),
        html.Div(id='country_dropdown'),
        html.Br(),
        html.Div([html.Label(' Disaster Type ')], style={"background": "black", "padding": "0.5rem 0.5rem"}),
        html.Br(),
        html.Div(id='disaster_checkbox'),
    ],
    id="side-bar",
    style=SIDEBAR_STYLE,
)

app.layout = html.Div([

    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div(id='page-content')
])


# Update the slider in sidebar
@app.callback(dash.dependencies.Output('slider', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return nat_dis_slider
    elif pathname == '/page-1':
        return pop_slider
    else:
        return pop_slider


# Update the country dropdown in sidebar
@app.callback(dash.dependencies.Output('country_dropdown', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return dis_country_filter
    elif pathname == '/page-1':
        return pop_country_filter
    else:
        return pop_country_filter


# Update the disaster filter in sidebar
@app.callback(dash.dependencies.Output('disaster_checkbox', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return dis_checkbox
    elif pathname == '/page-1':
        return pop_checkbox
    else:
        return pop_checkbox


# Update the slider in sidebar
@app.callback(dash.dependencies.Output('sidebar-temp', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-2':
        return temp_label_dis
    elif pathname == '/page-1':
        return temp_label_pop
    else:
        return temp_label_dis


@app.callback(dash.dependencies.Output('update-temp-by-year', 'children'),
              dash.dependencies.Input('pop_slider', 'value'))
def update_temp(selected_year):
    filtered_df = df_temp[df_temp.Year == selected_year]
    temp = filtered_df['Temperature'].values[0]

    return html.Label(str(temp) + '°C')


@app.callback(dash.dependencies.Output('update-temp-by-year-dis', 'children'),
              dash.dependencies.Input('dis_slider', 'value'))
def update_temp(selected_year):
    filtered_df = df_temp[df_temp.Year == selected_year]
    temp = filtered_df['Temperature'].values[0]
    print(temp)
    return html.Label(str(temp) + '°C')


# POPULATION DISPLACEMENTS -----------------------------------------------------------
page_1_layout = html.Div([

    html.Div([
        html.Div([
            html.H2('Population Displacements'),
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Link('See Natural Disasters', href='/page-2', style={"font-size": 16}),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '15.5vw',
                  'margin-top': '2vw'})
    ]),

    html.Div(id='page-1-content'),
    html.Div([
        html.Div([
            dcc.Graph(id='graph1'),
        ], style={'width': '100%'}),

        html.Div([
            dcc.Graph(id='graph2'),
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='graph3',
                      figure=px.line(df_temp, x="Year", y="Temperature",
                                     custom_data=['Temperature', 'Year']),
                      )

        ], style={'width': '50%', 'display': 'inline-block'}),

    ], className="row"),

    html.Br(),

], style=CONTENT_STYLE)


@app.callback(dash.dependencies.Output('graph2', 'figure'),
              dash.dependencies.Input('dis-checklist', 'value'),
              dash.dependencies.Input('pop_country_dropdown', 'value'))
def update_figure(selected_disaster, selected_country):
    df1 = pd.DataFrame(df.groupby(by=['Year', 'Hazard_Type', 'Name'])['New Displacements'].sum())
    df1.reset_index(inplace=True)

    filtered_df = df1[df1.Hazard_Type.isin(selected_disaster)]
    if selected_country:
        filtered_df = filtered_df[filtered_df.Name == selected_country]

    fig = px.bar(filtered_df, x="Year", y="New Displacements", color="New Displacements",
                 hover_name="Hazard_Type", custom_data=['Hazard_Type', 'New Displacements', 'Year'],
                 color_continuous_scale=["Thistle", "purple", "MidnightBlue"])

    fig.update_layout(
        title={'text': "Displacements Over Time", 'y': 0.93},
        paper_bgcolor="#303030",
        plot_bgcolor="#303030",
        font={'color': "white",
              'family': "ui-monospace"},
        yaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.25)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.25)"),
        margin=dict(l=10, r=10, t=55, b=10),
        hoverlabel=dict(
            font_size=14,
            font_family="ui-monospace",
        ),
    )
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b></br> '
                                    '<br>Year: <b>%{customdata[2]}</b> <br>Total Displacements:'
                                    ' <b>%{customdata[1]:,}</b>')
    return fig


@app.callback(dash.dependencies.Output('graph3', 'figure'),
              dash.dependencies.Input('pop_slider', 'value'))
def update_figure(selected_year):

    fig = px.line(df_temp, x="Year", y="Temperature",
                  custom_data=['Temperature', 'Year'])
    fig.update_layout(
        title={'text': "Yearly Global Temperatures", 'y': 0.93},
        paper_bgcolor="#303030",
        plot_bgcolor="#303030",
        font={'color': "white",
              'family': "ui-monospace"},
        yaxis=dict(title='Temperature (°C)', gridcolor="rgba(255,255,255,0.25)",
                   zerolinecolor="rgba(255,255,255,0.25)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.25)"),
        margin=dict(l=10, r=10, t=55, b=10),
        hoverlabel=dict(
            font_size=14,
            font_family="ui-monospace",
        ),
    )
    fig.update_traces(hovertemplate='<b>%{customdata[0]}°C</b> '
                                    '<br>Year: <b>%{customdata[1]}</b> ')
    return fig


# DISASTER STATS -------------------------------------------------------------------
page_2_layout = html.Div([

    html.Div([
        html.Div([
            html.H2('Natural Disasters'),
        ], style={'width': '50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Link('See Population Displacements', href='/page-1', style={"font-size": 16}),
        ], style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '15.5vw',
                  'margin-top': '2vw'})
    ]),
    html.Div(id='page-2-content'),

    html.Div([
        html.Div([
            dcc.Graph(id='g1')
        ], style={'width': '100%'}),

        html.Div([
            dcc.Graph(id='g2'),

        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='g3',
                      figure=px.line(dfs, x="Year", y="Total Deaths",
                                     custom_data=['Year', 'Total Deaths']),
                      )

        ], style={'width': '49%', 'display': 'inline-block'}),

    ], className="row"),

    html.Br(),

], style=CONTENT_STYLE)


@app.callback(dash.dependencies.Output('g3', 'figure'),
              dash.dependencies.Input('dis-checklist1', 'value'),
              dash.dependencies.Input('dis_country_dropdown', 'value'))
def update_figure(selected_disaster, selected_country):

    title = "(Globally)"
    filtered_df3 = dfs
    if selected_disaster and selected_country:
        title = "(" + selected_country + ")"
        filtered_dis = filtered_df3[filtered_df3['Disaster Type'].isin(selected_disaster)]
        filtered_df3 = filtered_dis[filtered_dis.Country == selected_country]
    elif selected_country and not selected_disaster:
        title = "(" + selected_country + ")"
        filtered_df3 = filtered_df3[filtered_df3.Country == selected_country]
    elif selected_disaster and not selected_country:
        filtered_df3 = filtered_df3[filtered_df3['Disaster Type'].isin(selected_disaster)]

    filtered_df2 = pd.DataFrame(
        filtered_df3.groupby(by=['Year', 'Disaster Type'], as_index=False)['Total Deaths'].sum())
    filtered_df4 = pd.DataFrame(
        filtered_df3.groupby(by=['Year', 'Disaster Type'], as_index=False)['Total Damages'].sum())

    # fig = go.Figure
    fig1 = px.line(filtered_df2, x="Year", y="Total Deaths", custom_data=['Total Deaths', 'Year', 'Disaster Type'],
                   title=f"Total Casualties by Year <b>{title}")

    fig1.update_traces(hovertemplate='Total Casualties: <b>%{customdata[0]:,}</b> '
                                     '<br>Disaster type: <b>%{customdata[2]}</b>'
                                     '<br>Year: <b>%{customdata[1]}</b> '),
    fig1.add_trace(
        go.Scatter(
            x=filtered_df4.Year,
            y=filtered_df4['Total Damages'],
            name="damages",
            text=filtered_df4['Disaster Type'],
            hovertemplate='Damages: <b>$%{y:,}</b> '
                          '<br>Disaster type: <b>%{text}</b>'
                          '<br>Year: <b>%{x}</b> ',
            line=dict(color="MediumVioletRed"),

            visible=False,
        ),
    )
    fig1.update_layout(
        paper_bgcolor="#303030",
        plot_bgcolor="#303030",
        font={'color': "white",
              'family': "ui-monospace"},
        margin=dict(l=10, r=10, t=55, b=10),
        hoverlabel=dict(
            font_size=14,
            font_family="ui-monospace",
        ),
        yaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.25)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.25)"),
        yaxis_title="Casualties",
        updatemenus=[
            dict(
                active=0,
                x=0,
                y=1.04,
                font=dict(family='ui-monospace'),
                bgcolor="grey",
                buttons=list([
                    dict(label="Casualties",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Total Casualties by Year" + " <b>" + title,
                                'yaxis': dict(title='Casualties', gridcolor="rgba(255,255,255,0.25)",
                                              zerolinecolor="rgba(255,255,255,0.25)"),
                                'xaxis': dict(gridcolor="rgba(255,255,255,0.25)",
                                              zerolinecolor="rgba(255,255,255,0.25)"),
                                "annotations": []}]),
                    dict(label="Damages",
                         method="update",

                         args=[{"visible": [False, True]},
                               {"title": "Total Damages by Year" + " <b>" + title,
                                'yaxis': dict(title='Total Damages (US$)', gridcolor="rgba(255,255,255,0.25)",
                                              zerolinecolor="rgba(255,255,255,0.25)"),
                                'xaxis': dict(gridcolor="rgba(255,255,255,0.25)",
                                              zerolinecolor="rgba(255,255,255,0.25)"
                                              ),
                                "annotations": []}]),
                ]),
            )])

    return fig1


@app.callback(dash.dependencies.Output('g2', 'figure'),
              dash.dependencies.Input('dis-checklist1', 'value'),
              dash.dependencies.Input('dis_slider', 'value'),
              dash.dependencies.Input('dis_country_dropdown', 'value'))
def update_figure(selected_disaster, selected_year, selected_country):
    filtered_df_year = dfs[dfs.Year == selected_year]
    df1 = pd.DataFrame(filtered_df_year.groupby(by=['Year', 'Disaster Type', 'Country'])['Total Deaths'].sum())
    df1.reset_index(inplace=True)
    print("DF1", df1)
    title = ""
    filtered_df3 = df1
    if selected_disaster and selected_country:
        title = "(" + selected_country + ")"
        filtered_dis = filtered_df3[filtered_df3['Disaster Type'].isin(selected_disaster)]
        filtered_df3 = filtered_dis[filtered_dis.Country == selected_country]

    elif selected_country and not selected_disaster:
        title = "(" + selected_country + ")"
        filtered_df3 = filtered_df3[filtered_df3.Country == selected_country]
    elif selected_disaster and not selected_country:
        filtered_df3 = filtered_df3[filtered_df3['Disaster Type'].isin(selected_disaster)]

    year = selected_year

    if filtered_df3.empty:
        return {
            "layout": {
                "xaxis": {
                    "visible": True
                },
                "yaxis": {
                    "visible": True
                },
                "paper_bgcolor": "#303030",
                "plot_bgcolor": "#303030",
                "annotations": [
                    {
                        "text": f"No matching data found :(",
                        "xref": "paper",
                        "yref": "paper",
                        "showarrow": False,
                        "font": {
                            "size": 19,
                            "family": "ui-monospace",
                            "color": "grey"
                        }
                    }
                ]
            }
        }
    fig = px.bar(filtered_df3, x="Total Deaths", y="Disaster Type", color="Disaster Type", orientation='h',
                 hover_name="Disaster Type", custom_data=['Disaster Type', 'Total Deaths', 'Year'],
                 title=f"<b>{year}</b> Casualties by Disaster Type <b>{title}"
                 )

    fig.update_layout(
        title={'y': 0.93},
        paper_bgcolor="#303030",
        plot_bgcolor="#303030",
        font={'color': "white",
              'family': "ui-monospace"},
        yaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.75)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.25)", zerolinecolor="rgba(255,255,255,0.25)"),
        margin=dict(l=10, r=10, t=55, b=10),
        hoverlabel=dict(
            font_size=14,
            font_family="ui-monospace",
        ),
    )
    fig.update_traces(hovertemplate='<b>%{customdata[0]}</b></br> '
                                    '<br>Year: <b>%{customdata[2]}</b> <br>Total Casualties:'
                                    ' <b>%{customdata[1]:,}</b>')
    fig.update_yaxes(visible=False, showticklabels=False)

    return fig


@app.callback(
    dash.dependencies.Output("dis-checklist", "value"),
    dash.dependencies.Output("all-dis-checklist", "value"),
    dash.dependencies.Input("dis-checklist", "value"),
    dash.dependencies.Input("all-dis-checklist", "value"),
)
def sync_checklists(dis_selected, all_selected):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dis-checklist":
        all_selected = ["All"] if set(dis_selected) == set(df.Hazard_Type) else []
    else:
        dis_selected = df.Hazard_Type.unique() if all_selected else []
    return dis_selected, all_selected


@app.callback(
    dash.dependencies.Output("dis-checklist1", "value"),
    dash.dependencies.Output("all-dis-checklist1", "value"),
    dash.dependencies.Input("dis-checklist1", "value"),
    dash.dependencies.Input("all-dis-checklist1", "value"),
)
def sync_checklists(dis_selected, all_selected):
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if input_id == "dis-checklist1":
        all_selected = ["All"] if set(dis_selected) == set(dfs['Disaster Type']) else []
    else:
        dis_selected = dfs['Disaster Type'].unique() if all_selected else []
    return dis_selected, all_selected


@app.callback(dash.dependencies.Output('g1', 'figure'),
              dash.dependencies.Input('dis_slider', 'value'),
              dash.dependencies.Input('dis-checklist1', 'value'))
def update_map2(selected_year, selected_disaster):
    filtered_df = dfs[dfs.Year == selected_year]
    if selected_disaster:
        filtered_df3 = filtered_df[filtered_df['Disaster Type'].isin(selected_disaster)]
    else:
        filtered_df3 = filtered_df
    filtered_df2 = pd.DataFrame(
        filtered_df3.groupby(by=['Disaster Type', 'ISO', 'Country'], as_index=False)['Total Deaths'].sum())

    map_fig = px.scatter_geo(filtered_df2, locations="ISO", color="Disaster Type",
                             color_discrete_map=color_map_dis,
                             size="Total Deaths", size_max=50,
                             custom_data=['Disaster Type', 'Total Deaths', 'Country']
                             )
    map_fig.update_geos(
        showcoastlines=True, coastlinecolor="#3D3D3D",
        showland=True, landcolor="black",
        showocean=True, oceancolor="#303030",
        showlakes=True, lakecolor="#202945",
        showcountries=True, countrycolor="#3D3D3D",
        fitbounds="locations",
    )

    map_fig.update_layout(
        autosize=False,
        width=1010,
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        hoverlabel=dict(
            font_size=14,
            font_family="ui-monospace",
        ),
        legend_title="Disaster Types",
        legend=dict(
            title_font_family="ui-monospace",
            title_font_color="white",
            yanchor="top",
            y=0.35,
            xanchor="left",
            x=0,
            font=dict(
                family="ui-monospace",
                size=12,
                color="white",
            ),
            bgcolor="#000039",
            bordercolor="Black",
            borderwidth=2,

        ),
    )
    map_fig.update_traces(hovertemplate='Casualties: <b>%{customdata[1]:,}</b></br> '
                                        '<br>Disaster Type: <b>%{customdata[0]}</b> <br>Country:'
                                        ' <b>%{customdata[2]}</b>',
                          )

    return map_fig


color_map = {'Flood': '#29335C',
             'Earthquake': 'yellow',
             'Extreme temperature': 'rgb(255,127,0)',
             'Wet mass movement': '#F0CEA0',
             'Dry mass movement': '#534D41',
             'Storm': '#17BECF',
             'Drought': '#ed7953',
             'Volcanic eruption': 'Magenta',
             'Wildfire': 'red',
             'Mass movement': '#f0f921',
             'Volcanic activity': '#1B98E0',
             'Severe winter condition': '#E8F1F2',
             }
color_map_dis = {'Flood': '#29335C',
                 'Earthquake': 'yellow',
                 'Extreme temperature': 'rgb(255,127,0)',
                 'Epidemic': '#F0CEA0',
                 'Mass movement (dry)': '#534D41',
                 'Storm': '#17BECF',
                 'Drought': '#ed7953',
                 'Wildfire': 'red',
                 'Insect infestation': '#f0f921',
                 'Volcanic activity': '#1B98E0',
                 'Landslide': '#E8F1F2',
                 }


@app.callback(dash.dependencies.Output('graph1', 'figure'),
              dash.dependencies.Input('pop_slider', 'value'),
              dash.dependencies.Input('dis-checklist', 'value'))
def update_map2(selected_year, selected_disaster):
    filtered_df = df[df.Year == selected_year]

    if selected_disaster:
        filtered_df3 = filtered_df[filtered_df.Hazard_Type.isin(selected_disaster)]
    else:
        filtered_df3 = filtered_df
    filtered_df2 = pd.DataFrame(
        filtered_df3.groupby(by=['Hazard_Type', 'ISO3', 'Name'], as_index=False)['New Displacements'].sum())

    map_fig = px.scatter_geo(filtered_df2, locations="ISO3", color="Hazard_Type",
                             color_discrete_map=color_map,
                             size="New Displacements", size_max=50,
                             custom_data=['Hazard_Type', 'New Displacements', 'Name']

                             )
    map_fig.update_geos(
        showcoastlines=True, coastlinecolor="#3D3D3D",
        showland=True, landcolor="black",
        showocean=True, oceancolor="#303030",
        showlakes=True, lakecolor="#202945",
        showcountries=True, countrycolor="#3D3D3D",
        fitbounds="locations",
    )

    map_fig.update_layout(
        autosize=False,
        width=1010,
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        hoverlabel=dict(
            font_size=14,
            font_family="ui-monospace",
        ),
        legend_title="Disaster Types",
        legend=dict(
            title_font_family="ui-monospace",
            title_font_color="white",
            yanchor="top",
            y=0.35,
            xanchor="left",
            x=0,
            font=dict(
                family="ui-monospace",
                size=12,
                color="white",
            ),
            bgcolor="#000039",
            bordercolor="Black",
            borderwidth=2,

        ),

    )
    map_fig.update_traces(hovertemplate='Displacements: <b>%{customdata[1]:,}</b></br> '
                                        '<br>Disaster Type: <b>%{customdata[0]}</b> <br>Country:'
                                        ' <b>%{customdata[2]}</b>')
    return map_fig


# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return page_1_layout


if __name__ == '__main__':
    app.run_server(debug=True)
