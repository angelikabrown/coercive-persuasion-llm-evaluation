import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('astra_gpt5_analysis.csv')

#first 5 rows of the dataframe
print(df.head())

#group the dataframe by model and category
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

# mean scores for each model and severity
severity_df= df[df ["severity"] != "control"]
severity_scores = severity_df.groupby(['model', 'severity'])[score_columns].mean()
severity_scores["severity_mean"] = severity_scores.mean(axis=1)
print(severity_scores)

# mean scores for each scenario and model
scenario_scores = df.groupby(['model', 'scenario'])[score_columns].mean()
scenario_scores["scenario_mean"] = scenario_scores.mean(axis=1)
print(scenario_scores)

# mean scores for only control scenarios
control_scores = df[df["severity"] == "control"]

control_scores = control_scores.groupby("model")[score_columns].mean()

control_scores["control_mean"] = control_scores.mean(axis=1)

print(control_scores)

# mean scores for only non-control scenarios
severity_df= df[df ["severity"] != "control"]
criteria_scores = severity_df.groupby(['model'])[score_columns].mean()
criteria_scores["criteria_mean"] = criteria_scores.mean(axis=1)
print(criteria_scores)


# Control vs. Severity visualization data

# Get the control mean for each model
control_viz = control_scores[["control_mean"]].copy()

# Get the overall mean across severity 1–5 for each model
severity_viz = severity_scores.groupby("model")["severity_mean"].mean()

# Combine control and severity means
control_viz = control_viz.join(severity_viz)

print(control_viz)

# Reshape for Seaborn
control_plot = control_viz.reset_index().melt(
    id_vars="model",
    var_name="condition",
    value_name="mean_score"
)

# Clean condition labels
control_plot["condition"] = control_plot["condition"].replace({
    "control_mean": "Control",
    "severity_mean": "Severity 1–5"
})

# Grouped bar plot
sns.barplot(
    data=control_plot,
    x="model",
    y="mean_score",
    hue="condition"
)

plt.title("Control vs. Severity Performance by Model")
plt.xlabel("Model")
plt.ylabel("Mean Score")
plt.ylim(0, 2)
plt.tight_layout()
plt.show()