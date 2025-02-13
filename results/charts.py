import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for better visuals
sns.set_theme(style="whitegrid")

# Load the dataset
file_path = "....."

try:
    df = pd.read_csv(file_path)
    
    # Ensure correct data types
    df["Avg_Wait_Time"] = pd.to_numeric(df["Avg_Wait_Time"], errors="coerce")
    df["Requests_Served"] = pd.to_numeric(df["Requests_Served"], errors="coerce")
    df["Efficiency_Score"] = pd.to_numeric(df["Efficiency_Score"], errors="coerce")
    
    print("Data Loaded Successfully:\n", df.head())

    # Bar chart for Average Wait Time
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Algorithm", y="Avg_Wait_Time", data=df, palette="Blues")
    plt.title("Average Wait Time per Algorithm")
    plt.xlabel("Algorithm")
    plt.ylabel("Average Wait Time (seconds)")
    plt.show()

    # Bar chart for Requests Served
    plt.figure(figsize=(8, 5))
    sns.barplot(x="Algorithm", y="Requests_Served", data=df, palette="Greens")
    plt.title("Number of Requests Served per Algorithm")
    plt.xlabel("Algorithm")
    plt.ylabel("Requests Served")
    plt.show()

    # Line plot for Efficiency Score
    plt.figure(figsize=(8, 5))
    sns.lineplot(x="Algorithm", y="Efficiency_Score", data=df, marker="o", linewidth=2.5, color="red")
    plt.title("Efficiency Score Comparison")
    plt.xlabel("Algorithm")
    plt.ylabel("Efficiency Score")
    plt.show()

except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print("Error: The file is empty.")
except Exception as e:
    print(f"An error occurred: {e}")
