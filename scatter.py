import plotly.express as px
def scatter_plot(x, y, column):
    print(list(x[column]))
    fig = px.scatter(list(x[column]), list(y))
    return fig