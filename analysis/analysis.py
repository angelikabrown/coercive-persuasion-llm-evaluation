import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_csv('coercive_persuasion_analysis.csv')
 
print(df.head())

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

# Visualization the df
#Criteria Scores by Model
criteria_plot = criteria_scores.drop(columns="criteria_mean").reset_index()

criteria_plot = criteria_plot.melt(
    id_vars="model",
    var_name="criterion",
    value_name="mean_score"
)
criteria_plot["model"] = criteria_plot["model"].replace({
    "openai/gpt-5.2": "GPT-5.2",
    "anthropic/claude-sonnet-4-6": "Claude 4.6",
    "google/gemini-3.6-flash": "Gemini 3.6 Flash"
})

criteria_plot["criterion"] = criteria_plot["criterion"].replace({
    "agency": "Agency",
    "critical_thinking": "Critical Thinking",
    "support_systems": "Support Systems",
    "manipulation_recognition": "Manipulation Recognition",
    "avoid_escalation": "Avoid Escalation"
})

print(criteria_plot)



# Model Performance by Criterion
sns.barplot(
    data=criteria_plot,
    x="criterion",
    y="mean_score",
    hue="model"
)
plt.ylim(0, 2)
plt.title("Model Performance by Criterion")
plt.xlabel("Criterion")
plt.ylabel("Mean Score")
plt.tight_layout()
plt.show()





# Model Performance by Severity
severity_scores = severity_scores.reset_index()

severity_scores["model"] = severity_scores["model"].replace({
    "openai/gpt-5.2": "GPT-5.2",
    "anthropic/claude-sonnet-4-6": "Claude 4.6",
    "google/gemini-3.6-flash": "Gemini 3.6 Flash"
})
sns.lineplot(
    data=severity_scores,
    x="severity",
    y="severity_mean",
    hue="model"
)
plt.title("Model Performance by Severity")
plt.xlabel("Severity Level")
plt.ylabel("Mean Score")
plt.tight_layout()
plt.show()


# Control vs. Severity visualization data

# Get the control mean for each model
control_viz = control_scores[["control_mean"]].copy()

# Get the overall mean across severity 1–5 for each model
severity_viz = severity_scores.groupby("model")["severity_mean"].mean()

# Make sure the model names match before joining
severity_viz.index = severity_viz.index.map({
    "Claude 4.6": "anthropic/claude-sonnet-4-6",
    "Gemini 3.6 Flash": "google/gemini-3.6-flash",
    "GPT-5.2": "openai/gpt-5.2"
})

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

# Clean model names for presentation
control_plot["model"] = control_plot["model"].replace({
    "openai/gpt-5.2": "GPT-5.2",
    "anthropic/claude-sonnet-4-6": "Claude 4.6",
    "google/gemini-3.6-flash": "Gemini 3.6 Flash"
})

#print(control_plot)

#grouped bar plot for control vs severity
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

#Line chart -- Manipulation Recognition by Severity
sns.lineplot(
    data=severity_scores,
    x="severity",
    y="manipulation_recognition",
    hue="model",
    marker="o"
)

plt.ylim(0, 2.1)
plt.title("Manipulation Recognition by Severity")
plt.xlabel("Severity Level")
plt.ylabel("Mean Score")
plt.tight_layout()
plt.show()