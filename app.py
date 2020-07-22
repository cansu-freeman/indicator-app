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
colorThree = 'indianred'


### Date Variables
today = date.today()

thisYear = str(date.today().year)

thisMonth = date.today().month
lastMonth = '0'+str(thisMonth - 1)

# MOST RECENT PAST SATURDAY
lastSaturday = today - timedelta(days=today.weekday()) + timedelta(days=5, weeks=-1)
lastSaturdayString = lastSaturday.strftime('%Y-%m-%d')

# SATURDAY PRIOR THAN MOST RECENT
lastLastSaturday = lastSaturday + timedelta(weeks=-1)
lastLastSaturdayString = lastLastSaturday.strftime('%Y-%m-%d')

# THREE SATURDAYS AGO
threeSatsAgo = lastLastSaturday + timedelta(weeks=-1)
threeSatsAgo = threeSatsAgo.strftime('%Y-%m-%d')


### Style Sheet for Dash/Heroku
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'The Indicator App' #tab on top of browser

### Spreadsheets
ICSA_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/fredICSA.csv', header =0)
ICSA_historical = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/ICSA_historical.csv', header = 0)
CCSA_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/fredCCSA.csv', header= 0)
unemploymentRate_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/unemploymentRate.csv', header= 0)
u6_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/U6unemployment.csv', header = 0)
payrollJobs_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/PayrollJobs.csv', header = 0)

# ### Defining Key Inicators as Variables
totalInitialClaims = ICSA_df['ICSA'].sum()
totalInitialClaims = (totalInitialClaims/1000000).round(1)

lastWeekClaims = ICSA_df.loc[ICSA_df['Date'] == lastLastSaturdayString, 'in_millions'].values[0].round(1)

CCSA_df['Date'] = CCSA_df['Date'].astype(str)
totalContinuedClaims = CCSA_df.loc[CCSA_df['Date'] == threeSatsAgo, 'in_millions'].values[0].round(1)

currentUnempRate = unemploymentRate_df.loc[unemploymentRate_df['Date'] == thisYear+'-'+lastMonth, 'Unemployment Rate'].sum()


### fig1: Recent Initial and Continued Claims for Unemployment Nationally
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x = ICSA_df['Date'], y = ICSA_df['ICSA'],
                    mode = 'lines', 
                    name = 'Initial Claims',
                    line_color = colorOne))
