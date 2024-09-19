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

pasta_raiz = Path(__file__).parent.parent
#matriculas = pd.read_csv(pasta_raiz / 'data/PDA_PNP_Matriculas.csv')
matriculas = pd.read_csv(pasta_raiz / 'data/matriculas.csv', sep=',',decimal=',')
servidores = pd.read_csv(pasta_raiz / 'data/servidores_2022.csv', sep=';')
docentes = servidores[servidores['VINCULO_CARREIRA']=='EBTT']

matriculas['MATRICULAS_TOTAL'] = pd.to_numeric(matriculas['MATRICULAS_EQUIVALENTES'].str.replace(',','.'))
matriculas['MATRICULAS_RAP'] = (matriculas['MATRICULAS_TOTAL']*(10/9)).where((matriculas['TIPO_DE_CURSO']=='Licenciatura')|(matriculas['TIPO_DE_CURSO']=='Bacharelado')|(matriculas['TIPO_DE_CURSO']=='Tecnologia'),matriculas['MATRICULAS_TOTAL'])
matriculas_por_campus = matriculas.groupby(['UNIDADE_DE_ENSINO','NOME_DE_CURSO','TIPO_DE_CURSO','EIXO_TECNOLOGICO','MODALIDADE_DE_ENSINO'])['MATRICULAS_RAP'].sum().reset_index()

matriculas_presenciais_por_campus = matriculas_por_campus[matriculas_por_campus['MODALIDADE_DE_ENSINO']=='Educação Presencial']

docentes_por_campus = docentes.groupby(['UNIDADE_LOTACAO','JORNADA_TRABALHO'])['MATRICULA'].count().reset_index()
docentes_por_campus['PROF_EQUIVALENTE'] = (docentes_por_campus['MATRICULA']*0.5).where(docentes_por_campus['JORNADA_TRABALHO']=='20h',docentes_por_campus['MATRICULA'])
docentes_equivalentes_por_campus = docentes_por_campus.groupby('UNIDADE_LOTACAO')['PROF_EQUIVALENTE'].sum().to_frame()
docentes_equivalentes_por_campus=docentes_equivalentes_por_campus.reset_index()
docentes_equivalentes_por_campus['PROF_EQUIVALENTE'] = [78,46,46,20,346,79,56,38,141,73,63,62,54,37,41,40,76,84.5]
#print(docentes_equivalentes_por_campus)


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
                    html.H1('RAP e RAPP'),
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
                                    id = 'campus6',
                                    options = campus,
                                    style={'font-size':'12px',} 
                                    
                        )],md=3),
                        dbc.Col([
                                    
                        ],md=3),
                        dbc.Col([
                                ],md=3),
                        dbc.Col([
                                ],md=3),
                    ])
                ],md=10)
                ]),
            dbc.Row([
                dbc.Col(md=1),
                dbc.Col([
                    dcc.Graph(id='graph_rap')
                ],md=10)
            ])
    ])  
])


@callback(Output('graph_rap','figure'),Input('campus6','value'))
def grafico_matriculas(campus):
    #print(campus,curso_escolhido,tipo, eixo)
    if campus==None:
        mat_filtrado = matriculas_por_campus
        doc_filtrado = docentes_equivalentes_por_campus['PROF_EQUIVALENTE']  
    else:
        mat_filtrado = matriculas_por_campus[matriculas_por_campus['UNIDADE_DE_ENSINO']==campus]
        doc_filtrado = docentes_equivalentes_por_campus[docentes_equivalentes_por_campus['UNIDADE_LOTACAO']==campus]['PROF_EQUIVALENTE']        
    
    #print(mat_filtrado)
    #fig=px.bar(mat_filtrado, x = 'NOME_DE_CURSO',y='MATRICULAS_TOTAL')
    mat_equivalente_rap = mat_filtrado['MATRICULAS_RAP'].sum()
    prof_equivalente_rap = doc_filtrado.sum()
    #print(mat_equivalente_rap, prof_equivalente_rap)
    rap = round((mat_equivalente_rap/prof_equivalente_rap),0)
    
    
    mat_filtrado_presencial = mat_filtrado[mat_filtrado['MODALIDADE_DE_ENSINO']=='Educação Presencial']
    rapp = round(mat_filtrado_presencial['MATRICULAS_RAP'].sum()/doc_filtrado.sum(),0)
    df_rap = pd.DataFrame([rap,rapp])
    df_rap.index=['RAP','RAPP']
    df_rap = df_rap.reset_index()
    df_rap.columns=['Indicador','Valor']    
    
    #print(df_rap)
    fig = px.bar(df_rap,
                x='Indicador',
                y='Valor',
                color='Valor',
                text = 'Valor',
                color_continuous_scale=[(0,"red"),(0.19,"red"),(0.2,"green"), (1,"green"),],
                range_color=[0,100])

    fig.update_layout(height = 600, width=1200)
    fig.update(layout_coloraxis_showscale=False)
    fig.update_traces(hovertemplate = '%{y:.2f}')
    return fig