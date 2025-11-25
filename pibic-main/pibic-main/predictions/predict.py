import joblib
import lime.lime_tabular
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import base64
import io

model = joblib.load("model_ML/LR.joblib")

train = pd.read_csv("files/X_train.csv")[[
    "Pre-Hematocrit", "Pre-Hemoglobin","Pre-Lactate", "Height (m)", "Reoperation",
    "CPB Time (minutes)", "Anoxia Time (minutes)", "Female",
    "Normothermia"
]]

feature_names = list(train.columns)

class_names = ["Sem Hiperlactatemia", "Com Hiperlactatemia"]

explainer = lime.lime_tabular.LimeTabularExplainer(
    train.values,
    feature_names=feature_names,
    class_names=class_names,
    discretize_continuous=True
)

def explain_instance(instance):
    exp = explainer.explain_instance(np.array(instance), model.predict_proba, num_features=10)
    return exp

def prepare_features_and_values(exp):
    exp_features = exp.as_list()
    features, values = zip(*exp_features)
    return features[::-1], values[::-1]

def assign_colors(values):
    return ['red' if val > 0 else 'green' for val in values]

def create_plot(features, values, colors):
    fig, ax = plt.subplots()
    y_pos = np.arange(len(features))
    ax.barh(y_pos, values, color=colors, align='center')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(features)
    ax.invert_yaxis()
    ax.set_xlabel('Contribuição da Feature')
    ax.set_ylabel('Features')
    ax.set_title('Importância das Features na Predição')
    return fig

def predict_and_explain(pre_hematocrit, pre_hemoglobin,pre_lactate, height, redo, cpb, anoxia, female, normothermia):
    instance_dict = {
        "Pre-Hematocrit": [float(pre_hematocrit)],
        "Pre-Hemoglobin": [float(pre_hemoglobin)],
        "Pre-Lactate": [float(pre_lactate)],
        "Height (m)": [float(height)],
        "Reoperation": [int(redo)],
        "CPB Time (minutes)": [float(cpb)],
        "Anoxia Time (minutes)": [float(anoxia)],
        "Female": [int(female)],
        "Normothermia": [int(normothermia)]
    }

    instance_df = pd.DataFrame(instance_dict)

    prediction = model.predict(instance_df)[0]
    prob = model.predict_proba(instance_df)[0][1]

    exp = explain_instance(instance_df.iloc[0].to_numpy())
    features_plot, values = prepare_features_and_values(exp)
    colors = assign_colors(values)
    fig = create_plot(features_plot, values, colors)

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return prob, prediction, image_base64