fig1.add_trace(go.Scatter(x = ICSA_df['Date'], y = CCSA_df['CCSA'],
                    mode = 'lines',
                    name = 'Continuing Claims',
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


### fig2: Historical Initial Claims Nationally
fig2 = go.Figure()
fig2.add_trace(go.Bar(x = ICSA_historical['Date'], y = ICSA_historical['ICSA'],
                    name = 'Initial Claims',
                    marker_color = colorOne))
fig2.update_layout(
    xaxis = dict(
        showline = True,
        showgrid = False,
        linecolor = textColor,
        type = 'date',
        tickformat = '%Y',
        ticks = 'outside',
        tickangle=-45
    ), 
    yaxis = dict(
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


### fig3: Unemployment Rate since 2010
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = unemploymentRate_df['Date'], y = unemploymentRate_df['Unemployment Rate'],
                    name = 'Unemployment Rate',
                    marker_color = colorOne))
fig3.update_layout(
     xaxis = dict(
        showline = True,
        showgrid = False,
        linecolor = textColor,
        type = 'date',
        tickformat = '%Y',
        ticks = 'outside',
        tickangle=-45
    ), 
    yaxis = dict(
        title = 'Percent (%)',
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

### fig4: U6 Unemployment Rate
fig4 = go.Figure()
fig4.add_trace(go.Scatter(x = u6_df['Date'], y = u6_df['U6'],
                    mode = 'lines',
                    name = 'U6',
                    line_color = colorTwo))
fig4.add_trace(go.Scatter(x = unemploymentRate_df['Date'], y = unemploymentRate_df['Unemployment Rate'],
                    mode = 'lines',
                    name = 'Unemployment Rate',
                    line_color = colorOne))
fig4.update_layout(
    xaxis = dict(
        showline = True,
        showgrid = False,
        linecolor = textColor,
        type = 'date',
        tickformat = '%Y',
        ticks = 'outside',
        tickangle=-45
    ), 
    yaxis = dict(
        title = 'Percent (%)',
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

###fig5: Payroll Jobs
fig5 = go.Figure()
fig5.add_trace(go.Bar(x = payrollJobs_df['Date'], y = payrollJobs_df['12M Change'],
                    name = 'MoY Change in Payroll Jobs',
                    marker_color = colorThree))
fig5.update_layout(
    xaxis = dict(
        showline = True,
        showgrid = False,
        linecolor = textColor,
        type = 'date',
        tickformat = '%Y',
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

### fig6: Month to Month Payroll Jobs Change
fig6 = go.Figure()
fig6.add_trace(go.Bar(x = payrollJobs_df['Date'], y = payrollJobs_df['1M Change'],
                    name = 'MoY Change in Payroll Jobs',
                    marker_color = colorThree))
fig6.update_layout(
    xaxis = dict(
        showline = True,
        showgrid = False,
        linecolor = textColor,
        type = 'date',
        tickformat = '%Y',
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

app.layout = html.Div(style = {'backgroundColor': backgroundColor, 'padding': '30px', 'color': textColor, 'font-family': 'Verdana'}, children =[
    
    html.Div([
        html.H1('THE INDICATOR APP'),

        # Button on top of page 
        # html.Button(['VIEW ON ',
        #         html.A('GITHUB', href ='https://github.com/cansu-freeman/indicator-app', 
        #         style = {'color': highlightColor}
        #         )
        # ]),
    ], style = {'text-align': 'center'}),

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
            html.P(['Continuing', html.Br(),' Claims']),
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
            html.P(['Claims Filed', html.Br(), 'Last Week']),
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
        
    #Tabbed Unemployment Graphs 
    html.Div([
        dcc.Tabs([
            dcc.Tab(label = 'Unemployment Claims', children = [ 
                html.H6('National Unemployment Claims (seasonally adjusted)', style = {'color' : textColor}),
                dcc.Graph(
                    id='Unemployment Claims',
                    figure = fig1
                ),
                html.P('Initial claims measure emerging unemployment. Continuing claims is the number of people receiving unemployment benefits who have already filed an initial claim.  In order to be included in continuing claims, the person must have been covered by unemployment insurance and be currently receiving benefits. He or she must have been unemployed for at least a week after filing the initial claim, per Department of Labor specifications.')
            ]),
            dcc.Tab(label = 'Unemployment Rate', children = [
                html.H6('National Unemployment Rate, Month-to-Month'),
                dcc.Graph(
                    id = 'Unemployment Rate',
                    figure = fig3
                ),
                html.P('The unemployment rate measures the share of the labor force that is not currently employed but could be. It is expressed as a percentage.')
            ]),
            dcc.Tab(label = 'U6', children = [
                html.H6('U6 Rate Compared to Regular Unemployment Rate'),
                dcc.Graph(
                    id = 'U6 Unemployment',
                    figure = fig4

                ),
                html.P('There are alternative measures of unemployment. The "U6" measures total unemployed, plus all persons marginally attached to the labor force, plus total employed part time for economic reasons, as a percent of the civilian labor force plus all persons marginally attached to the labor force.')
            ]),
            dcc.Tab(label = 'Historical Initial Claims', children = [
                html.H6('Weekly Initial Unemployment Claims since 2007'),
                dcc.Graph(
                    id = 'Historical Claims',
                    figure = fig2
                ),
                html.P('Recall that the last recession in the United States occured from the end of 2007 to the middle of 2009.')
            ])
        ], colors={
        "border": "white",
        "primary": highlightColor,
        "background": 'ghostwhite'}),
    ], style = {
                            'border': '1px #f9f9f9 solid',
                            'border-radius' : 10,
                            'box-shadow':'10px 5px 8px #e6e6e6',
                            'background-color' : 'white',
                            'padding': '20px',
                            'text-color' : textColor}),
    html.Br(),
    html.Br(),

    # Tabbed Jobs Graphs
    html.H3('Jobs Report'),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label = 'Annual Payroll Jobs Change', children = [
                html.H6('Annual Payroll Jobs Change Since 2007 (Month over Year)'),
                dcc.Graph(
                    id ='12M Change Payroll Jobs',
                    figure = fig5
                ),
                html.P('This is showing the change in the amount of Payroll Jobs each month from the corresponding month a year prior.'),
            ]),
            dcc.Tab(label = 'Monthly Payroll Jobs Change', children = [
                html.H6('Month to Month Payroll Jobs Change Since 2007'),
                dcc.Graph(
                    id = '1M Change in Payroll Jobs',
                    figure = fig6
                ),
                html.P('')
            ])
        ], colors={
        "border": "white",
        "primary": highlightColor,
        "background": 'ghostwhite'})
    ], style = {
                            'border': '1px #f9f9f9 solid',
                            'border-radius' : 10,
                            'box-shadow':'10px 5px 8px #e6e6e6',
                            'background-color' : 'white',
                            'padding': '20px',
                            'text-color': textColor}),

    #source text
    html.Br(),
    html.Div([
        html.P('Source: Bureau of Labor Statistics and Federal Reserve Economic Data'),
        html.P([
            html.A('Created by Cansu Freeman', href = 'https://cansufreeman.com', style = {'color': highlightColor})
        ])])
])

if __name__ == '__main__':
    app.run_server(debug = True)