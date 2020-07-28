import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta


### COLORS & STYLE OF GRAPHS AS VARIABLES
backgroundColor = 'white'
textColor = '#282A2A'
highlightColor = 'lightsteelblue'
colorOne = 'mediumaquamarine'
colorTwo = 'cornflowerblue'
colorThree = 'indianred'

quadBoxStyle = {'text-align':'center', 
                'border':'1px #f9f9f9 solid',
                'border-radius':10, 
                'box-shadow':'10px 5px 8px #e6e6e6',
                'background-color':'white',
                'padding':'2px'}

tabsStyle = {'border': '1px #f9f9f9 solid',
                'border-radius' : 10,
                'box-shadow':'10px 5px 8px #e6e6e6',
                'background-color' : 'white',
                'padding': '20px',
                'text-color' : textColor}

tabColors = {'border': 'white',
                'primary': highlightColor,
                'background': 'ghostwhite'}

xaxisYearlyStyle = {'showline': True,
                'showgrid': False,
                'linecolor': textColor,
                'type': 'date',
                'tickformat': '%Y',
                'ticks': 'outside'}

xaxisMonthlyStyle = {'showline': True,
                'showgrid': False,
                'linecolor': textColor,
                'type': 'date',
                'tickformat': '%b %d',
                'ticks': 'outside'}

yaxisStyle = { 'fixedrange': True,
                'showline': False,
                'linecolor': textColor,
                'showgrid': True,
                'gridcolor': '#e1e1e1'}

yaxisPercentStyle = {'title': '%',
                'fixedrange': True,
                'showline': False,
                'linecolor': textColor,
                'showgrid': True,
                'gridcolor': '#e1e1e1'}


marginStyle = {'t': 50, 'l': 20, 'r': 20}

legendStyle = {'orientation': 'h',
                'yanchor': 'bottom',
                'y': 1.02,
                'xanchor': 'center',
                'x': 1}

headerStyle = {'letter-spacing': '2px',
                'font-weight': 'lighter',
                'font-family': 'Futura',
                'text-align': 'left'
}

   


### DATE VARIABLES
today = date.today()

thisYear = str(date.today().year)

thisMonth = date.today().month
lastMonth = '0'+str(thisMonth - 1)
twoMonthsAgo = '0'+str(thisMonth -2)

lastSaturday = today - timedelta(days=today.weekday()) + timedelta(days=5, weeks=-1)
lastSaturdayString = lastSaturday.strftime('%Y-%m-%d')

lastLastSaturday = lastSaturday + timedelta(weeks=-1)
lastLastSaturdayString = lastLastSaturday.strftime('%Y-%m-%d')

threeSatsAgo = lastLastSaturday + timedelta(weeks=-1)
threeSatsAgo = threeSatsAgo.strftime('%Y-%m-%d')


### SERVER AND APP SETUP
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = 'The Indicator App' #tab on top of browser


### SPREADSHEETS
ICSA_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/fredICSA.csv', header =0)
ICSA_historical = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/ICSA_historical.csv', header = 0)
CCSA_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/fredCCSA.csv', header= 0)
unemploymentRate_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/unemploymentRate.csv', header= 0)
u6_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/U6unemployment.csv', header = 0)
payrollJobs_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/PayrollJobs.csv', header = 0)
jobsBySector_MoM_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/payroll-jobs-by-sector/jobsSector_MoM.csv', header = 0)
jobsBySector_MoY_df = pd.read_csv('https://raw.githubusercontent.com/cansu-freeman/indicator-app-data/master/payroll-jobs-by-sector/jobsSector_MoY.csv', header = 0)


### KEY INDICATORS AS VARIABLES
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
    xaxis = xaxisMonthlyStyle, 
    yaxis = yaxisStyle,
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)

