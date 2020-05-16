import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div('enter the credit summ:'),
    dcc.Input(id='credit_size_id', type='number', value=None, max=10000000, step=1),
    html.Div('enter the rate:'),
    dcc.Input(id='rate_id', type='number', value=None, max=100, min=0, step=1),
    html.Div('enter the period in monthes:'),
    dcc.Input(id='period_id', type='number', value=None, max=120, min=0, step=1),
    html.Div('enter the max size of month payment:'),
    dcc.Input(id='max_payment_size_id', type='number', value=None),
    html.Div(id='errors'),
    dcc.Graph(id='month_graph'),
    dcc.Graph(id='overpayment_graph')
])

@app.callback(Output('errors', 'children'),
    [
        Input('credit_size_id', 'value'),
        Input('rate_id', 'value'),
        Input('period_id', 'value'),
        Input('max_payment_size_id', 'value')
    ])
def render_content(credit_size, rate, period, max_payment_size):
    return html.Div([
        html.Div('error')
    ])


if __name__ == '__main__':
    app.run_server(debug=True)