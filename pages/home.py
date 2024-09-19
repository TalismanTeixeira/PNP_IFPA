import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
import pandas as pd

layout = html.Div([
    dbc.Row([
        dbc.Col([
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
                dbc.Col([], md=1),
                dbc.Col([
                    html.Br(),
                    html.Br(),
                    dbc.Col([
                        html.H1('PNP IFPA'),
                    ]),
                    html.Hr(),
                    html.H3('Escolha um painel: ')], md=10),
                dbc.Col([], md=1),
            ], className='linha_verde_menu'),
            dbc.Row([
                dbc.Col([], md=1),
                dbc.Col([
                        dbc.Card([
                             dbc.CardBody(html.A('Matrículas por Campus', href='/matriculas_por_campus')),
                        ], style={'background-color':'rgb(0,100,0)','color':'white','margin-top':'10px','margin-bottom':'10px'}),
                        dbc.Card([
                             dbc.CardBody(html.A('Matrículas por Tipo de Curso e Eixo Tecnólogico', href='/matriculas_por_tipo'),),
                        ],style={'background-color':'rgb(255,255,255)','color':'black','margin-top':'10px','margin-bottom':'10px'}),
                        dbc.Card([
                             dbc.CardBody(html.A('Matrículas Equivalentes por Campus', href='/matriculas_equivalentes_por_campus'),),
                        ],style={'background-color':'rgb(0,100,0)','color':'white','margin-top':'10px','margin-bottom':'10px'}),
                        dbc.Card([
                             dbc.CardBody(html.A('Matrículas Equivalentes por Tipo de Curso e Eixo Tecnólogico', href='/matriculas_equivalentes_por_tipo'),),
                        ],style={'background-color':'rgb(255,255,255)','margin-top':'10px','margin-bottom':'10px'}),
                        dbc.Card([
                             dbc.CardBody(html.A('Eficiência Acadêmica (em manutenção)', href='/eficiencia_academica'),),
                        ],style={'background-color':'rgb(0,100,0)','color':'white','margin-top':'10px','margin-bottom':'10px'}),
                        ],md=5),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(html.A('RAP e RAPP', href='/RAP_RAPP'),),
                    ],style={'background-color':'rgb(0,100,0)','color':'white','margin-top':'10px','margin-bottom':'10px'}),
                    dbc.Card([
                        dbc.CardBody( html.A('Relação Inscritos/Vagas', href='/RIV'),),
                    ],style={'background-color':'rgb(255,255,255)','margin-top':'10px','margin-bottom':'10px'}),
                    dbc.Card([
                        dbc.CardBody(html.A('Taxa de Evasão', href='/evasao'),),
                    ],style={'background-color':'rgb(0,100,0)','color':'white','margin-top':'10px','margin-bottom':'10px'}),
                    dbc.Card([
                        dbc.CardBody(html.A('Taxa de Ocupação', href='/ocupacao'),),
                    ],style={'background-color':'rgb(255,255,255)','margin-top':'10px','margin-bottom':'10px'}),
                    dbc.Card([
                        dbc.CardBody(html.A('Índice de Verticalização', href='/verticalizacao'),),
                    ],style={'background-color':'rgb(0,100,0)','color':'white','margin-top':'10px','margin-bottom':'10px'}),
                ],md=5),
                dbc.Col([], md=1),
            ]),
            dbc.Row([
                dbc.Col([]),
                dbc.Col([]),
                dbc.Col([]),
            ]),
        ])
    ])
])


