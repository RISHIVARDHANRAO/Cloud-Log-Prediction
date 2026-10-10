import pandas as pd
from pathlib import Path

project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "Hdfs_structured.csv"

df = pd.read_csv(file_path)

print("\n========== DATASET OVERVIEW ==========")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

print("\n========== FIRST 10 ROWS ==========")
print(df.head(10).to_string())

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

print("\n========== LOG LEVEL DISTRIBUTION ==========")
if "Level" in df.columns:
    print(df["Level"].value_counts(dropna=False))

print("\n========== TOP 10 COMPONENTS ==========")
if "Component" in df.columns:
    print(df["Component"].value_counts().head(10))

print("\n========== TOP 10 EVENT TEMPLATES ==========")
if "EventTemplate" in df.columns:
    print(df["EventTemplate"].value_counts().head(10))