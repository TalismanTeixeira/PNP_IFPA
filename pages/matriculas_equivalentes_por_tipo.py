import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
from pathlib import Path
from dash import callback
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

pasta_raiz = Path(__file__).parent.parent
#matriculas = pd.read_csv(pasta_raiz / 'data/PDA_PNP_Matriculas.csv')
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',',decimal=',')
matriculas['MATRICULAS_TOTAL'] = pd.to_numeric(matriculas['MATRICULAS_EQUIVALENTES'].str.replace(',','.'))
matriculas_por_campus = matriculas.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['MATRICULAS_TOTAL'].sum().reset_index()

campus = matriculas_por_campus['UNIDADE_DE_ENSINO'].unique()
#items_campus = [dbc.DropdownMenuItem(x) for x in campus]

curso = matriculas_por_campus['NOME_DE_CURSO'].unique()
#items_curso = [dbc.DropdownMenuItem(x) for x in curso]

tipo = matriculas_por_campus['TIPO_DE_CURSO'].unique()
#items_tipo = [dbc.DropdownMenuItem(x) for x in tipo]

eixo = matriculas_por_campus['EIXO_TECNOLOGICO'].unique()
#items_eixo = [dbc.DropdownMenuItem(x) for x in eixo]



app.layout = html.Div([
    dbc.Row([
                dbc.Col([],md=1),
                dbc.Col([
                    html.H5('IFPA'),
                    html.H1('Instituto Federal do Pará', style={'fontWeight':'bold'}),
                    html.H5('MINISTÉRIO DA EDUCAÇÃO')
                ], md=10),
                dbc.Col([], md=1),
            ], className='linha_verde'),
    dbc.Row([
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    html.H1('Matrículas Equivalentes por Tipo de Curso e Eixo Tecnológico'),
                    html.Br(),
                ])
            ]),
            dbc.Row([
                dbc.Col([],md=1),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                                html.H5('Escolha o campus'),
                                dcc.Dropdown(
                                    id = 'campus4',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o curso'),
                                dcc.Dropdown(
                                    id = 'curso4',
                                    style={'font-size':'12px',}   
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o tipo de curso'),
                                dcc.Dropdown(
                                    id = 'tipo4',
                                    options = tipo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o eixo tecnológico'),
                                dcc.Dropdown(
                                    id = 'eixo4',
                                    options = eixo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph5')
                ],md=10)
            ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph6')
                ],md=10)
            ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph_equival_curso')
                ],md=10)
            ]),
    ])  
])

@callback(Output('curso4','options'),Input('campus4','value',),Input('eixo4','value'),Input('tipo4','value'),)
def filtra_campus(campus=None, eixo=None, tipo=None):
    if campus==None:
        if (tipo==None) & (eixo != None):
            curso = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]['NOME_DE_CURSO'].unique()
        elif (eixo==None) & (tipo != None):
            curso = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]['NOME_DE_CURSO'].unique()
        elif (tipo!=None) & (eixo != None):
            curso = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]['NOME_DE_CURSO'].unique()
        else: 
            curso = matriculas_por_campus['NOME_DE_CURSO'].unique()
    else:
        if (tipo==None) & (eixo != None):
            curso = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]['NOME_DE_CURSO'].unique()
        elif (eixo==None) & (tipo != None):
            curso = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]['NOME_DE_CURSO'].unique()
        elif (eixo!=None) & (tipo != None):
            curso = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]['NOME_DE_CURSO'].unique()
        else:
            curso = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)]['NOME_DE_CURSO'].unique()
    ####print(curso)
    return curso

@callback(Output('graph5','figure'),Input('campus4','value'),Input('curso4','value'),Input('tipo4','value'),Input('eixo4','value'),)
def grafico_matriculas(campus,curso_escolhido,tipo,eixo):
    ##print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    ##print(mat_filtrado)
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = px.treemap(mat_filtrado, 
                     path=[px.Constant('Tipo de Curso'),'TIPO_DE_CURSO','UNIDADE_DE_ENSINO','NOME_DE_CURSO'],
                     values='MATRICULAS_TOTAL',)
    fig.update_layout(height = 600, width=1200)
    fig.update_traces(hovertemplate = 'Campus: %{parent}<br>Curso: %{label}<br>Matrículas: %{value}')
    return fig


@callback(Output('graph6','figure'),Input('campus4','value'),Input('curso4','value'),Input('tipo4','value'),Input('eixo4','value'),)
def grafico_matriculas(campus,curso_escolhido,tipo,eixo):
    ##print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    ##print(mat_filtrado)
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = px.treemap(mat_filtrado, 
                     path=[px.Constant('Eixo Tecnológico'),'EIXO_TECNOLOGICO','UNIDADE_DE_ENSINO','NOME_DE_CURSO'],
                     values='MATRICULAS_TOTAL',)
    fig.update_layout(height = 600, width=1200)
    fig.update_traces(hovertemplate = '%{parent}<br>%{label}<br>Matrículas: %{value:.2f}')
    return fig


@callback(Output('graph_equival_curso','figure'),Input('campus4','value'),Input('curso4','value'),Input('tipo4','value'),Input('eixo4','value'),)
def grafico_matriculas(campus,curso_escolhido,tipo,eixo):
    ###print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    ####print(mat_filtrado)
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = px.treemap(mat_filtrado, 
                     path=[px.Constant('Curso'),'NOME_DE_CURSO','UNIDADE_DE_ENSINO'],
                     values='MATRICULAS_TOTAL',)
    fig.update_layout(height = 600, width=1200)
    fig.update_traces(hovertemplate = '%{parent}<br>%{label}<br>Matrículas: %{value}')
    return fig