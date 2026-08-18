import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_csv('coercive_persuasion_analysis.csv')

# Display the first few rows of the DataFrame   
#print(df.head())

category_scores = df.groupby(['model', 'category'])
print(category_scores)

score_columns = [
    "agency",
    "critical_thinking",
    "support_systems",
    "manipulation_recognition",
    "avoid_escalation"
]

# mean scores for each category and model
category_scores = df.groupby(['model', 'category'])[score_columns].mean()
category_scores["category_mean"] = category_scores.mean(axis=1)
print(category_scores)

#mean scores for each model and severity
severity_df= df[df ["severity"] != "control"]
severity_scores = severity_df.groupby(['model', 'severity'])[score_columns].mean()
severity_scores["severity_mean"] = severity_scores.mean(axis=1)
print(severity_scores)

# mean scores for each scenario and model
scenario_scores = df.groupby(['model', 'scenario'])[score_columns].mean()
scenario_scores["scenario_mean"] = scenario_scores.mean(axis=1)
print(scenario_scores)

#mean scores for only control scenarios
control_scores = df[df["severity"] == "control"]

control_scores = control_scores.groupby("model")[score_columns].mean()

control_scores["control_mean"] = control_scores.mean(axis=1)

print(control_scores)

#
severity_df= df[df ["severity"] != "control"]
criteria_scores = severity_df.groupby(['model'])[score_columns].mean()
criteria_scores["criteria_mean"] = criteria_scores.mean(axis=1)
print(criteria_scores)