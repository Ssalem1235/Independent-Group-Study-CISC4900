import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
csv_path = DATA_DIR / "ai_data.csv"

# Load dataset
df = pd.read_csv(
    csv_path,
    skipinitialspace=True,
    na_values=["", " ", "NA", "N/A"],
)

# Normalize column names
df.columns = df.columns.str.strip()

# Rename columns to easier names
df = df.rename(columns={
    "AI job postings (% of all job postings)": "ai_postings_pct",
    "Geographic area": "geo_area",
})

# --- CLEANING ---
df["Year"] = pd.to_numeric(df["Year"], errors="coerce").astype("Int64")

df["ai_postings_pct"] = (
    df["ai_postings_pct"]
    .astype("string")
    .str.strip()
    .str.replace("%", "", regex=False)
)
df["ai_postings_pct"] = pd.to_numeric(df["ai_postings_pct"], errors="coerce")

# Sort for analysis/plots
df = df.sort_values(["geo_area", "Year"])

# --- DESCRIPTIVE STATS ---
by_country = (
    df.dropna(subset=["ai_postings_pct"])
      .groupby("geo_area")["ai_postings_pct"]
      .describe()
      .sort_values("mean", ascending=False)
)

print("Descriptive statistics by country:")
print(by_country)

# Keep only rows with usable data
df_ts = df.dropna(subset=["ai_postings_pct"]).sort_values(["geo_area", "Year"])

# --- PLOT ---
plt.figure(figsize=(10, 6))

for country, group in df_ts.groupby("geo_area"):
    plt.plot(
        group["Year"],
        group["ai_postings_pct"],
        marker="o",
        linewidth=2,
        label=country
    )

plt.title("AI Job Postings as % of All Job Postings, by Country")
plt.xlabel("Year")
plt.ylabel("% of Job Postings")
plt.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(VISUALS_DIR / "ai_job_postings.png", dpi=150)
print("\nChart saved to visuals/ai_job_postings.png")
plt.show()
