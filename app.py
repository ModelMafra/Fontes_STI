import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import plotly as pl
import warnings
warnings.filterwarnings('ignore')

df = pd.read_excel("tabela produtos.xlsx")

mark_values= {2010:{'label':'2010', 'style': {'font-size': '140%'}},
2011:{'label':'2011', 'style': {'font-size': '140%'}},
2012:{'label':'2012', 'style': {'font-size': '140%'}},
2013:{'label':'2013', 'style': {'font-size': '140%'}},
2014:{'label':'2014', 'style': {'font-size': '140%'}},
2015:{'label':'2015', 'style': {'font-size': '140%'}},
2016:{'label':'2016', 'style': {'font-size': '140%'}},
2017:{'label':'2017', 'style': {'font-size': '140%'}},
2018:{'label':'2018', 'style': {'font-size': '140%'}},
2019:{'label':'2018', 'style': {'font-size': '140%'}},
2020:{'label':'2020', 'style': {'font-size': '140%'}},
2021:{'label':'2021', 'style': {'font-size': '140%'}},
2022:{'label':'2022', 'style': {'font-size': '140%'}}}



app = Dash(__name__)
server = app.server

colors = {
    'background': '#ffffff',
    'text': '#000000'
    }

fig = px.sunburst(df, path=['Fonte', 'Área', 'Produto'],
                  values='Qt indicadores (Outputs)',
                  labels="Produtos",
                  color="Fonte",
                  color_discrete_map={"EPM": "#9DB3A0",
                                      "Access": "#657367",
                                      "SIEE": "#D5F2DA",
                                      "Excel": "#E0FFE5",
                                      "SIIP": "#BFD9C3",
                                      "Edoclink": "#CFF9EE",
                                      "SIGAI": "#B6DBC7",
                                      "Google Analytics": "#D5F2DA",
                                      "SIMPPO": "#BBDBB6",
                                      "VagasNaPraia": "#E4F9CF"},
                  height=950
                  )
fig.update_layout(uniformtext=dict(minsize=14))
# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Sistemas e Indicadores de Apoio à Decisão STI ",
                style={'backgroundColor': colors['background'],
                       'text-align': 'center',
                       'color': colors['text'],
                       'font-family': 'Arial'}),
    html.Br(),

    html.Div([
        dcc.Tabs(id='tabs-example-1', value='tab-1', children=[
        dcc.Tab(label='Evolução dos Produtos BI',
                value='tab-1',
                style={'font-size': '140%', 'font-family': 'Arial', 'color': '#bbbdbf'},
                selected_style={'font-size': '140%', 'font-family': 'Arial'}),

        dcc.Tab(label='Produtos e Área por Fonte',
                value='tab-2',
                style={'font-size': '140%', 'font-family': 'Arial', 'color': '#bbbdbf'},
                selected_style={'font-size': '140%', 'font-family': 'Arial'})
        ]),
    html.Div(id='tabs-example-content-1')
            ]),
    ]),
])

@app.callback(
    Output('tabs-example-content-1', 'children'),
    Input('tabs-example-1', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([dcc.Graph(id="scatter-plot")]),
            html.Div([
                dcc.RangeSlider(id='year-slider',
                                min=2010,
                                max=2022,
                                value=[2010, 2022],
                                marks=mark_values,
                                step=None)
            ], style={"width": "70%", "position": "absolute",
                      "left": "15%"})
            ])
    elif tab == 'tab-2':
          return html.Div([dcc.Graph(id="sunburst", figure=fig)])


@app.callback(
    Output('scatter-plot', 'figure'),
    Input('year-slider', 'value')
    )
def update_graph(years_chosen):
    # print(years_chosen)
    dff = df[(df['Data'] >= years_chosen[0]) & (df['Data'] <= years_chosen[1])]

    scatterplot = px.scatter(
        data_frame=dff,
        x="Data",
        y='Fonte',
        size="Qt indicadores (Outputs)",
        color="Área",
        hover_data=['Produto'],
        #text="Produto",
        height=650,
        # width=1250,
        color_discrete_map={
            "Projetos": "#9DB3A0",
            "Pessoal": "#E0D779",
            "Operações": "#719DDE",
            "Financeira": "#A7DEA6",
            "Estatistica": "#D7DBB6"}
            )

    scatterplot.update_layout(plot_bgcolor="#FFFFFF",
                              xaxis = dict(title=dict(text="", font=dict(size=20), font_family="Arial")),
                              yaxis = dict(title=dict(text="", font=dict(size=20), font_family="Arial")),
                              )
    scatterplot.update_xaxes(gridcolor="#e3dfde")
    scatterplot.update_yaxes(gridcolor="#e3dfde",categoryorder='category descending')
    scatterplot.update_traces(marker_sizeref=0.01)
    scatterplot.update_xaxes(tickfont=dict(color='#38383b', size=16))
    scatterplot.update_yaxes(tickfont=dict(color='#38383b', size=16))
    scatterplot.update_layout(legend=dict(font_size=20))
    scatterplot.update_layout(margin_pad=20)
    return (scatterplot)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
