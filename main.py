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
server = dashboard.server
dashboard.title = "Student Sleep Quality"
dashboard.layout = html.Div(
    children = [
        html.Div(id="figure", children= [
        html.Div("Student Sleep Quality", style={"color": "#120c08", "text-align": "center", "font-size": "30px"}),
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
                         {"label": "Bar Graph", "value": "Bar"},
                         {"label": "Line", "value": "Line"}
        ], value="Scatter",
        placeholder="Select How to Visualize", style={"color": "#120c08"}),
        dcc.Graph(id = "scatter", figure=fig)], style={"background-color": "#ddcdc6", "width":"50%", "margin-left": "25%"}),
        html.Div([
        html.Div(
            "Predict your sleep quality:"
        , style={"font-size": "30px", "margin-top": "-3%", "text-align": "center"}),
        dcc.Input(
            id="prediction"
        , style={"font-size": "26px", "background-color": "#ddcdc6", "border": "None", "margin-left": "48.5%", "color": "#ffffff"}),
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
        ], style={"text-align": "center"})], style={"color": "#120c08", "background-color": "#ddcdc6", "width":"50%", "margin-left": "25%"})
    ]
, style={"background-image": "url(pexels-mdsnmdsnmdsn-1405761.jpg)", "color": "#ffffff"})
@dashboard.callback(
    Output("scatter", "figure"),
    [Input("selection", "value"), Input("visualization", "value")])
def update_figure(selection, visualization):
    choice = selection
    chosen_columns = data[[choice, "Sleep_Quality"]]
    res = chosen_columns.group_by(list(chosen_columns.columns)).len()
    choice_values = res[choice]
    sleep_quality = res["Sleep_Quality"]
    counts = res["len"]
    if(visualization == "Scatter"):
        fig = px.scatter(x = choice_values, y = sleep_quality, size = counts, color_continuous_scale="brwnyl", color=counts)
    elif(visualization == "Bar"):
        fig = px.bar(x = [str(i) for i in list(zip(choice_values, sleep_quality))], y = counts, color_discrete_sequence=["#ceb397", "#c6a686", "#b68c63",
                                                                                                                          "#8b6641", "#684d31", "#574029",
                                                                                                                          "#453321", "#342618", "#231a10", "#110d08", "#231910", "#120c08", "#7b5637", "#b88861"], color=counts)
    elif(visualization == "Line"):
        fig = px.line(x = [str(i) for i in list(zip(choice_values, sleep_quality))], y = counts, color_discrete_sequence=["#c6a686"])
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