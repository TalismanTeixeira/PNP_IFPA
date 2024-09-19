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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

pasta_raiz = Path(__file__).parent.parent
#matriculas = pd.read_csv(pasta_raiz / 'data/PDA_PNP_Matriculas.csv')
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',',decimal=',',parse_dates=['DATA_INICIO_CICLO'], dayfirst=True)

matriculas['MATRICULAS_TOTAL'] = matriculas['MATRICULAS_ATENDIDA'].replace('Sim',1)
matriculas_por_campus = matriculas.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO','CATEGORIA_SITUACAO'])['MATRICULAS_TOTAL'].sum().reset_index()
#print(matriculas_por_campus)

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
                    html.H1('Taxa de Evasão'),
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
                                    id = 'campus_evasao',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o curso'),
                                dcc.Dropdown(
                                    id = 'curso_evasao',
                                    style={'font-size':'12px',}   
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o tipo de curso'),
                                dcc.Dropdown(
                                    id = 'tipo_evasao',
                                    options = tipo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o eixo tecnológico'),
                                dcc.Dropdown(
                                    id = 'eixo_evasao',
                                    options = eixo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph_evasao')
                ],md=7),
                dbc.Col([
                    dcc.Graph(id='graph_Indicator_evasao')
                ],md=3),
            ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                        dcc.Graph(id = 'graph-evasao-por-tipo')
                ],md=5),
                dbc.Col([
                        dcc.Graph(id = 'graph-evasao-por-eixo')
                ],md=5),
            ]),
    ])  
])

@callback(Output('curso_evasao','options'),Input('campus_evasao','value',),Input('eixo_evasao','value'),Input('tipo_evasao','value'),)
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

@callback(Output('graph_evasao','figure'),Input('campus_evasao','value'),Input('curso_evasao','value'),Input('tipo_evasao','value'),Input('eixo_evasao','value'),)
def grafico_evasao(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    #evadidos_filtrado = evadidos_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    #evadidos_filtrado = evadidos_por_campus[evadidos_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    #print(mat_filtrado)
    #print(evadidos_filtrado)
    #print(mat_filtrado)
    
    total_alunos = mat_filtrado.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO'])['MATRICULAS_TOTAL'].sum().reset_index()
    #print(total_alunos)
    mat_pivotado = mat_filtrado.pivot(index=['UNIDADE_DE_ENSINO','NOME_DE_CURSO'],columns='CATEGORIA_SITUACAO', values='MATRICULAS_TOTAL').reset_index()
    #print(mat_pivotado)
    #print(total_evadidos)
    try:
        total_evadidos = mat_pivotado.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO'])['Evadidos'].sum().reset_index()
        evasao_todos = round(100*total_evadidos['Evadidos']/total_alunos['MATRICULAS_TOTAL'],2)
    except:
        return go.Figure()
    #print(evasao_todos)
    
    total_alunos['evasao'] = evasao_todos
    evasao_top_10 = total_alunos.sort_values(by='evasao', ascending=False).head(10)
    evasao_top_10=evasao_top_10[['NOME_DE_CURSO','UNIDADE_DE_ENSINO','evasao',]]
    #print(evasao_top_10)
    
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    #fig=go.Figure()
    fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = go.Figure(data = go.Table(
        header=dict(values=['Curso','Campus','Evasão (%)'],align='left',fill_color=headerColor,font=dict(color='white', size=12)), 
        cells = dict(values=[evasao_top_10['NOME_DE_CURSO'], evasao_top_10['UNIDADE_DE_ENSINO'],evasao_top_10['evasao']],align='left',fill_color = [[rowOddColor,rowEvenColor]*5],),
    ))
    fig.update_layout(height = 600, width=1000)
    fig.add_annotation(x=0.4,y=1.1, text='TOP 10 Cursos com maior Evasão', showarrow=False, font=dict(size=18))
    return fig


@callback(Output('graph_Indicator_evasao','figure'),Input('campus_evasao','value'),Input('curso_evasao','value'),Input('tipo_evasao','value'),Input('eixo_evasao','value'),)
def grafico_evasao(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    #evadidos_filtrado = evadidos_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    #evadidos_filtrado = evadidos_por_campus[evadidos_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    #print(mat_filtrado)
    #print(evadidos_filtrado)
    total_alunos = mat_filtrado.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO'])['MATRICULAS_TOTAL'].sum().reset_index()
    resumo_alunos = total_alunos['MATRICULAS_TOTAL'].sum()
    #print(resumo_alunos)
    mat_pivotado = mat_filtrado.pivot(index=['UNIDADE_DE_ENSINO','NOME_DE_CURSO'],columns='CATEGORIA_SITUACAO', values='MATRICULAS_TOTAL').reset_index()
    #print(mat_pivotado)
    try:
        total_evadidos = mat_pivotado.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO'])['Evadidos'].sum().reset_index()
        resumo_evadidos = total_evadidos['Evadidos'].sum()
        evasao = round(100*resumo_evadidos/resumo_alunos,2)
    except:
        return go.Figure()
    #print(total_evadidos)
    #print(evasao_todos)
        
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+gauge",
        value = evasao,
        delta = {"reference": 50, "valueformat": ".0f"},title = {"text": "Evasão (%)"},
        domain = {'y': [0.5,1], 'x': [0, 1]}))
    fig.update_layout(height = 600, width=400)
    return fig

