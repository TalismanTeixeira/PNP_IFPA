import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
from pathlib import Path
from dash import callback
import plotly.express as px
import warnings
warnings.filterwarnings("ignore")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

pasta_raiz = Path(__file__).parent.parent

matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',', decimal = ',')

matriculas['MATRICULAS_TOTAL'] = matriculas['MATRICULAS_ATENDIDA'].replace('Sim',1)
matriculas_por_campus = matriculas.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['MATRICULAS_TOTAL'].sum().reset_index()
matriculas['MATRICULAS_TOTAL'].value_counts()

campus = matriculas_por_campus['UNIDADE_DE_ENSINO'].unique()
curso = matriculas_por_campus['NOME_DE_CURSO'].unique()
tipo = matriculas_por_campus['TIPO_DE_CURSO'].unique()
eixo = matriculas_por_campus['EIXO_TECNOLOGICO'].unique()

matriculas_por_tipo_de_curso = matriculas_por_campus.groupby('TIPO_DE_CURSO')['MATRICULAS_TOTAL'].sum().reset_index().sort_values(by='MATRICULAS_TOTAL')
matriculas_por_eixo_tecnologico = matriculas_por_campus.groupby('EIXO_TECNOLOGICO')['MATRICULAS_TOTAL'].sum().reset_index().sort_values(by='MATRICULAS_TOTAL')

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
                    html.H1('Matrículas por campus'),
                    html.Br(),
                    html.Hr(),
                    dbc.RadioItems(options=['2017','2018','2019','2020','2021','2022'], value='2022 ', inline=True, id = 'ano_mat_campus'),
                    html.Hr(),
                ])
            ]),
            dbc.Row([
                dbc.Col([],md=1),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                                html.H5('Escolha o campus'),
                                dcc.Dropdown(
                                    id = 'campus',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o curso'),
                                dcc.Dropdown(
                                    id = 'curso',
                                    options = curso,
                                    style={'font-size':'12px',}   
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o tipo de curso'),
                                dcc.Dropdown(
                                    id = 'tipo',
                                    options = tipo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o eixo tecnológico'),
                                dcc.Dropdown(
                                    id = 'eixo',
                                    options = eixo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph1')
                ],md=10)
            ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                        dcc.Graph(id = 'graph-matriculas-por-tipo')
                ],md=5),
                dbc.Col([
                        dcc.Graph(id = 'graph-matriculas-por-eixo')
                ],md=5),
            ]),
    ])  
])

@callback(Output('curso','options'),Input('campus','value',),Input('eixo','value'),Input('tipo','value'),)
def filtra_campus(campus=None, eixo=None, tipo=None):
    #matriculas_por_campus=retorna_matriculas_por_campus(ano)
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
    #print(curso)
    return curso

@callback(Output('graph1','figure'),Input('ano_mat_campus','value'),Input('campus','value'),Input('curso','value'),Input('tipo','value'),Input('eixo','value'),)
def grafico_matriculas(ano, campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
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
                
    #print(mat_filtrado)
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = px.treemap(mat_filtrado, 
                     path=[px.Constant('IFPA'),'UNIDADE_DE_ENSINO','NOME_DE_CURSO'],
                     values='MATRICULAS_TOTAL',)
    fig.update_layout(height = 600, width=1200)
    fig.update_traces(hovertemplate = 'Campus: %{parent}<br>Curso: %{label}<br>Matrículas: %{value}')
    return fig


@callback(Output('graph-matriculas-por-tipo','figure'),Input('campus','value'),Input('curso','value'),Input('tipo','value'),Input('eixo','value'),)
def grafico_matriculas_por_tipo(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
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
                
    matriculas_por_tipo_de_curso = mat_filtrado.groupby('TIPO_DE_CURSO')['MATRICULAS_TOTAL'].sum().reset_index().sort_values(by='MATRICULAS_TOTAL')
    #print(matriculas_por_tipo_de_curso) 
    fig2=px.bar(matriculas_por_tipo_de_curso,x='TIPO_DE_CURSO',y='MATRICULAS_TOTAL', color='MATRICULAS_TOTAL', 
            labels = {'MATRICULAS_TOTAL':'Matrículas','TIPO_DE_CURSO':'Tipo de Curso'},text_auto=True)
    fig2.update_layout(
            title={
            'text' : 'Matrículas por Tipo de Curso',
            'x':0.5,
            'xanchor': 'center'
        })                        
    return fig2

@callback(Output('graph-matriculas-por-eixo','figure'),Input('campus','value'),Input('curso','value'),Input('tipo','value'),Input('eixo','value'),)
def grafico_matriculas_por_eixo(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
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
                
    
    matriculas_por_eixo_tecnologico = mat_filtrado.groupby('EIXO_TECNOLOGICO')['MATRICULAS_TOTAL'].sum().reset_index().sort_values(by='MATRICULAS_TOTAL')
    #print(matriculas_por_tipo_de_curso) 
    fig3=px.bar(matriculas_por_eixo_tecnologico,x='EIXO_TECNOLOGICO',y='MATRICULAS_TOTAL', color='MATRICULAS_TOTAL', 
            labels = {'MATRICULAS_TOTAL':'Matrículas','EIXO_TECNOLOGICO':'Eixo Tecnológico'},text_auto=True)
    fig3.update_layout(
            title={
            'text' : 'Matrículas por Eixo Tecnológico',
            'x':0.5,
            'xanchor': 'center'
        }) 
    fig3.update_xaxes(tickangle=45,)                       
    return fig3

