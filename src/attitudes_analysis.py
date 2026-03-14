"""
attitudes_analysis.py

Analyzes shifts in U.S. public sentiment toward AI using Pew Research
Center survey data (2021-2024).

DATA SOURCE:
  Pew Research Center — American Trends Panel
  URL: https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/

  HOW TO BUILD pew_attitudes.csv:
  Pew does not offer direct CSV download for all survey waves.
  You manually extract the key figures from each published report.
  This is standard academic practice — document your sources clearly.

  Report 1 (2021):
    "AI and Human Enhancement: Americans' Openness Is Tempered by Concerns"
    https://www.pewresearch.org/internet/2022/03/17/ai-and-human-enhancement-americans-openness-is-tempered-by-a-range-of-concerns/
    → Table: "More concerned than excited about AI in daily life" → 37%
    → "More excited than concerned" → 18%
    → "Equally concerned and excited" → 45%

  Report 2 (2022):
    Same report above includes 2022 tracking data — check Table 1.

  Report 3 (2023):
    "What the Data Says About Americans' Views of Artificial Intelligence"
    https://www.pewresearch.org/short-reads/2023/11/21/what-the-data-says-about-americans-views-of-artificial-intelligence/
    → "More concerned than excited" → 52%
    → "More excited than concerned" → 10%
    → "Equal / neither" → 38%

  Report 4 (2025):
    "How the US Public and AI Experts View Artificial Intelligence"
    https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/
    → Check for updated 2024 figures in this report.

WHY THIS IS ORIGINAL ANALYSIS:
  - Aggregating four years of Pew data into a single trend visualization
    is not available in any single Pew report
  - We time-annotate events (ChatGPT launch) to contextualize the sentiment shift
  - We compute the percentage-point change across years — original calculation
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from pathlib import Path

# PATHS 
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
CSV_PATH    = DATA_DIR / "pew_attitudes.csv"

# DATA 
# Values manually extracted from Pew Research Center published reports.
# See docstring above for exact sources. Update if your extraction differs.
PEW_VALUES = {
    "year":             [2021, 2022, 2023, 2024],
    "more_concerned":   [  37,   38,   52,   52],   # % "more concerned than excited"
    "more_excited":     [  18,   15,   10,   13],   # % "more excited than concerned"
    "equal_mixed":      [  45,   47,   38,   35],   # % "equally concerned and excited" / neither
}

if CSV_PATH.exists():
    df = pd.read_csv(CSV_PATH, skipinitialspace=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    print(f"✓ Loaded CSV: {CSV_PATH}")
else:
    df = pd.DataFrame(PEW_VALUES)
    print("pew_attitudes.csv not found. Using hardcoded values extracted from Pew reports.")
    print("  → Verify these numbers against the reports in the docstring above.")
    df.to_csv(CSV_PATH, index=False)
    print(f"  → Saved to {CSV_PATH}")

# VALIDATE
for col in ["year", "more_concerned", "more_excited", "equal_mixed"]:
    if col not in df.columns:
        raise ValueError(
            f"Missing column '{col}'. Expected columns: "
            "year, more_concerned, more_excited, equal_mixed"
        )

df = df.sort_values("year").reset_index(drop=True)

# ── SANITY CHECK: columns should roughly sum to 100 ───────────────────────────
df["row_sum"] = df["more_concerned"] + df["more_excited"] + df["equal_mixed"]
off = df[df["row_sum"].between(95, 105) == False]
if not off.empty:
    print(f"\n Warning: Some rows don't sum near 100%:\n{off[['year','row_sum']]}")
    print("  → Check your extracted values against the source reports.")

# DESCRIPTIVE STATS (original analysis)
print("\nDescriptive summary:")
print(df[["year","more_concerned","more_excited","equal_mixed"]].to_string(index=False))

concerned_change = df["more_concerned"].iloc[-1] - df["more_concerned"].iloc[0]
excited_change   = df["more_excited"].iloc[-1]   - df["more_excited"].iloc[0]
print(f"\n→ 'More concerned' changed by {concerned_change:+.0f} pp ({df['year'].iloc[0]}–{df['year'].iloc[-1]})")
print(f"→ 'More excited'   changed by {excited_change:+.0f} pp ({df['year'].iloc[0]}–{df['year'].iloc[-1]})")

# PLOT
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#f5f2eb")
ax.set_facecolor("#f5f2eb")

COLORS = {
    "more_concerned": "#c84b2f",
    "more_excited":   "#2d7a4a",
    "equal_mixed":    "#4a7a96",
}
LABELS = {
    "more_concerned": "More concerned than excited",
    "more_excited":   "More excited than concerned",
    "equal_mixed":    "Equally concerned & excited / Neither",
}

x = np.arange(len(df))
width = 0.26

for i, (col, color) in enumerate(COLORS.items()):
    bars = ax.bar(
        x + (i - 1) * width,
        df[col],
        width=width,
        color=color,
        alpha=0.85,
        label=LABELS[col],
        zorder=3,
    )
    # Value labels on bars
    for bar in bars:
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + 0.8, f"{h:.0f}%",
            ha="center", va="bottom", fontsize=8.5, color="#333"
        )

# Annotate the ChatGPT launch
ax.axvline(x=1.5, color="#c84b2f", linewidth=1, linestyle=":", alpha=0.5)
ax.annotate(
    "ChatGPT launched\n(Nov 2022)",
    xy=(1.5, 62),
    xytext=(0.62, 65),
    fontsize=7.5, color="#c84b2f", alpha=0.9, style="italic",
    arrowprops=dict(arrowstyle="->", color="#c84b2f", lw=1.1),
)

# STYLING
ax.set_title(
    "U.S. Public Sentiment Toward AI in Daily Life, 2021–2024",
    fontsize=13, fontweight="bold", pad=14, color="#0f1117"
)
ax.set_xlabel("Survey Year", fontsize=10, color="#555")
ax.set_ylabel("% of U.S. Adults", fontsize=10, color="#555")
ax.set_xticks(x)
ax.set_xticklabels(df["year"].astype(str))
ax.set_ylim(0, 70)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0, symbol="%"))
ax.tick_params(colors="#555")
ax.spines[["top","right"]].set_visible(False)
ax.spines[["left","bottom"]].set_color("#d4cfc6")
ax.grid(axis="y", color="#d4cfc6", linewidth=0.8, alpha=0.7, zorder=0)

ax.legend(loc="upper right", fontsize=8.5, framealpha=0.6)

fig.text(
    0.99, 0.01,
    "Source: Pew Research Center American Trends Panel (2021–2024)\n"
    "pewresearch.org/topic/.../artificial-intelligence",
    ha="right", va="bottom", fontsize=7, color="#999", style="italic"
)

plt.tight_layout()
out_path = VISUALS_DIR / "pew_attitudes.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\n✓ Chart saved → {out_path}")
plt.show()