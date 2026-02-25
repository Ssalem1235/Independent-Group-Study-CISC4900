import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "ai_data.csv"

# Load dataset (more robust CSV reading)
df = pd.read_csv(
    csv_path,
    skipinitialspace=True,     # trims spaces after delimiters
    na_values=["", " ", "NA", "N/A"],  # treat blanks as NaN
)

# Optional: normalize column names (remove accidental whitespace)
df.columns = df.columns.str.strip()

print("Raw Data:")
print(df.head())

# Rename columns to easier names (recommended)
df = df.rename(columns={
    "AI job postings (% of all job postings)": "ai_postings_pct",
    "Geographic area": "geo_area",
})

# --- CLEANING ---
# Year -> integer (nullable)
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

# Percent column -> float (e.g., 1.28 for 1.28%)
df["ai_postings_pct"] = (
    df["ai_postings_pct"]
    .astype("string")              # safe for mixed types
    .str.strip()
    .str.replace("%", "", regex=False)
)
df["ai_postings_pct"] = pd.to_numeric(df["ai_postings_pct"], errors="coerce")

print("\nCleaned Data:")
print(df.head())

print("\nMissing values by column:")
print(df.isna().sum())

print("\nData types:")
print(df.dtypes)

# Optional basic checks
if df["Year"].isna().any():
    print("\nWARNING: Some Year values could not be parsed.")

# Sort for analysis/plots
df = df.sort_values(["geo_area", "Year"])

print("\nRUNNING DESCRIPTIVE STATS SECTION")

# ===== DESCRIPTIVE STATISTICS BY COUNTRY =====
by_country = (
    df.dropna(subset=["ai_postings_pct"])
      .groupby("geo_area")["ai_postings_pct"]
      .describe()
      .sort_values("mean", ascending=False)
)

print("\nDescriptive statistics by country:")
print(by_country)

# Keep only rows with usable data
df_ts = (
    df.dropna(subset=["ai_postings_pct"])
      .sort_values(["geo_area", "Year"])
)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

for country, group in df_ts.groupby("geo_area"):
    plt.plot(
        group["Year"],
        group["ai_postings_pct"],
        marker="o",
        label=country
    )

plt.title("AI job postings as % of all job postings (by country)")
plt.xlabel("Year")
plt.ylabel("Percent of job postings")
plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True)
plt.tight_layout()
plt.show()