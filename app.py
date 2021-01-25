import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import dash_table
import os

data = pd.read_excel('data/Concentrado_24_enero.xlsx')
data.columns = data.columns.str.lower()

materias_full = data.materia.unique()
docentes_full = data.docente.unique()

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

app.layout = html.Div([
    html.Div([
            html.Div([
                html.Img(src='assets/logoFISMAT.jpg',
                         style={'width': 500, 'height': 100})
            ],
                className='six columns'),
            html.Div([
                html.H2('Consulta de horarios para asesoría',
                        style={'color': '#dc4b4a'})
            ],
                className='six columns')
        ], className='row'),
    html.Div([
        html.H5('Selecciona tu materia'),
        dcc.Dropdown(
            id='selector_materia',
            options=[
                {'label': materia, 'value': materia}
                for materia in materias_full
            ],
            placeholder='Selecciona aquí tu materia'
        ),
        dash_table.DataTable(
            id='tabla_asesores',
            page_action='none',
            style_table={'overflowX': 'auto', 'overflowY': 'auto', 'height': '500px'},
            style_header={
                'backgroundColor': '#c5beb5',
                'fontWeight': 'bold',
                'color': 'white'
            },
            style_cell_conditional=[
                {
                    'if': {'column_id': 'id/correo'},
                    'textAlign': 'left'
                },
                {
                    'if': {
                        'filter_query': '{disponibilidad} = "Disponible"',
                        'column_id': 'disponibilidad'
                    },
                    'backgroundColor': '#76dd4b'
                },
                {
                    'if': {
                        'filter_query': '{disponibilidad} = "No disponible"',
                        'column_id': 'disponibilidad'
                    },
                    'backgroundColor': '#db4b4b',
                    'color': 'white'
                }
            ],
            sort_action='native',
            sort_mode='multi',
            columns=[{'name': col, 'id': col} for col in data.iloc[:, 1:7].columns],
            data=data.iloc[:, 1:7].to_dict('records')
        )
    ])
])

@app.callback(
    Output('tabla_asesores', 'columns'),
    Output('tabla_asesores', 'data'),
    Input('selector_materia', 'value')
)
def update_table(selector_materia):
    if selector_materia is None:
        filtered_data = data.iloc[:, 1:7]
    else:
        filtered_data = data[data.materia == selector_materia].iloc[:, 1:7]
    columns = [{'name': col, 'id': col} for col in filtered_data.columns]
    return columns, filtered_data.to_dict('records')



if __name__ == '__main__':
    app.run_server(debug=True)
