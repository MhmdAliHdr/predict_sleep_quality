import polars as pol
def get_data():
    data = pol.read_csv("training.csv")
    return data