### fig2: Historical Initial Claims Nationally
fig2 = go.Figure()
fig2.add_trace(go.Bar(x = ICSA_historical['Date'], y = ICSA_historical['ICSA'],
                    name = 'Initial Claims',
                    marker_color = colorOne))
fig2.update_layout(
    xaxis = xaxisYearlyStyle,
    yaxis = yaxisStyle,
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)


### fig3: Unemployment Rate since 2010
fig3 = go.Figure()
fig3.add_trace(go.Bar(x = unemploymentRate_df['Date'], y = unemploymentRate_df['Unemployment Rate'],
                    name = 'Unemployment Rate',
                    marker_color = colorOne))
fig3.update_layout(
    xaxis = xaxisYearlyStyle,
    yaxis = yaxisPercentStyle,
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
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
    xaxis = xaxisYearlyStyle,
    yaxis = yaxisPercentStyle,
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)

###fig5: Payroll Jobs
fig5 = go.Figure()
fig5.add_trace(go.Bar(x = payrollJobs_df['Date'], y = payrollJobs_df['12M Change'],
                    name = 'MoY Change in Payroll Jobs',
                    marker_color = colorTwo))
fig5.update_layout(
    xaxis = xaxisYearlyStyle,
    yaxis = yaxisStyle,
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)

### fig6: Month to Month Payroll Jobs Change
fig6 = go.Figure()
fig6.add_trace(go.Bar(x = payrollJobs_df['Date'], y = payrollJobs_df['1M Change'],
                    name = 'MoY Change in Payroll Jobs',
                    marker_color = colorTwo))
fig6.update_layout(
    xaxis = xaxisYearlyStyle,
    yaxis = yaxisStyle,
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)

### fig7: Recent Month Change Payroll Jobs by Sector 
# Prepping DF
jobsBySector_MoM_df = jobsBySector_MoM_df.rename(columns = {'Unnamed: 0' : 'Sector'}) #have to rename because of github
jobsBySector_MoM_df['Sector'].replace({'fedGovt 1M': 'Federal Govt',
                                        'eduHealth 1M': 'Education & Health Services',
                                        'profBusServ 1M': 'Professional Business Services',
                                        'leisureHosp 1M': 'Leisure & Hospitality',
                                        'retailTrade 1M': 'Retail Trade',
                                        'mfg 1M': 'Manufacturing',
                                        'financial 1M': 'Financial',
                                        'constr 1M': 'Construction',
                                        'wholesale 1M': 'Wholesale Trade',
                                        'other 1M': 'Other Servies',
                                        'transp 1M': 'Transportation',
                                        'info 1M': 'Information'}, inplace = True)
jobsBySector_MoM_df['Color'] = np.where(jobsBySector_MoM_df[thisYear+'-'+lastMonth]<0, colorThree, colorOne)

fig7 = go.Figure()
fig7.add_trace(go.Bar(x = jobsBySector_MoM_df[thisYear+'-'+lastMonth], y = jobsBySector_MoM_df['Sector'],
                    orientation = 'h',
                    marker_color = jobsBySector_MoM_df['Color']))
fig7.update_layout(
    xaxis = {
        'title': 'Number of Jobs (in thousands)',
        'showline': True,
        'showgrid': True,
        'gridcolor': '#e1e1e1',
        'linecolor': textColor
    },
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)

### fig8: Recent Yearly (MoY) Change Payroll Jobs by Sector
# Preparing DF
jobsBySector_MoY_df = jobsBySector_MoY_df.rename(columns = {'Unnamed: 0' : 'Sector'})
jobsBySector_MoY_df['Sector'].replace({'fedGovt 12M': 'Federal Govt',
                                        'eduHealth 12M': 'Education & Health Services',
                                        'profBusServ 12M': 'Professional Business Services',
                                        'leisureHosp 12M': 'Leisure & Hospitality',
                                        'retailTrade 12M': 'Retail Trade',
                                        'mfg 12M': 'Manufacturing',
                                        'financial 12M': 'Financial',
                                        'constr 12M': 'Construction',
                                        'wholesale 12M': 'Wholesale Trade',
                                        'other 12M': 'Other Servies',
                                        'transp 12M': 'Transportation',
                                        'info 12M': 'Information'}, inplace = True)

