import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
from pathlib import Path
from dash import callback
import plotly.express as px
import plotly.graph_objects as go
from numpy import inf
import warnings
warnings.filterwarnings("ignore")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

pasta_raiz = Path(__file__).parent.parent
#matriculas = pd.read_csv(pasta_raiz / 'data/PDA_PNP_Matriculas.csv')
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',', decimal = ',' ,parse_dates=['DATA_INICIO_CICLO'], dayfirst=True)
#matriculas['VAGAS'] = matriculas['VAGAS'].str.replace(',','.').astype(int)
matriculas = matriculas[matriculas['TIPO_DE_CURSO'] != 'Qualificação Profissional (FIC)']
vagas_por_campus = matriculas.groupby(['CODIGO_CICLO_MATRICULA','UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['VAGAS'].first().reset_index()
#vagas_teste = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']=='Campus Abaetetuba')&(vagas_por_campus['NOME_DE_CURSO']=='Técnico em Meio Ambiente')]
#print(vagas_teste)
vagas_por_campus = vagas_por_campus.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['VAGAS'].sum().reset_index()



matriculas['MATRICULAS_TOTAL'] = matriculas['MATRICULAS_ATENDIDA'].replace('Sim',1)
matriculas_por_campus = matriculas.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['MATRICULAS_TOTAL'].sum().reset_index()

campus = matriculas_por_campus['UNIDADE_DE_ENSINO'].unique()
#items_campus = [dbc.DropdownMenuItem(x) for x in campus]
curso = matriculas_por_campus['NOME_DE_CURSO'].unique()
#items_curso = [dbc.DropdownMenuItem(x) for x in curso]
tipo = matriculas_por_campus['TIPO_DE_CURSO'].unique()
#items_tipo = [dbc.DropdownMenuItem(x) for x in tipo]
eixo = matriculas_por_campus['EIXO_TECNOLOGICO'].unique()
#items_eixo = [dbc.DropdownMenuItem(x) for x in eixo]

#print(curso)

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
                    html.H1('Taxa de Ocupação'),
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
                                    id = 'campus_ocupacao',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o curso'),
                                dcc.Dropdown(
                                    id = 'curso_ocupacao',
                                    style={'font-size':'12px',}   
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o tipo de curso'),
                                dcc.Dropdown(
                                    id = 'tipo_ocupacao',
                                    options = tipo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o eixo tecnológico'),
                                dcc.Dropdown(
                                    id = 'eixo_ocupacao',
                                    options = eixo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph_ocupacao')
                ],md=7),
                dbc.Col([
                    dcc.Graph(id='graph_Indicator_ocupacao')
                ],md=3),
            ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                        dcc.Graph(id = 'graph-ocupacao-por-tipo')
                ],md=5),
                dbc.Col([
                        dcc.Graph(id = 'graph-ocupacao-por-eixo')
                ],md=5),
            ]),
    ])  
])

@callback(Output('curso_ocupacao','options'),Input('campus_ocupacao','value',),Input('eixo_ocupacao','value'),Input('tipo_ocupacao','value'),)
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
    #print(curso)
    return curso

@callback(Output('graph_ocupacao','figure'),Input('campus_ocupacao','value'),Input('curso_ocupacao','value'),Input('tipo_ocupacao','value'),Input('eixo_ocupacao','value'),)
def tabela_ocupacao(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
    #print(mat_filtrado.columns)            
    ocupacao_todos = round(100*mat_filtrado['MATRICULAS_TOTAL']/vagas_filtrado['VAGAS'],2)
    ocupacao_todos[ocupacao_todos==inf] = 0
    mat_filtrado['OCUPACAO'] = ocupacao_todos
    
    ocupacao_top_10 = mat_filtrado.sort_values(by='OCUPACAO', ascending=False).head(10)
    ocupacao_top_10=ocupacao_top_10[['NOME_DE_CURSO','UNIDADE_DE_ENSINO','OCUPACAO','MATRICULAS_TOTAL']]
    
    vagas_filtrado['OCUPACAO'] = ocupacao_todos
    vagas_top_10 = vagas_filtrado.sort_values(by='OCUPACAO', ascending=False).head(10)
    vagas_top_10=vagas_top_10[['NOME_DE_CURSO','UNIDADE_DE_ENSINO','OCUPACAO','VAGAS']]

    #print(ocupacao_top_10,vagas_top_10)


    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = go.Figure(data = go.Table(
        header=dict(values=['Curso','Campus','Taxa de Ocupação (%)'],align='left',fill_color=headerColor,font=dict(color='white', size=12)), 
        cells = dict(values=[ocupacao_top_10['NOME_DE_CURSO'], ocupacao_top_10['UNIDADE_DE_ENSINO'],ocupacao_top_10['OCUPACAO']],align='left',fill_color = [[rowOddColor,rowEvenColor]*5],),
    ))
    fig.update_layout(height = 600, width=1000)
    fig.add_annotation(x=0.4,y=1.1, text='TOP 10 Cursos com maior Taxa de Ocupação', showarrow=False, font=dict(size=18))
    return fig


@callback(Output('graph_Indicator_ocupacao','figure'),Input('campus_ocupacao','value'),Input('curso_ocupacao','value'),Input('tipo_ocupacao','value'),Input('eixo_ocupacao','value'),)
def grafico_indicador_ocupacao(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    #print(mat_filtrado)
    #print(vagas_filtrado)
    resumo_matriculas = mat_filtrado['MATRICULAS_TOTAL'].sum()
    resumo_vagas = vagas_filtrado['VAGAS'].sum()
    ocupacao = round(100*resumo_matriculas/resumo_vagas,2)
    #print(ocupacao_top_10)
    
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+gauge",
        value = ocupacao,

        delta = {"reference": 50, "valueformat": ".0f"},title = {"text": "Taxa de Ocupação (%)"},
        domain = {'y': [0,1], 'x': [0, 1]}))
    #fig.update_layout(height = 600, width=1200)
    return fig


