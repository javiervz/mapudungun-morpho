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
    html.Label('¿Cuántas personas realizan la acción?: elige el "número"', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.RadioItems(id='input-2-state',
    options=[
        {'label': 'singular', 'value': 'singular'},
        {'label': 'dual', 'value': 'dual'},
        {'label': 'plural', 'value': 'plural'}
    ],
    value='singular'
),
    html.Label('¿Quiénes participan?: elige la "persona"', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
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
    html.Label('¿Cuándo ocurrió la acción?: elige el "tiempo"', style={'color': 'black', 'fontSize': 18, 'font-weight': 'bold'}),
    dcc.RadioItems(id='input-5-state',
    options=[
        {'label': 'no-futuro', 'value': 'no-futuro'},
        {'label': 'futuro', 'value': 'futuro'}
    ],
    value='no-futuro'
),
    html.Button(id='submit-button', n_clicks=0, children='mapudungun mew!'),
    html.Div(id='output-state'),
    html.H3('Si quieres cooperar con esta iniciativa escríbeme a jxvera@gmail.com',style={'fontSize': 14})
], style={'columnCount': 2})


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value'),
               State('input-3-state', 'value'),
               State('input-4-state', 'value'),
               State('input-5-state', 'value')])


def verb_to_mapudungun(n_clicks, verb_esp,numero,persona,polaridad,tiempo):

    verbos={esp:mapu for (esp,mapu) in zip(verbos_esp,verbos_mapu)}
    base=verbos[verb_esp]
    conjugacion={'singular':{'primera':'iñche (yo)','segunda':'eymi (tú)','tercera':'fey (ella/él)'},'dual':{'primera':'iñchiw (nosotras/nosotros dos)','segunda':'eymu (ustedes dos)','tercera':'feyengu (ellas/ellos dos)'},'plural':{'primera':'iñchiñ (nosotras/nosotros)','segunda':'eymün (ustedes)','tercera':'feyengün (ellas/ellos)'}}
    expansion=base+' '+'(base)'
    if polaridad=='positiva':## persona gramatical + base + futuro + polaridad
        if tiempo=='futuro':
            traduccion=conjugacion[numero][persona]+' '+base+'a'
            expansion+=' '+'+'+' '+'a'+' (futuro)'
        else:
            traduccion=conjugacion[numero][persona]+' '+base
    elif polaridad=='negativa':
        if tiempo=='futuro':
            traduccion=conjugacion[numero][persona]+' '+base+'la'+'ya'
            expansion+=' '+'+'+' '+'la'+' '+'(negación)'+' '+'+'+' '+'ya'+' '+'(futuro)'
        else:
            traduccion=conjugacion[numero][persona]+' '+base+'la'
            expansion+=' '+'+'+' '+'la'+' '+'(negación)'


    if base[-1] in consonantes: ## terminan en consonante
        if numero=='singular':
            if persona=='primera':
                traduccion=traduccion+'ün'
                expansion+=' '+'+'+'ün'+' '+'(1SG)'
            elif persona=='segunda':
                traduccion=traduccion+'imi'
                expansion+=' '+'+'+'imi'+' '+'(2SG)'
            else:
                traduccion=traduccion+'i'
                expansion+=' '+'+'+'i'+' '+'(3SG)'
        elif numero=='dual':
            if persona=='primera':
                traduccion=traduccion+'iyu'
                expansion+=' '+'+'+'iyu'+' '+'(1DUAL)'
            elif persona=='segunda':
                traduccion=traduccion+'imu'
                expansion+=' '+'+'+'imu'+' '+'(2DUAL)'
            else:
                traduccion=traduccion+'ingu'
                expansion+=' '+'+'+'ingu'+' '+'(3DUAL)'
        else:
            if persona=='primera':
                traduccion=traduccion+'iyiñ'
                expansion+=' '+'+'+'iyiñ'+' '+'(1PL)'
            elif persona=='segunda':
                traduccion=traduccion+'imün'
                expansion+=' '+'+'+'imün'+' '+'(2PL)'
            else:
                traduccion=traduccion+'ingün'
                expansion+=' '+'+'+'ingün'+' '+'(3PL)'

    elif base[-1]=='i': ## termina en i
        if numero=='singular':
            if persona=='primera':
                traduccion=traduccion+'n'
                expansion+=' '+'+'+'n'+' '+'(1SG)'
            elif persona=='segunda':
                traduccion=traduccion+'mi'
                expansion+=' '+'+'+'mi'+' '+'(2SG)'
            else:
                traduccion=traduccion
                expansion+=' '+'+'+'0'+' '+'(3SG)'
        elif numero=='dual':
            if persona=='primera':
                traduccion=traduccion+'yu'
                expansion+=' '+'+'+'yu'+' '+'(1DUAL)'
            elif persona=='segunda':
                traduccion=traduccion+'mu'
                expansion+=' '+'+'+'mu'+' '+'(2DUAL)'
            else:
                traduccion=traduccion+'ngu'
                expansion+=' '+'+'+'ngu'+' '+'(3DUAL)'
        else:
            if persona=='primera':
                traduccion=traduccion+'iñ'
                expansion+=' '+'+'+'iñ'+' '+'(1PL)'
            elif persona=='segunda':
                traduccion=traduccion+'mün'
                expansion+=' '+'+'+'mün'+' '+'(2PL)'
            else:
                traduccion=traduccion+'ngün'
                expansion+=' '+'+'+'ngün'+' '+'(3PL)'

    else: ## en otro caso
        if numero=='singular':
            if persona=='primera':
                traduccion=traduccion+'n'
                expansion+=' '+'+'+'n'+' '+'(1SG)'
            elif persona=='segunda':
                traduccion=traduccion+'ymi'
                expansion+=' '+'+'+'ymi'+' '+'(2SG)'
            else:
                traduccion=traduccion+'y'
                expansion+=' '+'+'+'y'+' '+'(3SG)'
        elif numero=='dual':
            if persona=='primera':
                traduccion=traduccion+'yu'
                expansion+=' '+'+'+'yu'+' '+'(1DUAL)'
            elif persona=='segunda':
                traduccion=traduccion+'ymu'
                expansion+=' '+'+'+'ymu'+' '+'(2DUAL)'
            else:
                traduccion=traduccion+'yngu'
                expansion+=' '+'+'+'yngu'+' '+'(3DUAL)'
        else:
            if persona=='primera':
                traduccion=traduccion+'iñ'
                expansion+=' '+'+'+'iñ'+' '+'(1PL)'
            elif persona=='segunda':
                traduccion=traduccion+'ymün'
                expansion+=' '+'+'+'ymün'+' '+'(2PL)'
            else:
                traduccion=traduccion+'yngün'
                expansion+=' '+'+'+'yngün'+' '+'(3PL)'


    return (html.P(['En mapudungun, el verbo "{}" conjugado en "{}" persona "{}" en polaridad "{}" y tiempo "{}" se dice'.format(verb_esp,persona,numero,polaridad,tiempo)+' '+'"'+traduccion+'"',html.Br(),html.Strong('Morfología :) '+traduccion.replace(conjugacion[numero][persona]+' ','')+' = '+expansion, style={'color': '#8B008B', 'fontSize': 14})]))



if __name__ == '__main__':
    app.run_server(debug=True)