jobsBySector_MoY_df['Color'] = np.where(jobsBySector_MoY_df[thisYear+'-'+lastMonth]<0, colorThree, colorOne)

fig8 = go.Figure()
fig8.add_trace(go.Bar(x = jobsBySector_MoY_df[thisYear+'-'+lastMonth], y = jobsBySector_MoY_df['Sector'],
                    orientation = 'h',
                    marker_color = jobsBySector_MoY_df['Color']))
fig8.update_layout(
    xaxis = {
        'title': 'Number of Jobs (in thousands)',
        'showline': True,
        'showgrid': True,
        'gridcolor': '#e1e1e1',
        'linecolor': textColor
    },
    margin= marginStyle,
    paper_bgcolor = 'white',
    plot_bgcolor = 'white',
    legend = legendStyle
)




################ APPLICATION #################

app.layout = html.Div(children = [


    html.Div([
        html.Img(src = app.get_asset_url('icon.png'), alt = 'The Indicator App Logo', style = {
            'width': '100px',
            'height': '100px',
            #'vertical-align': 'bottom'
        }),
            html.H1('The Indicator  ', style = {'display': 'inline-block',
                                                'width': '65%',
                                                'font-family': 'Futura',
                                                'color': '#282A2A',
                                                'font-weight': 'bold'}),
            html.Button(['VIEW ON ',
                    html.A('GITHUB', href = 'https://github.com/cansu-freeman/indicator-app',
                        style = {'color': highlightColor}
                    )
            ], style = {'display': 'inline-block',
                        'width': '166px',
                        'height': '40px'}
            ),
    ], 
    style = {'background': 'white',
                'width': '100%'}
    ),

    html.Br(),
    html.Br(),

    html.Div([
        html.H4('UNEMPLOYMENT SITUATION',
            style = headerStyle),
    ]),
    
    ### QUADBOX INDICATORS AT TOP
    html.Div([
        html.Div([
            html.Br(),
            html.H3(str(totalInitialClaims)+' M'),
            html.P(['Total Claims', html.Br(), 'since March']),
            html.Br(),
        ], style = quadBoxStyle, className = 'four columns'),

        html.Div([
            html.Br(),
            html.H3(str(totalContinuedClaims)+' M'),
            html.P(['Continuing', html.Br(), 'Claims']),
            html.Br(),
        ], style = quadBoxStyle, className = 'four columns'),

        html.Div([
            html.Br(),
            html.H3(str(lastWeekClaims)+' M'),
            html.P(['New Claims Filed', html.Br(), 'Last Week']),
            html.Br(),    
        ], style = quadBoxStyle, className = 'four columns'),

        html.Div([
            html.Br(),
            html.H3(str(currentUnempRate)+' %'),
            html.P(['Unemployment Rate', html.Br(), 'June 2020']),
            html.Br(),
        ], style = quadBoxStyle, className = 'four columns')

    ], style = {
        'width': '100%',
        'display':'flex',
        'align-items':'center',
        'justify-content':'center'}, className = 'row'),

    html.Br(),

    ### TABBED UNEMPLOYMENT GRAPHS
    html.Div([
        dcc.Tabs([

            dcc.Tab(label = 'Unemployment Claims', children =[
                html.H6('Recent National Unemployment Claims (seasonally adjusted)'),
                dcc.Graph(
                    id = 'recent-nemployment',
                    figure = fig1
                ),
                html.P('Initial claims measure emerging unemployment. Continuing claims is the number of people receiving unemployment benefits who have already filed an initial claim.  In order to be included in continuing claims, the person must have been covered by unemployment insurance and be currently receiving benefits. He or she must have been unemployed for at least a week after filing the initial claim, per Department of Labor specifications.')
            ]),

            dcc.Tab(label = 'Unemployment Rate', children = [
                html.H6('National Unemployment Rate, Month to Month'),
                dcc.Graph(
                    id = 'unemployment-rate',
                    figure = fig3
                ),
                html.P('The unemployment rate measures the share of the labor force that is not currently employed but could be. It is expressed as a percentage.')
            ]),

            dcc.Tab(label = 'Comparing U6', children = [
                html.H6('U6 Unemployment Compared to Standard Measure of Unemployment'),
                dcc.Graph(
                    id = 'u6-unemployment',
                    figure = fig4
                ),
                html.P('There are alternative measures of unemployment. The "U6" measures total unemployed, plus all persons marginally attached to the labor force, plus total employed part time for economic reasons, as a percent of the civilian labor force plus all persons marginally attached to the labor force.')
            ]),

            dcc.Tab(label = 'Historical Initial Claims', children = [
                html.H6('Weekly Initial Unemployment Claims since 2007'),
                dcc.Graph(
                    id = 'historical-initial-claims',
                    figure = fig2
                ),
                html.P('Recall that the last recession in the United States occured from the end of 2007 to the middle of 2009.')
            ])

        ], colors = tabColors)

    ], style = tabsStyle),

    html.Br(),

    html.Br(),

    html.Div([
        html.H4('JOBS REPORT',
            style = headerStyle),
    ]),

    ### TABBED JOBS GRAPHS
    html.Div([
        dcc.Tabs([

            dcc.Tab(label = 'Annual Jobs Change', children = [
                html.H6('Annual Payroll Jobs Change, Month over Year'),
                dcc.Graph(
                    id = 'annual-jobs-change',
                    figure = fig5
                ),
                html.P("This is showing the change in the amount of Payroll Jobs each month from the corresponding month a year prior. The y-axis is scaled in thousands (000's) so 20k corresponds to 2 million. This effect will be changed in future versions of The Indicator.")
            ]),

            dcc.Tab(label = 'Monthly Jobs Change', children = [
                html.H6('Monthly Payroll Jobs Change'),
                dcc.Graph(
                    id = 'monthly-jobs-change',
                    figure = fig6
                ),
                html.P("This chart shows month-to-month change in payroll jobs. The y-axis is scaled in thousands (000's) so 20k corresponds to 2 million. This effect will be changed in future versions of The Indicator.")
            ]),

            dcc.Tab(label = 'Current Month Job Change by Sector', children = [
                html.H6("Payroll Job Change by Sector for June 2020 (in thousands 000's)"),
                dcc.Graph(
                    id = 'sector-MoM',
                    figure = fig7
                ),
                html.P('Change in number of jobs for the month of June. The "Leisure and Hospitality sector gained over 2 million jobs.')
            ]),

            dcc.Tab(label = 'One Year Job Change by Sector', children = [
                html.H6("Payroll Job Change by Sector from June 2019 to June 2020 (in thousands 000's)"),
                dcc.Graph(
                    id = 'sector-MoY',
                    figure = fig8
                ),
                html.P('This represents the change in jobs per sector over the last year.')
            ])

        ], colors = tabColors)

    ], style = tabsStyle),
    
    html.Br(),



    ### SOURCES
    html.Div([
        html.P([
            html.A('Developed by Cansu Freeman', href = 'https://cansufreeman.com',
                style = {'color': highlightColor})
        ]),
        html.P('Sources: Bureau of Labor Statistics and Federal Reserve Economic Data'),
    ], style = {'width': '100%', 'text-align': 'right'}),

    html.Br()
    


], style = {
    'backgroundColor': backgroundColor,
    'padding': '10px',
    'color': textColor,
    'font-family': 'Futura',
    'font-weight': ''})





if __name__ == '__main__':
    app.run_server(debug = True)