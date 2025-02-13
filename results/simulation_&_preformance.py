import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Fix seed for reproducibility
np.random.seed(42)

num_requests = 500 
num_floors = 10 
algorithms = ["SCAN", "LOOK", "MYLIFT"]

#generate random requests
requests = pd.DataFrame({
    "Request_Time": np.random.randint(0, 300, size=num_requests),#request made at (0-300s)
    "Start_Floor": np.random.randint(1, num_floors + 1, size=num_requests),
    "End_Floor": np.random.randint(1, num_floors + 1, size=num_requests),
    "Algorithm": np.random.choice(algorithms, size=num_requests)
})

requests = requests[requests["Start_Floor"] != requests["End_Floor"]].reset_index(drop=True)#remove cases where Start Floor == End Floor

print("Sample Requests:\n", requests.head())


def calculate_lift_metrics(df):
    results = []

    for algo in df["Algorithm"].unique():
        subset = df[df["Algorithm"] == algo]

        #wait time
        subset["Wait_Time"] = np.abs(subset["End_Floor"] - subset["Start_Floor"]) * 2  # Assume 2s per floor

        avg_wait_time = subset["Wait_Time"].mean()
        requests_served = len(subset)

        #efficiency Score
        efficiency_score = (requests_served / max(df["Request_Time"])) * 100 - avg_wait_time

        results.append({
            "Algorithm": algo,
            "Avg_Wait_Time": avg_wait_time,
            "Requests_Served": requests_served,
            "Efficiency_Score": efficiency_score
        })

    return pd.DataFrame(results)

# Compute metrics
performance_df = calculate_lift_metrics(requests)

# Save metrics to CSV for further analysis
performance_df.to_csv("lift_performance.csv", index=False)

print("Performance Metrics:\n", performance_df)