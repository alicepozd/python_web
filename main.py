from flask import Flask, render_template
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output


def calculate_period(credit_size, rate, input_period, max_payment_size):
    month_rate = float(rate) / 100 / 12
    period = 0
    while credit_size > 0:
        if max_payment_size - credit_size * month_rate <= 0 or period > 120:
            return input_period
        credit_size -= max_payment_size - credit_size * month_rate
        period += 1
    return period


def get_month_graph(credit_size, rate, period, max_payment_size):
    if max_payment_size:
        period = calculate_period(credit_size, rate, period, max_payment_size)
    month_rate = float(rate) / 100 / 12
    annuity_rate = month_rate * (1 + month_rate)**period / ((1 + month_rate)**period - 1)
    month_payment = round(annuity_rate * credit_size)
    body_remainder = credit_size
    x_payment = []
    y_payment = []
    y_credit_body = []
    for i in range(period):
        x_payment.append(i)
        y_payment.append(round(body_remainder * month_rate))
        y_credit_body.append(month_payment - round(body_remainder * month_rate))
        body_remainder = body_remainder - (month_payment - body_remainder * month_rate)
    return x_payment, y_payment, y_credit_body


def get_overpayment_graph(credit_size, rate):
    payment_period = []
    overpayment = []
    for period in range(1, 180):
        month_rate = float(rate) / 100 / 12
        annuity_rate = month_rate * (1 + month_rate)**period / ((1 + month_rate)**period - 1)
        month_payment = annuity_rate * credit_size
        payment_period.append(period)
        overpayment.append(round(period * month_payment - credit_size))
    return payment_period, overpayment


server = Flask(__name__)


@server.route("/", methods=['post', 'get'])
def home():
    return render_template("home.html")


app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')


app.layout = html.Div([
    html.Div('enter the credit summ:'),
    dcc.Input(id='credit_size_id', type='number', value=None, max=10000000, step=1),
    html.Div('enter the rate:'),
    dcc.Input(id='rate_id', type='number', value=None, max=100, min=0, step=1),
    html.Div('enter the period in monthes:'),
    dcc.Input(id='period_id', type='number', value=None, max=120, min=0, step=1),
    html.Div('enter the max size of month payment:'),
    dcc.Input(id='max_payment_size_id', type='number', value=None),
    dcc.Graph(id='month_graph'),
    dcc.Graph(id='overpayment_graph')
])


@app.callback(
    Output('overpayment_graph', 'figure'),
    [Input('credit_size_id', 'value'),
    Input('rate_id', 'value')]
)
def update_overpayment_graph(credit_size, rate):
    try:
        payment_period, overpayment = get_overpayment_graph(credit_size, rate)
        return {
            'data': [
                {'x': payment_period, 'y': overpayment, 'name': 'overpayment'},
                {'x': payment_period, 'y': [credit_size] * 179, 'name': 'credit_size'}],
            'layout': {
                'height': 600, 'width': 800, 'title': 'overpayment dependence from period'}}
    except:
        return {
            'layout': {
                'height': 600, 'width': 800, 'title': 'overpayment dependence from period'}}


@app.callback(
    Output('month_graph', 'figure'),
    [Input('credit_size_id', 'value'),
    Input('rate_id', 'value'),
    Input('period_id', 'value'),
    Input('max_payment_size_id', 'value')]
)
def update_month_graph(credit_size, rate, period, max_payment_size):
    try:
        x_payment, y_payment, y_credit_body = get_month_graph(credit_size, rate, period, max_payment_size)
        return {
            'data': [
                {'x': x_payment, 'y': y_credit_body, 'type': 'bar', 'name': 'credit body'},
                {'x': x_payment, 'y': y_payment, 'type': 'bar', 'name': 'payments'}],
            'layout': {
                'height': 600, 'width': 800, 'title': 'month payment', 'barmode': 'stack'}}
    except:
        return {
            'layout': {'height': 600, 'width': 800, 'title': 'month payment'}}


if __name__ == "__main__":
    server.run(debug=True)
