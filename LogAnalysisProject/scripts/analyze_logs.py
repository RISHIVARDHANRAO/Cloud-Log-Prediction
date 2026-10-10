import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
data_path = project_dir / "data" / "Hdfs_structured.csv"
output_dir = project_dir / "output"

output_dir.mkdir(exist_ok=True)

df = pd.read_csv(data_path)

print("=" * 50)
print("CLOUD-BASED LOG ANALYTICS")
print("=" * 50)

print("\n1. DATASET SUMMARY")
print("-" * 30)
print(f"Total log entries: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Missing values: {df.isnull().sum().sum()}")

print("\n2. LOG LEVEL DISTRIBUTION")
print("-" * 30)
level_counts = df["Level"].value_counts()
print(level_counts)

print("\n3. COMPONENT ANALYSIS")
print("-" * 30)
component_counts = df["Component"].value_counts()
print(component_counts)

print("\n4. TOP 10 EVENT TEMPLATES")
print("-" * 30)
event_counts = df["EventTemplate"].value_counts().head(10)
print(event_counts)

print("\n5. WARN LOG ANALYSIS")
print("-" * 30)
warn_logs = df[df["Level"].str.upper() == "WARN"]

print(f"Total WARN logs: {len(warn_logs)}")

if not warn_logs.empty:
    print("\nWARN logs by component:")
    print(warn_logs["Component"].value_counts())

    print("\nWARN event templates:")
    print(warn_logs["EventTemplate"].value_counts())

print("\n6. EVENT FREQUENCY")
print("-" * 30)
event_id_counts = df["EventId"].value_counts()
print(event_id_counts.head(10))

summary = pd.DataFrame({
    "Metric": [
        "Total Logs",
        "Total Components",
        "Unique Event IDs",
        "Missing Values",
        "INFO Logs",
        "WARN Logs"
    ],
    "Value": [
        len(df),
        df["Component"].nunique(),
        df["EventId"].nunique(),
        df.isnull().sum().sum(),
        (df["Level"].str.upper() == "INFO").sum(),
        (df["Level"].str.upper() == "WARN").sum()
    ]
})

summary.to_csv(output_dir / "summary.csv", index=False)
level_counts.rename_axis("Level").reset_index(
    name="Count"
).to_csv(output_dir / "level_distribution.csv", index=False)

component_counts.rename_axis("Component").reset_index(
    name="Count"
).to_csv(output_dir / "component_distribution.csv", index=False)

event_counts.rename_axis("EventTemplate").reset_index(
    name="Count"
).to_csv(output_dir / "top_events.csv", index=False)

warn_logs.to_csv(output_dir / "warn_logs.csv", index=False)

print("\n" + "=" * 50)
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("Results saved in the output folder.")
print("=" * 50)