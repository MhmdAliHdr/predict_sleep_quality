import pandas as pd
data = pd.read_csv("student_sleep_patterns.csv")
cleaned = data[["Age", "University_Year", "Sleep_Duration", "Study_Hours", "Screen_Time", "Caffeine_Intake", "Physical_Activity", "Sleep_Quality"]].replace("1st Year", 1).replace("2nd Year", 2).replace("3rd Year", 3).replace("4th Year", 4)
training = cleaned[:450]
testing = cleaned[450:]
training.to_csv("training.csv", index = False)
testing.to_csv("testing.csv", index = False)