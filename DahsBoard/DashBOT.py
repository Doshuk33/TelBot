import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Создать дашборд
app = dash.Dash(__name__)

# Добавить интерактивные элементы
app.layout = html.Div([
    html.H1('Дашборд по работе с клиентами'),
    html.P('Этот дашборд показывает данные по работе с клиентами'),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Причина ухода', 'value': 'eason'},
            {'label': 'Отзыв', 'value': 'feedback'},
            {'label': 'Оценка', 'value': 'rate'}
        ],
        value='reason'
    ),
    dcc.Graph(id='graph'),
    dcc.Slider(
        id='slider',
        min=0,
        max=100,
        step=1,
        value=50
    ),
    dcc.Input(
        id='input',
        type='text',
        placeholder='Введите текст'
    ),
    dcc.DatePickerRange(
        id='date-picker',
        start_date_placeholder_text='Выберите дату начала',
        end_date_placeholder_text='Выберите дату окончания'
    ),
    dcc.Dropdown(
        id='category-dropdown',
        options=[
            {'label': 'Все категории', 'value': 'all'},
            {'label': 'Категория 1', 'value': 'category1'},
            {'label': 'Категория 2', 'value': 'category2'}
        ],
        value='all'
    )
])

# Добавить функцию обратного вызова для обновления графика
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown', 'value')]
)
def update_graph(selected_value):
    df = pd.DataFrame({
        'eason': ['Причина 1', 'Причина 2', 'Причина 3'],
        'feedback': ['Отзыв 1', 'Отзыв 2', 'Отзыв 3'],
        'rate': [1, 2, 3]
    })
    fig = px.bar(x=df[selected_value], y=df['rate'])
    return fig

# Запустить дашборд
if __name__ == '__main__':
    app.run_server(debug=True)