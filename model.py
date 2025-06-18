
import polars as pol
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
# Read the training dataset
def make_model():
    training_features = pol.read_csv("training.csv")[["Age", "University_Year", "Sleep_Duration", "Study_Hours", "Screen_Time", "Caffeine_Intake", "Physical_Activity"]]
    training_labels = pol.read_csv("training.csv")["Sleep_Quality"]
    neigh = KNeighborsClassifier(n_neighbors=3)
    neigh.fit(training_features.to_numpy(), training_labels.to_numpy())
    return neigh