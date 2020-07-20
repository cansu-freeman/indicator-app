import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
from datetime import date, timedelta


### Colors
backgroundColor = 'whitesmoke'
textColor = 'darkslategrey'
highlightColor = 'lightsteelblue'
colorOne = 'mediumaquamarine'
colorTwo = 'cornflowerblue'


### Date Variables
today = date.today()

thisYear = str(date.today().year)

thisMonth = date.today().month
lastMonth = '0'+str(thisMonth - 1)

lastSaturday = today - timedelta(days=today.weekday()) + timedelta(days=5, weeks=-1)
lastSaturdayString = lastSaturday.strftime('%Y-%m-%d')

lastLastSaturday = lastSaturday + timedelta(weeks=-1)
lastLastSaturday = lastLastSaturday.strftime('%Y-%m-%d')


### Style Sheet for Dash/Heroku
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


### Spreadsheets
ICSA_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app/master/fredICSA.csv', header =0)
CCSA_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app/master/fredCCSA.csv', header= 0)
unemploymentRate_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app/master/unemploymentRate.csv', header= 0)

# ### Defining Key Inicators as Variables
totalInitialClaims = ICSA_df['ICSA'].sum()
totalInitialClaims = (totalInitialClaims/1000000).round(1)

lastWeekClaims = ICSA_df.loc[ICSA_df['Date'] == lastSaturdayString, 'in_millions'].values[0].round(1)

CCSA_df['Date'] = CCSA_df['Date'].astype(str)
totalContinuedClaims = CCSA_df.loc[CCSA_df['Date'] == lastLastSaturday, 'in_millions'].values[0].round(1)

currentUnempRate = unemploymentRate_df.loc[unemploymentRate_df['Date'] == thisYear+'-'+lastMonth, 'Unemployment Rate'].values[0]
print(currentUnempRate)

### Creating fig1: Initial Claims for Unemployment Nationally
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x = ICSA_df['Date'], y = ICSA_df['ICSA'],
                    mode = 'lines', 
                    name = 'Initial CLaims',
                    line_color = colorOne))
fig1.add_trace(go.Scatter(x = ICSA_df['Date'], y = CCSA_df['CCSA'],
                    mode = 'lines',
                    name = 'Continued Claims',
                    line_color = colorTwo))
fig1.update_layout(
    xaxis = dict(
        title = '2020',
        showline = True,
        showgrid = False,
        linecolor = textColor,
        type = 'date',
        tickformat = '%b %d',
        ticks = 'outside',
        tickangle=-45
    ), 
    yaxis = dict(
        title = '',
        showline = False,
        linecolor = textColor,
        showgrid = True,
        gridcolor = '#e1e1e1',
     ),
    margin= dict(
        t=50,
        l=20,
        r=20,
    ),
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=1
    )
)





################ APPLICATION

app.layout = html.Div(style = {'backgroundColor': backgroundColor, 'padding': '30px', 'color': textColor}, children =[
    
    html.Div([
        html.Div([
            html.H1('Economic Indicators'
            )
        ], style = {'width' : '60%'}, className = 'two columns'),
        html.Div([
            html.Button(['CREATED BY ',
                dcc.Link('CANSU FREEMAN', href ='https://cansufreeman.com', 
                style = {'color': highlightColor})
            ])
        ], style = {'justify-items': 'right', 'display': 'flex', 'width': '20%'}, className = 'two columns'),
    ], style = {'width': '100%', 'display': 'inline'}, className = 'top row header'),

    html.Br(),
    html.H3('Unemployment Situation',
    style = {'text-align': 'left'}),
  
   # four column-boxes at the top of page
    html.Div([
        html.Div([
            html.Br(),
            html.H3(str(totalInitialClaims)+' M'),
            html.P(['Total Claims', html.Br(), ' since March']),
            html.Br(),
                ],  
            style = {
                'text-align': 'center', 
                'border':'1px #f9f9f9 solid',
                'border-radius': 10, 
                'box-shadow':'10px 5px 8px #e6e6e6',
                'background-color': 'white',
                'padding': '2px'}, className = 'four columns'),

        html.Div([
            html.Br(),
            html.H3(str(totalContinuedClaims)+' M'),
            html.P(['Continued', html.Br(),' Claims']),
            html.Br(),
                ],  
            style = {
                'text-align': 'center', 
                'border':'1px #f9f9f9 solid',
                'border-radius': 10, 
                'box-shadow':'10px 5px 8px #e6e6e6',
                'background-color': 'white',
                'padding': '2px'}, className = 'four columns'),

        html.Div([
            html.Br(),
            html.H3(str(lastWeekClaims)+' M'),
            html.P('Claims Filed Last Week'),
            html.Br(),
        ],  
            style = {
                'color': textColor,
                'text-align': 'center', 
                'border':'1px #f9f9f9 solid',
                'border-radius': 10, 
                'box-shadow':'10px 5px 8px #e6e6e6',
                'background-color': 'white',
                'padding': '2px'}, className = 'four columns'),

        html.Div([
            html.Br(),
            html.H3(str(currentUnempRate)+' %'),
            html.P(['Unemployment Rate', html.Br(), ' June 2020']),
            html.Br(),
                ],  
            style = {
                'text-align': 'center', 
                'border':'1px #f9f9f9 solid',
                'border-radius': 10, 
                'box-shadow':'10px 5px 8px #e6e6e6',
                'background-color': 'white',
                'padding': '2px'}, className = 'four columns')
    
    ], style = {'width': '100%', 'display':'flex', 'align-items':'center', 'justify-content':'center'}, className = 'row'),

    html.Br(),
        
    #graph
    html.Div([
        html.H5('National Unemployment Claims (seasonally adjusted)', style = {'text-align' :'center', 'color' : textColor}),
        dcc.Graph(
        id='InitialClaims_recent',
        figure=fig1,
        config={'frameMargins': False})
    ], style = {
        'border': '1px #f9f9f9 solid',
        'border-radius' : 10,
        'box-shadow':'10px 5px 8px #e6e6e6',
        'background-color' : 'white',
        'padding': '2px'
    }),

    #source text
    html.Br(),
    html.Div([
        html.P('Source: Bureau of Labor Statistics and Federal Reserve Economic Data'),
        html.P([
            dcc.Link('View on GitHub', href = 'https://github.com/cansu-freeman', style = {'color': highlightColor})
        ])])
])

if __name__ == '__main__':
    app.run_server()

#0.0.0.0
