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
import numpy as np


def modulacao(valor):
    print(valor)
    if valor > 1:
        valor = 1        
    return valor
  

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
server = app.server

pasta_raiz = Path(__file__).parent.parent
#matriculas = pd.read_csv(pasta_raiz / 'data/PDA_PNP_Matriculas.csv')
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',', decimal=',',parse_dates=['DATA_INICIO_CICLO'], dayfirst=True)
matriculas['VAGAS'] = matriculas['VAGAS'].astype(int)
matriculas_neste_ano = matriculas[matriculas['DATA_INICIO_CICLO'].dt.year==2022]
vagas_por_campus = matriculas_neste_ano.groupby(['CODIGO_CICLO_MATRICULA','UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['VAGAS'].first().reset_index()
vagas_por_campus = vagas_por_campus.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO'])['VAGAS'].sum().reset_index()


matriculas['MATRICULAS_TOTAL'] = matriculas['MATRICULAS_ATENDIDA'].replace('Sim',1).infer_objects(copy=False)
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
                    html.H1('Índice de Verticalização'),
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
                                    id = 'campus_IV',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph_IV')
                ],md=7),
                
            ]),
    ])  
])

@callback(Output('graph_IV','figure'),Input('campus_IV','value'))
def grafico_IV(campus):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        vagas_filtrado = vagas_por_campus
    else:
        vagas_filtrado = vagas_por_campus[vagas_por_campus['UNIDADE_DE_ENSINO']==campus]
        
    vagas_por_eixo = vagas_filtrado.groupby(['EIXO_TECNOLOGICO','TIPO_DE_CURSO'])['VAGAS'].sum().reset_index()
    vagas_por_eixo_pivotado = vagas_por_eixo.pivot_table(index='EIXO_TECNOLOGICO',columns='TIPO_DE_CURSO',values='VAGAS')
    vagas_por_eixo_pivotado = vagas_por_eixo_pivotado.fillna(0)
    
    try:
        vagas_por_eixo_pivotado['Graduação'] = vagas_por_eixo_pivotado['Bacharelado']+vagas_por_eixo_pivotado['Licenciatura']+vagas_por_eixo_pivotado['Tecnologia']
    except:
        if 'Bacharelado' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Bacharelado'] = 0
        if 'Licenciatura' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Licenciatura'] = 0
        if 'Tecnologia' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Tecnologia'] = 0
        vagas_por_eixo_pivotado['Graduação'] = vagas_por_eixo_pivotado['Bacharelado']+vagas_por_eixo_pivotado['Licenciatura']+vagas_por_eixo_pivotado['Tecnologia']
    
    try:
        vagas_por_eixo_pivotado['Pós-Graduação'] = vagas_por_eixo_pivotado['Especialização (Lato Sensu)']+vagas_por_eixo_pivotado['Mestrado Profissional']+vagas_por_eixo_pivotado['Doutorado']
    except:
        if 'Mestrado Profissional' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Mestrado Profissional'] = 0
        if 'Especialização (Lato Sensu)' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Especialização (Lato Sensu)'] = 0
        if 'Doutorado' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Doutorado'] = 0
        vagas_por_eixo_pivotado['Pós-Graduação'] = vagas_por_eixo_pivotado['Especialização (Lato Sensu)']+vagas_por_eixo_pivotado['Mestrado Profissional']+vagas_por_eixo_pivotado['Doutorado']        
    #print(vagas_por_eixo_pivotado.info())

    try:
        Relacao_FIC_Tecnico = (vagas_por_eixo_pivotado['Qualificação Profissional (FIC)']/vagas_por_eixo_pivotado['Técnico']).to_frame()
    except:
        if 'Qualificação Profissional (FIC)' not in vagas_por_eixo_pivotado.columns:
            vagas_por_eixo_pivotado['Qualificação Profissional (FIC)'] = 0
            Relacao_FIC_Tecnico = (vagas_por_eixo_pivotado['Qualificação Profissional (FIC)']/vagas_por_eixo_pivotado['Técnico']).to_frame()

    Relacao_Tecnico_Graduacao = vagas_por_eixo_pivotado['Técnico']/vagas_por_eixo_pivotado['Graduação']
    Relacao_Graduacao_Pos = vagas_por_eixo_pivotado['Graduação']/vagas_por_eixo_pivotado['Pós-Graduação']
    Relacao_Tecnico_Pos = vagas_por_eixo_pivotado['Técnico']/vagas_por_eixo_pivotado['Pós-Graduação']
    Relacao_FIC_Graduacao = vagas_por_eixo_pivotado['Qualificação Profissional (FIC)']/vagas_por_eixo_pivotado['Graduação']
    Relacao_FIC_Pos = vagas_por_eixo_pivotado['Qualificação Profissional (FIC)']/vagas_por_eixo_pivotado['Pós-Graduação']
    #print(vagas_por_eixo_pivotado.loc['Informação e Comunicação'])    
    IV=Relacao_FIC_Tecnico
    IV.columns=['Relação FIC Técnico']
    IV['Relação Técnico Graduação'] = Relacao_Tecnico_Graduacao
    IV['Relação Graduação Pós-Graduação'] = Relacao_Graduacao_Pos
    IV['Relação Técnico Pós-Graduação'] = Relacao_Tecnico_Pos
    IV['Relação FIC Graduação'] = Relacao_FIC_Graduacao
    IV['Relação FIC Pós-Graduação'] = Relacao_FIC_Pos
    
    IV = IV.replace(np.inf,0)
    IV = IV.fillna(0)
    #print(IV.loc['Informação e Comunicação'])


    IV = IV.map(lambda x: 1 if x > 1 else x)
    IV = IV.fillna(0)
    IV['Indicador'] = IV['Relação FIC Técnico']*0.397 + IV['Relação Técnico Graduação']*0.365 + IV['Relação Graduação Pós-Graduação']*0.095 + IV['Relação Técnico Pós-Graduação']*0.089 + IV['Relação FIC Graduação']*0.028 + IV['Relação FIC Pós-Graduação']*0.026
    IV['Indicador'] = round(IV['Indicador']*100,0)
    IV = IV.sort_values(by='Indicador')
    

    fig=go.Figure()
    fig=px.bar(IV, x = IV.index,y='Indicador', color='Indicador',text_auto=True)
    fig.update_layout(height = 600, width=1000, xaxis_title='Eixo Tecnológico', yaxis_title='Índice de Verticalização')
    #fig.add_annotation(x=0.4,y=1.1, text='TOP 10 Cursos com maior IV', showarrow=False, font=dict(size=18))
    return fig

