import dash
from dash import callback, dcc, html, Input, Output
from model import make_model
import plotly.express as px
from plotly.graph_objects import Layout
from fetch_data import get_data
import pandas as pd
model = make_model()
data = get_data()
choice = "Age"
chosen_columns = data[[choice, "Sleep_Quality"]]
res = chosen_columns.group_by(list(chosen_columns.columns)).len()
choice_values = res["Age"]
sleep_quality = res["Sleep_Quality"]
counts = res["len"]
d = {choice: choice_values, "Sleep Quality": sleep_quality, "Number of Students": counts}
df = pd.DataFrame(d)
fig = px.scatter(df, x = "Age", y = "Sleep Quality", size = "Number of Students")
fig.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
dashboard = dash.Dash()
server = dashboard.server
dashboard.title = "Student Sleep Quality"
dashboard.layout = html.Div(
    children = [
        html.Div(id="figure", children= [
        html.Img(src="https://res.cloudinary.com/s7eflphu/image/upload/v1792844722/Logo_c0ogvn.png", style={"width": "80%", "scale": "80%", "padding-left": "10%"}),
        dcc.Dropdown(id = "selection",
                     options = [
                         {"label": "Age", "value": "Age"},
                         {"label": "University Year", "value": "University_Year"},
                         {"label": "Sleep Duration", "value": "Sleep_Duration"},
                         {"label": "Study Hours", "value": "Study_Hours"},
                         {"label": "Caffeine Intake", "value": "Caffeine_Intake"},
                         {"label": "Physical Activity", "value": "Physical_Activity"},
        ], value="Age",
        placeholder="Select Data to Visualize", style={"color": "#120c08"}),
        dcc.Dropdown(id = "visualization",
                     options = [
                         {"label": "Scatterplot", "value": "Scatter"},
                         {"label": "Heatmap", "value": "Heatmap"}
        ], value="Scatter",
        placeholder="Select How to Visualize", style={"color": "#2e2f53"}),
        dcc.Graph(id = "scatter", figure=fig)], style={"background-color": "#f7f7f7", "width":"80%", "margin-left": "auto", "margin-right": "auto", "border-top-left-radius": "25%", "border-top-right-radius": "25%"}),
        html.Div([
        html.Div(
            "Predict your sleep quality:"
        , style={"font-size": "30px", "padding-top": "3%", "margin-top": "-3%", "text-align": "center"}),
        dcc.Input(
            id="prediction"
        , style={"font-size": "26px", "background-color": "#f7f7f7", "border": "None", "margin-left": "48.5%", "color": "#2e2f53"}),
        html.Div([
            html.Div("Age:"),
            dcc.Input(id = "age",  value = 0, placeholder= "Enter an age", type="number"),
            html.Div("University Year:"),
            dcc.Input(id = "year", value = 0, placeholder= "University Year", type="number"),
            html.Div("Sleep Duration:"),
            dcc.Input(id = "duration", value = 0, placeholder= "Sleep Duration", type="number"),
            html.Div("Study Hours:"),
            dcc.Input(id = "study", value = 0, placeholder= "Study Hours", type="number"),
            html.Div("Screen Time:"),
            dcc.Input(id = "screen", value = 0, placeholder= "Screen Time", type="number"),
            html.Div("Caffeine Intake:"),
            dcc.Input(id = "caffeine", value = 0, placeholder= "Caffeine Intake", type="number"),
            html.Div("Physical Activity:"),
            dcc.Input(id = "physical", value = 0, placeholder= "Physical Activity", type="number", style={"margin-bottom": "2%"}),
        ], style={"text-align": "center"})], style={"color": "#2e2f53", "background-color": "#f7f7f7", "padding-bottom": "3%", "width":"80%", "margin-left": "auto", "margin-right": "auto", "border-bottom-left-radius": "25%","border-bottom-right-radius": "25%"})
    ]
, style={"background-color": "#2e2f53", "color": "#ffffff"})
@dashboard.callback(
    Output("scatter", "figure"),
    [Input("selection", "value"), Input("visualization", "value")])
def update_figure(selection, visualization):
    choice = selection.replace(" ", "_")
    chosen_columns = data[[choice, "Sleep_Quality"]]
    res = chosen_columns.group_by(list(chosen_columns.columns)).len()
    choice_values = res[choice]
    sleep_quality = res["Sleep_Quality"]
    counts = res["len"]
    d = {choice: choice_values, "Sleep Quality": sleep_quality, "Number of Students": counts}
    df = pd.DataFrame(d)
    if(visualization == "Scatter"):
        fig = px.scatter(df, x = choice, y = "Sleep Quality", size = "Number of Students", trendline_color_override="#ffffff")
    elif(visualization == "Heatmap"):
        fig = px.density_heatmap(df, x = choice, y = "Sleep Quality", color_continuous_scale="YlGnBu")
    fig.update_layout(paper_bgcolor="rgba(0, 0, 0, 0)")
    fig.update_layout(transition_duration=40)
    return fig
@dashboard.callback(
    Output("prediction", "value"),
    [Input("age", "value"), Input("year", "value"), Input("duration", "value"), Input("study", "value"), Input("screen", "value"), Input("caffeine", "value"), Input("physical", "value")]
)
def predict(age, year, duration, study, screen, caffeine, physical):
    p = model.predict([[age, year, duration, study, screen, caffeine, physical]])
    return p
dashboard.run(host="0.0.0.0", port="10000")