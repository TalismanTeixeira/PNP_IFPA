import dash
import plotly.graph_objects as go
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd
from pathlib import Path
from dash import callback
import plotly.express as px

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)

pasta_raiz = Path(__file__).parent.parent
#matriculas = pd.read_csv(pasta_raiz / 'data/PDA_PNP_Matriculas.csv')
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',',decimal=',')
matriculas['MATRICULAS_TOTAL'] = matriculas['MATRICULAS_ATENDIDA'].replace('Sim',1)
matriculas['DATA_FIM'] = pd.to_datetime(matriculas['DATA_FIM_PREVISTO_CICLO'],dayfirst=True).dt.year

matriculas_ciclo_eficiencia = matriculas[matriculas['DATA_FIM']==2021]

matriculas_por_campus = matriculas_ciclo_eficiencia.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO','CATEGORIA_SITUACAO'])['MATRICULAS_TOTAL'].sum().reset_index()


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
                    html.H1('Eficiência Acadêmica'),
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
                                    id = 'campus5',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o curso'),
                                dcc.Dropdown(
                                    id = 'curso5',
                                    style={'font-size':'12px',}   
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o tipo de curso'),
                                dcc.Dropdown(
                                    id = 'tipo5',
                                    options = tipo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                html.H5('Escolha o eixo tecnológico'),
                                dcc.Dropdown(
                                    id = 'eixo5',
                                    options = eixo,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dbc.Col([
                        dcc.Graph(id='graph7')
                    ],md=4),
                    dbc.Col([
                        dcc.Graph(id='graph8')
                    ],md=4),
                    dbc.Col([
                        dcc.Graph(id='graph9')
                    ],md=4),
                ],md=10)
            ])
    ])  
])

@callback(Output('curso5','options'),Input('campus5','value',),Input('eixo5','value'),Input('tipo5','value'),)
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

@callback(Output('graph7','figure'),Input('campus5','value'),Input('curso5','value'),Input('tipo5','value'),Input('eixo5','value'),)
def grafico_situacao(campus,curso_escolhido,tipo,eixo):
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
    
    tot_matriculas = mat_filtrado['MATRICULAS_TOTAL'].sum()
    concluintes = mat_filtrado[mat_filtrado['CATEGORIA_SITUACAO']=='Concluintes']['MATRICULAS_TOTAL'].sum()                
    retidos = mat_filtrado[mat_filtrado['CATEGORIA_SITUACAO']=='Em curso']['MATRICULAS_TOTAL'].sum()                
    evadidos = mat_filtrado[mat_filtrado['CATEGORIA_SITUACAO']=='Evadidos']['MATRICULAS_TOTAL'].sum()
    eficiencia = 100*(concluintes+(retidos*concluintes)/(concluintes+evadidos))/tot_matriculas                
    print(tot_matriculas,concluintes,retidos,evadidos)
    resumo=pd.Series([concluintes/tot_matriculas,retidos/tot_matriculas,evadidos/tot_matriculas])
    resumo=resumo*100
    resumo.index = ['Concluintes','Retidos','Evadidos']
    resumo = resumo.to_frame().reset_index()
    resumo.columns=['Situação dos alunos','(%)']    
    print(resumo)


    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    fig = px.bar(resumo,y='(%)', x='Situação dos alunos', color='Situação dos alunos', )
    fig.add_trace(go.Indicator(
        mode = "number+delta",
        value = eficiencia,
        delta = {"reference": 50, "valueformat": ".0f"},
        title = {"text": "Eficiência Acadêmica"},
        domain = {'y': [0.5, 1], 'x': [0.75, 1]}))
    fig.update_layout(height = 600, width=1200, )
    fig.update_layout(showlegend=False)
    fig.update_yaxes(range=[0, 100])

    return fig
