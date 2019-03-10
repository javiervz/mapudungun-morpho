import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd

## verbo en espanol a conjugacion en mapudungun
verbos=pd.read_csv('verbs.csv',header=0,sep='\t')
verbos = verbos.sort_values(['esp', 'mapu'], ascending=[1, 0])
verbos_esp=[verbo for verbo in verbos.esp]
verbos_mapu=[verbo for verbo in verbos.mapu]
#verbos={esp:mapu for (esp,mapu) in zip(verbos_esp,verbos_mapu)}
personas={'singular':{'primera':'iñche','segunda':'eymi','tercera':'fey'},'dual':{'primera':'iñchiw','segunda':'eymu','tercera':'feyengu'},'plural':{'primera':'iñchiñ','segunda':'eymün','tercera':'feyengün'}}
consonantes=['n','w']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Label('Elige un verbo de la siguiente lista!',style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.Dropdown(id='input-1-state',
    options=[{'label':key,'value':key} for key in verbos_esp],
    value=verbos_esp[0]
),
    html.Label('Elige el "número"', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.RadioItems(id='input-2-state',
    options=[
        {'label': 'singular', 'value': 'singular'},
        {'label': 'dual', 'value': 'dual'},
        {'label': 'plural', 'value': 'plural'}
    ],
    value='singular'
),
    html.Label('Elige los participantes: ¿qué "persona"?', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.RadioItems(id='input-3-state',
    options=[
        {'label': 'primera', 'value': 'primera'},
        {'label': 'segunda', 'value': 'segunda'},
        {'label': 'tercera', 'value': 'tercera'}
    ],
    value='tercera'
),
    html.Label('¿Es afirmativo o negativo?: elige la "polaridad"', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.RadioItems(id='input-4-state',
    options=[
        {'label': 'positiva', 'value': 'positiva'},
        {'label': 'negativa', 'value': 'negativa'}
    ],
    value='positiva'
),
    html.Label('¿Cuándo ocurrió la acción?', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.RadioItems(id='input-5-state',
    options=[
        {'label': 'no-futuro', 'value': 'no-futuro'},
        {'label': 'futuro', 'value': 'futuro'}
    ],
    value='no-futuro'
),
    html.Button(id='submit-button', n_clicks=0, children='mapudungun mew!'),
    html.Div(id='output-state')
], style={'columnCount': 2})


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value'),
               State('input-5-state', 'value')])
#def update_output(n_clicks, input1, input2, input3, input4, input5):
#    return u'''
#        The Button has been pressed {} times,
#        Input 1 is "{}",
#        Input 2 is "{}"
#        and Input 3 is "{}" and Input 4 is "{}" and Input 5 is "{}"
#    '''.format(input1, input2, input3, input4, input5)

def verb_to_mapudungun(n_clicks, verb_esp,numero,persona,polaridad,tiempo):

    verbos={esp:mapu for (esp,mapu) in zip(verbos_esp,verbos_mapu)}
    base=verbos[verb_esp]
    conjugacion={'singular':{'primera':'(yo) iñche','segunda':'(tú) eymi','tercera':'(ella/él) fey'},'dual':{'primera':'(nosotras/nosotros dos) iñchiw','segunda':'(ustedes dos) eymu','tercera':'(ellas/ellos dos) feyengu'},'plural':{'primera':'(nosotras/nosotros) iñchiñ','segunda':'(ustedes) eymün','tercera':'(ellas/ellos) feyengün'}}

    if polaridad=='positiva':## persona gramatical + base + futuro + polaridad
        if tiempo=='futuro':
            traduccion=conjugacion[numero][persona]+' '+base+'a'
        else:
            traduccion=conjugacion[numero][persona]+' '+base
    elif polaridad=='negativa':
        if tiempo=='futuro':
            traduccion=conjugacion[numero][persona]+' '+base+'la'+'ya'
        else:
            traduccion=conjugacion[numero][persona]+' '+base+'la'




    if base[-1] in consonantes: ## terminan en consonante
        if numero=='singular':
            if persona=='primera':
                traduccion=traduccion+'ün'
            elif persona=='segunda':
                traduccion=traduccion+'imi'
            else:
                traduccion=traduccion+'i'
        elif numero=='dual':
            if persona=='primera':
                traduccion=traduccion+'iyu'
            elif persona=='segunda':
                traduccion=traduccion+'imu'
            else:
                traduccion=traduccion+'ingu'
        else:
            if persona=='primera':
                traduccion=traduccion+'iyiñ'
            elif persona=='segunda':
                traduccion=traduccion+'imün'
            else:
                traduccion=traduccion+'ingün'

    elif base[-1]=='i': ## termina en i
        if numero=='singular':
            if persona=='primera':
                traduccion=traduccion+'n'
            elif persona=='segunda':
                traduccion=traduccion+'mi'
            else:
                traduccion=traduccion
        elif numero=='dual':
            if persona=='primera':
                traduccion=traduccion+'yu'
            elif persona=='segunda':
                traduccion=traduccion+'mu'
            else:
                traduccion=traduccion+'ngu'
        else:
            if persona=='primera':
                traduccion=traduccion+'iñ'
            elif persona=='segunda':
                traduccion=traduccion+'mün'
            else:
                traduccion=traduccion+'ngün'

    else: ## en otro caso
        if numero=='singular':
            if persona=='primera':
                traduccion=traduccion+'n'
            elif persona=='segunda':
                traduccion=traduccion+'ymi'
            else:
                traduccion=traduccion+'y'
        elif numero=='dual':
            if persona=='primera':
                traduccion=traduccion+'yu'
            elif persona=='segunda':
                traduccion=traduccion+'ymu'
            else:
                traduccion=traduccion+'yngu'
        else:
            if persona=='primera':
                traduccion=traduccion+'iñ'
            elif persona=='segunda':
                traduccion=traduccion+'ymün'
            else:
                traduccion=traduccion+'yngün'


    return 'En mapudungun, el verbo "{}" conjugado en "{}" persona "{}" de polaridad "{}" y tiempo "{}" se dice'.format(verb_esp,persona,numero,polaridad,tiempo)+' '+traduccion


#        The Button has been pressed {} times
#        Input 1 is "{}",
#        Input 2 is "{}"
#        and Input 3 is "{}" and Input 4 is "{}" and Input 5 is "{}"
#    '''.format(input1, input2, input3, input4, input5)


if __name__ == '__main__':
    app.run_server(debug=True)
