import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
from dash import callback
from pages import home, matriculas_por_campus, matriculas_por_tipo, matriculas_equivalentes_por_campus, matriculas_equivalentes_por_tipo
from pages import matriculas_anual, eficiencia_academica, RAP_RAPP, RIV, evasao, ocupacao, verticalizacao

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='location'),
    html.Div(id='output')
])

@app.callback(Output('output', 'children'), Input('location', 'href'))
def display_href(href):
    #print(href)
    if href.split('/')[-1]=='':
        pagina=home.layout
        return pagina
    elif href.split('/')[-1]=='matriculas_por_campus':
        return matriculas_por_campus.app.layout
    elif href.split('/')[-1]=='matriculas_por_tipo':
        return matriculas_por_tipo.app.layout
    elif href.split('/')[-1]=='matriculas_equivalentes_por_campus':
        return matriculas_equivalentes_por_campus.app.layout
    elif href.split('/')[-1]=='matriculas_equivalentes_por_tipo':
        return matriculas_equivalentes_por_tipo.app.layout
    elif href.split('/')[-1]=='matriculas_anual':
        return matriculas_anual.app.layout
    elif href.split('/')[-1]=='eficiencia_academica':
        return eficiencia_academica.app.layout
    elif href.split('/')[-1]=='RAP_RAPP':
        return RAP_RAPP.app.layout
    elif href.split('/')[-1]=='RIV':
        return RIV.app.layout
    elif href.split('/')[-1]=='evasao':
        return evasao.app.layout
    elif href.split('/')[-1]=='ocupacao':
        return ocupacao.app.layout
    elif href.split('/')[-1]=='verticalizacao':
        return verticalizacao.app.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run(debug=True)