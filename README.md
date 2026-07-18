# Predict Sleep Quality
This is a dashboard created using Plotly and Dash in Python to visualize the synthesized dataset found in: https://www.kaggle.com/datasets/arsalanjamal002/student-sleep-patterns.
The dataset showcases multiple features regarding a university student's lifestyle, with a label in the range [1, 10] describing the quality of their sleep. 1 being the lowest, 10 being the best.
The goal of this project is to experiment with constructing a dataset visualizer using Plotly and Dash, combined with a machine learning model. Such an application can be built for a variety of datasets, allowing users to do without the nitty-gritty of manually inspecting datasets.
### A live demo can be seen at: https://predict-sleep-quality-1.onrender.com
## Visualization
Users can select a feature (University Year, Sleep Duration, Caffeine intake, and so on) and a type of graph (Scatterplot, Bar graph, or a line graph) to visualize the correlation between the impact of said feature on the quality of sleep of a student.
## KNN Model
At the lower part of the page, a user, likely a university student, can enter their own data, and predict their own sleep quality. This aspect of the application makes use of Scikit-Learn's KNN (K-Nearest Neighbors) model, trained on the same dataset, in order to propose a prediction.
## Some Notes
Our choice to use a KNN model is for simplicity, Scikit-Learn provides an array of different models possible to use (linear regression for example) without much difference in training steps at the programming level.