@callback(Output('graph-ocupacao-por-tipo','figure'),Input('campus_ocupacao','value'),Input('curso_ocupacao','value'),Input('tipo_ocupacao','value'),Input('eixo_ocupacao','value'),)
def grafico_ocupacao_por_tipo(campus,curso_escolhido,tipo,eixo):
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    matriculas_por_tipo = mat_filtrado.groupby('TIPO_DE_CURSO')['MATRICULAS_TOTAL'].sum().reset_index()
    vagas_por_tipo = vagas_filtrado.groupby('TIPO_DE_CURSO')['VAGAS'].sum().reset_index()
    #print(vagas_por_tipo.head(2))
        
    ocupacao_por_tipo = round(100*matriculas_por_tipo['MATRICULAS_TOTAL']/vagas_por_tipo['VAGAS'],2).to_frame()
    ocupacao_por_tipo.columns=['OCUPACAO']
    #print(riv_por_tipo.columns)
    resumo_ocupacao_por_tipo = pd.concat([matriculas_por_tipo,ocupacao_por_tipo],axis=1).sort_values(by='OCUPACAO')
    
    #print(resumo_riv_por_tipo.columns)

    fig=px.bar(resumo_ocupacao_por_tipo,x='TIPO_DE_CURSO',y='OCUPACAO', color='OCUPACAO', 
            labels = {'OCUPACAO':'Taxa de Ocupação (%)','TIPO_DE_CURSO':'Tipo de Curso'},text_auto=True)
    fig.update_layout(
            title={
            'text' : 'Taxa de Ocupação por Tipo de Curso',
            'x':0.5,
            'xanchor': 'center'
        })                        
    return fig

@callback(Output('graph-ocupacao-por-eixo','figure'),Input('campus_ocupacao','value'),Input('curso_ocupacao','value'),Input('tipo_ocupacao','value'),Input('eixo_ocupacao','value'),)
def grafico_ocupacao_por_eixo(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    
    matriculas_por_eixo = mat_filtrado.groupby('EIXO_TECNOLOGICO')['MATRICULAS_TOTAL'].sum().reset_index()
    vagas_por_eixo = vagas_filtrado.groupby('EIXO_TECNOLOGICO')['VAGAS'].sum().reset_index()
    #print(vagas_por_tipo.head(2))
        
    ocupacao_por_eixo = round(100*matriculas_por_eixo['MATRICULAS_TOTAL']/vagas_por_eixo['VAGAS'],2).to_frame()
    ocupacao_por_eixo.columns=['OCUPACAO']
    #print(ocupacao_por_tipo.columns)
    resumo_ocupacao_por_eixo = pd.concat([matriculas_por_eixo,ocupacao_por_eixo],axis=1).sort_values(by='OCUPACAO')
    
    #print(resumo_ocupacao_por_tipo.columns)

    fig=px.bar(resumo_ocupacao_por_eixo,x='EIXO_TECNOLOGICO',y='OCUPACAO', color='OCUPACAO', 
            labels = {'OCUPACAO':'Taxa de Ocupação (%)','EIXO_TECNOLOGICO':'Eixo Tecnológico'},text_auto=True)
    fig.update_layout(
            title={
            'text' : 'Taxa de Ocupação por Eixo Tecnológico',
            'x':0.5,
            'xanchor': 'center'
        })    
    fig.update_xaxes(tickangle=45,)                     
    return fig
