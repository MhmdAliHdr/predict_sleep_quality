import dash
from dash import callback, dcc, html, Input, Output
from model import make_model
import plotly.express as px
from plotly.graph_objects import Layout
from fetch_data import get_data
model = make_model()
data = get_data()
choice = "Age"
chosen_columns = data[[choice, "Sleep_Quality"]]
res = chosen_columns.group_by(list(chosen_columns.columns)).len()
choice_values = res["Age"]
sleep_quality = res["Sleep_Quality"]
counts = res["len"]
fig = px.scatter(x = choice_values, y = sleep_quality, size = counts, color_continuous_scale="brwnyl", color=counts)
fig.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
dashboard = dash.Dash()
dashboard.title = "Student Sleep Quality"
dashboard.layout = html.Div(
    children = [
        html.H1("Student Sleep Quality", style={"text-align": "center"}),
        dcc.Graph(id = "scatter", figure=fig),
        dcc.Dropdown(id = "selection",
                     options = [
                         {"label": "Age", "value": "Age"},
                         {"label": "University Year", "value": "University_Year"},
                         {"label": "Sleep Duration", "value": "Sleep_Duration"},
                         {"label": "Study Hours", "value": "Study_Hours"},
                         {"label": "Caffeince Intake", "value": "Caffeine_Intake"},
                         {"label": "Physical Activity", "value": "Physical_Activity"},
                     ],
                     placeholder="Select Data to Visualize"),
        html.Div(
            "Predict your sleep quality:"
        ),
        dcc.Input(
            id="prediction"
        ),
        html.Div([
            dcc.Input(id = "age",  value = 0, placeholder= "Enter an age", type="number"),
            dcc.Input(id = "year", value = 0, placeholder= "University Year", type="number"),
            dcc.Input(id = "duration", value = 0, placeholder= "Sleep Duration", type="number"),
            dcc.Input(id = "study", value = 0, placeholder= "Study Hours", type="number"),
            dcc.Input(id = "screen", value = 0, placeholder= "Screen Time", type="number"),
            dcc.Input(id = "caffeine", value = 0, placeholder= "Caffeine Intake", type="number"),
            dcc.Input(id = "physical", value = 0, placeholder= "Physical Activity", type="number"),
        ])
    ]
, style={"background-color": "#9e6c52", "color": "#ffffff"})
@dashboard.callback(
    Output("scatter", "figure"),
    Input("selection", "value"))
def update_figure(selection):
    choice = selection
    chosen_columns = data[[choice, "Sleep_Quality"]]
    res = chosen_columns.group_by(list(chosen_columns.columns)).len()
    choice_values = res[choice]
    sleep_quality = res["Sleep_Quality"]
    counts = res["len"]
    fig = px.scatter(x = choice_values, y = sleep_quality, size = counts, color_continuous_scale="brwnyl", color=counts)
    fig.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
    fig.update_layout(transition_duration=40)
    return fig
@dashboard.callback(
    Output("prediction", "value"),
    [Input("age", "value"), Input("year", "value"), Input("duration", "value"), Input("study", "value"), Input("screen", "value"), Input("caffeine", "value"), Input("physical", "value")]
)
def predict(age, year, duration, study, screen, caffeine, physical):
    p = model.predict([[age, year, duration, study, screen, caffeine, physical]])
    print(p)
    return p
dashboard.run()