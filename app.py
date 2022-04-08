import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import plotly as pl


df = pd.read_excel("tabela produtos.xlsx")

mark_values= {2010:'2010', 2011:'2011', 2012:'2012', 2013:'2013', 2014:'2014',
             2015:'2015', 2016:'2016', 2017:'2017', 2018:'2018',
             2019:'2019', 2020:'2020', 2021:'2021', 2022:'2022'}
app = Dash(__name__)
server = app.server

colors = {
    'background': '#ffffff',
    'text': '#000000'
    }

fig = px.sunburst(df, path=['Fonte', 'Área', 'Produto'],
                  values='Qt indicadores (Outputs)',
                  labels="Produtos",
                  color="Área",
                  color_discrete_map={
                      "Projetos": "#2bc470",
                      "Pessoal": "#f2e824",
                      "Operações": "#ed892b",
                      "Financeira": "#11a10a",
                      "Estatistica": "#c9352a"},
                  height=750
                  )
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
    dcc.Graph(id="scatter-plot"),
    ]),
    html.Br(),

    html.Div([
        dcc.RangeSlider(id='year-slider',
            min=2010,
            max=2022,
            value=[2010,2022],
            marks=mark_values,
            step=None)
    ], style = {"width": "70%", "position":"absolute",
                 "left":"15%"})
    ]),
    html.Br(),
    html.Br(),
    html.Div([
    dcc.Graph(id="sunburst",
              figure=fig),
    ]),
])
    #dcc.RangeSlider(2009, 2023, 1, value=[2009, 2023], id='my-range-slider'),
@app.callback(
    Output('scatter-plot','figure'),
    [Input('year-slider','value')]
    )
def update_graph(years_chosen):
    # print(years_chosen)
    dff = df[(df['Data'] >= years_chosen[0]) & (df['Data'] <= years_chosen[1])]

    scatterplot = px.scatter(
        data_frame=dff,
        x="Data",
        y="Fonte",
        size="Qt indicadores (Outputs)",
        color="Área",
        hover_data=['Produto'],
        #text="Produto",
        height=550,
        color_discrete_map={
            "Projetos": "#2bc470",
            "Pessoal": "#f2e824",
            "Operações": "#ed892b",
            "Financeira": "#11a10a",
            "Estatistica": "#fa7575"}
            )

    scatterplot.update_layout(plot_bgcolor="#FFFFFF",
                              xaxis = dict(title=dict(text="", font=dict(size=20), font_family="Arial")),
                              yaxis = dict(title=dict(text="", font=dict(size=20), font_family="Arial")),
                              )
    scatterplot.update_xaxes(gridcolor="#e3dfde")
    scatterplot.update_yaxes(gridcolor="#e3dfde")
    scatterplot.update_traces(marker_sizeref=0.01)
    scatterplot.update_layout(margin_pad=20)
    scatterplot.update_xaxes(tickfont=dict(color='#38383b', size=16))
    scatterplot.update_yaxes(tickfont=dict(color='#38383b', size=16))
    scatterplot.update_layout(legend=dict(font_size=20))

    return (scatterplot)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
