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
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',',decimal=',',parse_dates=['DATA_INICIO_CICLO'], dayfirst=True)

matriculas_neste_ano = matriculas[matriculas['DATA_INICIO_CICLO'].dt.year==2022]
matriculas_neste_ano['TOTAL_INSCRITOS'] = matriculas_neste_ano['TOTAL_INSCRITOS'].astype(float) 
print(matriculas_neste_ano.info())
vagas_por_campus = matriculas_neste_ano.groupby(['CODIGO_CICLO_MATRICULA','UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['VAGAS'].first().reset_index()
inscritos_por_campus = matriculas_neste_ano.groupby(['CODIGO_CICLO_MATRICULA','UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['TOTAL_INSCRITOS'].first().reset_index()

vagas_por_campus = vagas_por_campus.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['VAGAS'].sum().reset_index()
inscritos_por_campus = inscritos_por_campus.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['TOTAL_INSCRITOS'].sum().reset_index()


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
                    html.H1('Relação Inscritos / Vagas'),
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
                                    id = 'campus_RIV',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o curso'),
                                dcc.Dropdown(
                                    id = 'curso_RIV',
                                    style={'font-size':'12px',}   
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o tipo de curso'),
                                dcc.Dropdown(
                                    id = 'tipo_RIV',
                                    options = tipo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o eixo tecnológico'),
                                dcc.Dropdown(
                                    id = 'eixo_RIV',
                                    options = eixo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph_RIV')
                ],md=7),
                dbc.Col([
                    dcc.Graph(id='graph_Indicator')
                ],md=3),
            ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                        dcc.Graph(id = 'graph-riv-por-tipo')
                ],md=5),
                dbc.Col([
                        dcc.Graph(id = 'graph-riv-por-eixo')
                ],md=5),
            ]),
    ])  
])

@callback(Output('curso_RIV','options'),Input('campus_RIV','value',),Input('eixo_RIV','value'),Input('tipo_RIV','value'),)
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

