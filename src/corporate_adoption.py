"""
corporate_adoption.py
---------------------
Analyzes organizational AI adoption rates over time.

Data Source:
  Stanford AI Index 2025, Chapter 4 (Economy)
  Underlying survey data: McKinsey Global Survey on AI
  URL: https://hai.stanford.edu/ai-index/2025-ai-index-report

  CSV columns: Year, % of respondents, Label
    Label = "AI"    means % of orgs using AI in any business function
    Label = "GenAI" means % of orgs using generative AI specifically

Why this is original analysis:
  We plot the full 2017-2024 trend and overlay both AI and GenAI adoption
  on the same chart. We also calculate year-over-year growth rates.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
CSV_PATH    = DATA_DIR / "corporate_adoption.csv"

# Load data
if not CSV_PATH.exists():
    raise FileNotFoundError("Could not find corporate_adoption.csv in data folder.")

df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip()
print("Loaded corporate_adoption.csv")

# Clean the percentage column - strip % sign and convert to number
df["% of respondents"] = df["% of respondents"].astype(str).str.replace("%", "").str.strip()
df["% of respondents"] = pd.to_numeric(df["% of respondents"], errors="coerce")

# Split into general AI vs generative AI using the Label column
ai_df  = df[df["Label"] == "AI"][["Year", "% of respondents"]].copy()
gen_df = df[df["Label"] == "GenAI"][["Year", "% of respondents"]].copy()

ai_df  = ai_df.rename(columns={"Year": "year", "% of respondents": "adoption_pct"})
gen_df = gen_df.rename(columns={"Year": "year", "% of respondents": "gen_ai_pct"})

ai_df  = ai_df.sort_values("year").reset_index(drop=True)
gen_df = gen_df.sort_values("year").reset_index(drop=True)

# Print summary stats
print("\nAI Adoption Rate by Year:")
print(ai_df.to_string(index=False))

ai_df["yoy_change"] = ai_df["adoption_pct"].diff()
print("\nYear-over-year change (percentage points):")
print(ai_df[["year", "adoption_pct", "yoy_change"]].dropna().to_string(index=False))

print("\nGenerative AI Adoption:")
print(gen_df.to_string(index=False))

# Save a clean version for summary_analysis.py
ai_df[["year", "adoption_pct"]].to_csv(DATA_DIR / "corporate_adoption_clean.csv", index=False)
print("\nClean version saved to data/corporate_adoption_clean.csv")

# Plot
plt.figure(figsize=(10, 6))

plt.plot(ai_df["year"], ai_df["adoption_pct"],
         marker="o", linewidth=2, label="Any AI adoption", color="steelblue")

if not gen_df.empty:
    plt.plot(gen_df["year"], gen_df["gen_ai_pct"],
             marker="s", linewidth=2, linestyle="--",
             label="Generative AI specifically", color="tomato")

# Mark ChatGPT launch
plt.axvline(x=2022.9, color="red", linewidth=1, linestyle=":", alpha=0.5)
plt.text(2023.0, 25, "ChatGPT\n(Nov 2022)", fontsize=8, color="red")

# Annotate the big 2023-2024 jump
plt.annotate(
    "+23pp in one year",
    xy=(2024, 78), xytext=(2022.3, 82),
    fontsize=9,
    arrowprops=dict(arrowstyle="->", color="black")
)

# Add value labels on the main line
for _, row in ai_df.iterrows():
    plt.text(row["year"], row["adoption_pct"] + 1.5,
             f"{row['adoption_pct']:.0f}%", ha="center", fontsize=8)

plt.title("Organizational AI Adoption Rate, 2017-2024")
plt.xlabel("Year")
plt.ylabel("% of Organizations Using AI")
plt.xticks(ai_df["year"])
plt.ylim(0, 95)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(VISUALS_DIR / "corporate_adoption.png", dpi=150)
print("\nChart saved to visuals/corporate_adoption.png")
plt.show()