"""
attitudes_analysis.py
---------------------
Analyzes shifts in U.S. public sentiment toward AI using Pew Research
Center survey data (2021-2024).

Data Source:
  Pew Research Center - American Trends Panel
  URL: https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/

  How the CSV was built:
  Pew does not offer direct CSV downloads for all survey waves.
  Values were manually extracted from four published Pew reports:

  2021: pewresearch.org/internet/2022/03/17/ai-and-human-enhancement...
  2022: Same report as above, tracking table
  2023: pewresearch.org/short-reads/2023/11/21/what-the-data-says...
  2024: pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts...

Why this is original analysis:
  No single Pew report shows all four years on one chart.
  We also calculate the percentage point change across years.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# File paths
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
CSV_PATH    = DATA_DIR / "pew_attitudes.csv"

# Load data
if CSV_PATH.exists():
    df = pd.read_csv(CSV_PATH)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    print("Loaded pew_attitudes.csv")
else:
    # Values manually extracted from Pew Research Center reports
    df = pd.DataFrame({
        "year":           [2021, 2022, 2023, 2024],
        "more_concerned": [  37,   38,   52,   52],
        "more_excited":   [  18,   15,   10,   13],
        "equal_mixed":    [  45,   47,   38,   35],
    })
    df.to_csv(CSV_PATH, index=False)
    print("No CSV found - using manually extracted Pew values. Saved to pew_attitudes.csv")

df = df.sort_values("year").reset_index(drop=True)

# Print summary
print("\nPew Sentiment Data:")
print(df[["year", "more_concerned", "more_excited", "equal_mixed"]].to_string(index=False))

# Calculate percentage point changes (our own calculation)
concerned_change = df["more_concerned"].iloc[-1] - df["more_concerned"].iloc[0]
excited_change   = df["more_excited"].iloc[-1]   - df["more_excited"].iloc[0]
print(f"\n'More concerned' changed by {concerned_change:+.0f} percentage points (2021-2024)")
print(f"'More excited'   changed by {excited_change:+.0f} percentage points (2021-2024)")

# Plot - grouped bar chart
x = np.arange(len(df))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))

ax.bar(x - width, df["more_concerned"], width, label="More concerned than excited", color="tomato")
ax.bar(x,         df["more_excited"],   width, label="More excited than concerned", color="mediumseagreen")
ax.bar(x + width, df["equal_mixed"],    width, label="Equally concerned and excited", color="steelblue")

# Add value labels on each bar
for bars in ax.containers:
    ax.bar_label(bars, fmt="%.0f%%", padding=3, fontsize=8)

# Mark ChatGPT launch
ax.axvline(x=1.5, color="red", linewidth=1, linestyle="--", alpha=0.5)
ax.annotate(
    "ChatGPT launched (Nov 2022)",
    xy=(1.5, 60), xytext=(0.5, 64),
    fontsize=8, color="red",
    arrowprops=dict(arrowstyle="->", color="red")
)

ax.set_title("U.S. Public Sentiment Toward AI in Daily Life, 2021-2024")
ax.set_xlabel("Survey Year")
ax.set_ylabel("% of U.S. Adults")
ax.set_xticks(x)
ax.set_xticklabels(df["year"])
ax.set_ylim(0, 75)
ax.legend()
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig(VISUALS_DIR / "pew_attitudes.png", dpi=150)
print("\nChart saved to visuals/pew_attitudes.png")
plt.show()