@callback(Output('graph_RIV','figure'),Input('campus_RIV','value'),Input('curso_RIV','value'),Input('tipo_RIV','value'),Input('eixo_RIV','value'),)
def grafico_RIV(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[inscritos_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    #print(mat_filtrado)
    #print(vagas_filtrado)
    resumo_inscritos = inscritos_filtrado['TOTAL_INSCRITOS'].sum()
    resumo_vagas = vagas_filtrado['VAGAS'].sum()
    riv = round(resumo_inscritos/resumo_vagas,2)
    riv_todos = round(inscritos_filtrado['TOTAL_INSCRITOS']/vagas_filtrado['VAGAS'],2)
    inscritos_filtrado['RIV'] = riv_todos
    riv_top_10 = inscritos_filtrado.sort_values(by='RIV', ascending=False).head(10)
    riv_top_10=riv_top_10[['NOME_DE_CURSO','UNIDADE_DE_ENSINO','RIV',]]
    #print(riv_top_10)
    headerColor = 'grey'
    rowEvenColor = 'lightgrey'
    rowOddColor = 'white'
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = go.Figure(data = go.Table(
        header=dict(values=['Curso','Campus','RIV'],align='left',fill_color=headerColor,font=dict(color='white', size=12)), 
        cells = dict(values=[riv_top_10['NOME_DE_CURSO'], riv_top_10['UNIDADE_DE_ENSINO'],riv_top_10['RIV']],align='left',fill_color = [[rowOddColor,rowEvenColor]*5],),
    ))
    fig.update_layout(height = 600, width=1000)
    fig.add_annotation(x=0.4,y=1.1, text='TOP 10 Cursos com maior RIV', showarrow=False, font=dict(size=18))
    return fig


@callback(Output('graph_Indicator','figure'),Input('campus_RIV','value'),Input('curso_RIV','value'),Input('tipo_RIV','value'),Input('eixo_RIV','value'),)
def grafico_RIV(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[inscritos_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    #print(mat_filtrado)
    #print(vagas_filtrado)
    resumo_inscritos = inscritos_filtrado['TOTAL_INSCRITOS'].sum()
    resumo_vagas = vagas_filtrado['VAGAS'].sum()
    riv = round(resumo_inscritos/resumo_vagas,2)
    #print(riv_top_10)
    
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "number+gauge",
        value = riv,

        delta = {"reference": 50, "valueformat": ".0f"},title = {"text": "RIV"},
        domain = {'y': [0,1], 'x': [0, 1]}))
    #fig.update_layout(height = 600, width=1200)
    return fig


@callback(Output('graph-riv-por-tipo','figure'),Input('campus_RIV','value'),Input('curso_RIV','value'),Input('tipo_RIV','value'),Input('eixo_RIV','value'),)
def grafico_RIV_por_tipo(campus,curso_escolhido,tipo,eixo):
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[inscritos_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    inscritos_por_tipo = inscritos_filtrado.groupby('TIPO_DE_CURSO')['TOTAL_INSCRITOS'].sum().reset_index()
    vagas_por_tipo = vagas_filtrado.groupby('TIPO_DE_CURSO')['VAGAS'].sum().reset_index()
    #print(vagas_por_tipo.head(2))
        
    riv_por_tipo = round(inscritos_por_tipo['TOTAL_INSCRITOS']/vagas_por_tipo['VAGAS'],2).to_frame()
    riv_por_tipo.columns=['RIV']
    #print(riv_por_tipo.columns)
    resumo_riv_por_tipo = pd.concat([inscritos_por_tipo,riv_por_tipo],axis=1).sort_values(by='RIV')
    
    #print(resumo_riv_por_tipo.columns)

    fig=px.bar(resumo_riv_por_tipo,x='TIPO_DE_CURSO',y='RIV', color='RIV', 
            labels = {'RIV':'Relação Inscritos/Vagas','TIPO_DE_CURSO':'Tipo de Curso'},text_auto=True)
    fig.update_layout(
            title={
            'text' : 'RIV por Tipo de Curso',
            'x':0.5,
            'xanchor': 'center'
        })                        
    return fig

@callback(Output('graph-riv-por-eixo','figure'),Input('campus_RIV','value'),Input('curso_RIV','value'),Input('tipo_RIV','value'),Input('eixo_RIV','value'),)
def grafico_RIV_por_eixo(campus,curso_escolhido,tipo,eixo):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus
                    vagas_filtrado = vagas_por_campus
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
    else:
        if eixo==None:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[inscritos_por_campus['UNIDADE_DE_ENSINO']==campus]
                    vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]
        else:
            if tipo==None:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
            else:
                if curso_escolhido==None:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)]
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)]
                else:
                    inscritos_filtrado = inscritos_por_campus[(inscritos_por_campus['UNIDADE_DE_ENSINO']==campus)&(inscritos_por_campus['EIXO_TECNOLOGICO']==eixo)&(inscritos_por_campus['TIPO_DE_CURSO']==tipo)&(inscritos_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                    vagas_filtrado = vagas_por_campus[(vagas_por_campus['UNIDADE_DE_ENSINO']==campus)&(vagas_por_campus['EIXO_TECNOLOGICO']==eixo)&(vagas_por_campus['TIPO_DE_CURSO']==tipo)&(vagas_por_campus['NOME_DE_CURSO']==curso_escolhido)]            
                
    
    inscritos_por_tipo = inscritos_filtrado.groupby('EIXO_TECNOLOGICO')['TOTAL_INSCRITOS'].sum().reset_index()
    vagas_por_tipo = vagas_filtrado.groupby('EIXO_TECNOLOGICO')['VAGAS'].sum().reset_index()
    #print(vagas_por_tipo.head(2))
    #print(inscritos_por_tipo['TOTAL_INSCRITOS'].value_counts())        
    riv_por_tipo = round(inscritos_por_tipo['TOTAL_INSCRITOS']/vagas_por_tipo['VAGAS'],2).to_frame()
    riv_por_tipo.columns=['RIV']
    #print(riv_por_tipo.columns)
    resumo_riv_por_tipo = pd.concat([inscritos_por_tipo,riv_por_tipo],axis=1).sort_values(by='RIV')
    
    #print(resumo_riv_por_tipo.columns)

    fig=px.bar(resumo_riv_por_tipo,x='EIXO_TECNOLOGICO',y='RIV', color='RIV', 
            labels = {'RIV':'Relação Inscritos/Vagas','EIXO_TECNOLOGICO':'Eixo Tecnológico'},text_auto=True)
    fig.update_layout(
            title={
            'text' : 'RIV por Eixo Tecnológico',
            'x':0.5,
            'xanchor': 'center'
        })    
    fig.update_xaxes(tickangle=45,)                     
    return fig
