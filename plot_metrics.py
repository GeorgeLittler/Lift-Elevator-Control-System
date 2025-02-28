import pandas as pd
import matplotlib.pyplot as plt
import os

data_dir = "results/data/"
output_dir = "results/charts/"
os.makedirs(output_dir, exist_ok=True)

# Ensure the overall performance file exists
overall_performance_file = os.path.join(data_dir, "lift_performance.csv")
if os.path.exists(overall_performance_file):
    performance_df = pd.read_csv(overall_performance_file)
else:
    print("Overall performance data not found. Exiting...")
    exit()

# performing aggregation on the entire file
performance_df = performance_df.groupby("Algorithm", as_index=False).agg({
    "Avg_Wait_Time": "mean",        # wait time
    "Requests_Served": "sum",       # requests served
    "Efficiency_Score": "mean"      # efficiency score
})

# bar charts
def save_bar_chart(x, y, xlabel, ylabel, title, filename, colors):
    plt.figure(figsize=(8, 5))
    plt.bar(x, y, color=colors)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# line charts
def save_line_chart(x, y, xlabel, ylabel, title, filename, color):
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, marker='o', linestyle='-', color=color)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid()
    plt.savefig(os.path.join(output_dir, filename))
    plt.close()

# Generate overall performance charts
save_bar_chart(performance_df["Algorithm"], performance_df["Avg_Wait_Time"],
               "Algorithm", "Average Wait Time (s)", "Overall Average Wait Time per Algorithm",
               "avg_wait_time.png", ["blue", "green", "red"])

save_bar_chart(performance_df["Algorithm"], performance_df["Requests_Served"],
               "Algorithm", "Requests Served", "Overall Requests Served per Algorithm",
               "requests_served.png", ["blue", "green", "red"])

save_line_chart(performance_df["Algorithm"], performance_df["Efficiency_Score"],
                "Algorithm", "Efficiency Score", "Overall Efficiency Score Comparison",
                "efficiency_score.png", "purple")

# Generate charts for each input separately
for i in range(1, 4):
    input_file = os.path.join(data_dir, f"lift_performance_input{i}.csv")

    if not os.path.exists(input_file):
        print(f"Warning: {input_file} not found. Skipping...")
        continue

    input_df = pd.read_csv(input_file)
    input_df_aggregated = input_df.groupby("Algorithm", as_index=False).agg({
        "Avg_Wait_Time": "mean",        #  wait time 
        "Requests_Served": "sum",       #  sum total requests
        "Efficiency_Score": "mean"      #  efficiency score 
    })

    # generate and save charts
    save_bar_chart(input_df_aggregated["Algorithm"], input_df_aggregated["Avg_Wait_Time"],
                   "Algorithm", "Average Wait Time (s)", f"Average Wait Time for Input {i}",
                   f"avg_wait_time_input{i}.png", ["blue", "green", "red"])

    save_bar_chart(input_df_aggregated["Algorithm"], input_df_aggregated["Requests_Served"],
                   "Algorithm", "Requests Served", f"Requests Served for Input {i}",
                   f"requests_served_input{i}.png", ["blue", "green", "red"])

    save_line_chart(input_df_aggregated["Algorithm"], input_df_aggregated["Efficiency_Score"],
                    "Algorithm", "Efficiency Score", f"Efficiency Score for Input {i}",
                    f"efficiency_score_input{i}.png", "purple")

print("✅ Charts saved in results/charts/")
