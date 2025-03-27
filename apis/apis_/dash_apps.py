def declare_dash_app():
    from dash import dcc, html
    from dash.dependencies import Input, Output
    from django_plotly_dash import DjangoDash

    # Crear la aplicación Dash
    app = DjangoDash('dashb')  # Nombre único para la app Dash

    app.layout = html.Div(children=[
        html.H1(children='Dashboard en Django'),
        
        dcc.Dropdown(
            id='dropdown',
            options=[
                {'label': 'Opción 1', 'value': '1'},
                {'label': 'Opción 2', 'value': '2'},
            ],
            value='1'
        ),
        
        html.Div(id='output-div')
    ])

    @app.callback(
        Output('output-div', 'children'),
        [Input('dropdown', 'value')]
    )
    def update_output(value):
        return f'Seleccionaste la opción {value}'