@callback(Output('graph-evasao-por-tipo','figure'),Input('campus_evasao','value'),Input('curso_evasao','value'),Input('tipo_evasao','value'),Input('eixo_evasao','value'),)
def grafico_evasao_por_tipo(campus,curso_escolhido,tipo,eixo):
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    #evadidos_filtrado = evadidos_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    #evadidos_filtrado = evadidos_por_campus[evadidos_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    total_alunos = mat_filtrado.groupby('TIPO_DE_CURSO')['MATRICULAS_TOTAL'].sum().reset_index()
    
    #print(total_alunos.head(2))
    mat_filtrado_por_tipo = mat_filtrado.groupby(['TIPO_DE_CURSO','CATEGORIA_SITUACAO'])['MATRICULAS_TOTAL'].sum().reset_index()
    mat_pivotado = mat_filtrado_por_tipo.pivot(index=['TIPO_DE_CURSO'],columns='CATEGORIA_SITUACAO', values='MATRICULAS_TOTAL').reset_index()
    #print(mat_pivotado.head(2))
    try:
        evasao = round(100*mat_pivotado['Evadidos']/total_alunos['MATRICULAS_TOTAL'],2)
    except:
        return go.Figure()
    #print(evasao.head(2))
    evasao_por_tipo = pd.concat([total_alunos,evasao],axis=1)
    evasao_por_tipo.columns=['TIPO_DE_CURSO','MATRICULAS_TOTAL','EVASAO']
    evasao_por_tipo = evasao_por_tipo.fillna(0)
    evasao_por_tipo = evasao_por_tipo.sort_values(by='EVASAO')
    
    #print(evasao_por_tipo)
    
    fig=px.bar(evasao_por_tipo,x='TIPO_DE_CURSO',y='EVASAO', color='EVASAO', 
            labels = {'EVASAO':'Taxa de Evasão','TIPO_DE_CURSO':'Tipo de Curso'},text_auto=True)
    fig.update_layout(
            title={
            'text' : 'Taxa de Evasão por Tipo de Curso',
            'x':0.5,
            'xanchor': 'center'
        })                        
    return fig

@callback(Output('graph-evasao-por-eixo','figure'),Input('campus_evasao','value'),Input('curso_evasao','value'),Input('tipo_evasao','value'),Input('eixo_evasao','value'),)
def grafico_RIV_por_eixo(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus
                    #evadidos_filtrado = evadidos_por_campus
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
                    #evadidos_filtrado = evadidos_por_campus[evadidos_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)]
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    mat_filtrado = matriculas_por_campus[(matriculas_por_campus['UNIDADE_DE_ENSINO']==campus)&(matriculas_por_campus['EIXO_TECNOLOGICO']==eixo)&(matriculas_por_campus['TIPO_DE_CURSO']==tipo)&(matriculas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    #evadidos_filtrado = evadidos_por_campus[(evadidos_por_campus['UNIDADE_DE_ENSINO']==campus)&(evadidos_por_campus['EIXO_TECNOLOGICO']==eixo)&(evadidos_por_campus['TIPO_DE_CURSO']==tipo)&(evadidos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
            
    total_alunos = mat_filtrado.groupby('EIXO_TECNOLOGICO')['MATRICULAS_TOTAL'].sum().reset_index()
    
    #print(total_alunos)
    mat_filtrado_por_eixo = mat_filtrado.groupby(['EIXO_TECNOLOGICO','CATEGORIA_SITUACAO'])['MATRICULAS_TOTAL'].sum().reset_index()
    mat_pivotado = mat_filtrado_por_eixo.pivot(index=['EIXO_TECNOLOGICO'],columns='CATEGORIA_SITUACAO', values='MATRICULAS_TOTAL').reset_index()
    #print(mat_pivotado)
    try:
        evasao = round(100*mat_pivotado['Evadidos']/total_alunos['MATRICULAS_TOTAL'],2)
    except:
        return go.Figure()
    #print(total_evadidos)
    evasao_por_eixo = pd.concat([total_alunos,evasao],axis=1)
    evasao_por_eixo.columns=['EIXO_TECNOLOGICO','MATRICULAS_TOTAL','EVASAO']
    evasao_por_eixo = evasao_por_eixo.fillna(0)
    evasao_por_eixo = evasao_por_eixo.sort_values(by='EVASAO')
    
    #print(evasao_por_tipo)
    
    fig=px.bar(evasao_por_eixo,x='EIXO_TECNOLOGICO',y='EVASAO', color='EVASAO', 
            labels = {'EVASAO':'Taxa de Evasão','EIXO_TECNOLOGICO':'Eixo Tecnológico'},text_auto=True)
    fig.update_layout(
            title={
            'text' : 'Taxa de Evasão por Eixo Tecnológico',
            'x':0.5,
            'xanchor': 'center'
        })                        
    
    fig.update_xaxes(tickangle=45,)                     
    return fig
