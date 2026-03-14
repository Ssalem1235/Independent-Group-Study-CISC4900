"""
corporate_adoption.py
=====================
Analyzes organizational AI adoption rates over time using McKinsey Global
Survey data as aggregated and published by the Stanford AI Index 2025.

DATA SOURCE:
  Stanford AI Index 2025, Chapter 4: Economy
  Underlying data: McKinsey Global Survey on AI

CSV FORMAT (actual columns from Stanford public data):
  Year, % of respondents, Label
  Label = "AI"    -> general AI adoption (any function)
  Label = "GenAI" -> generative AI adoption specifically

WHY THIS IS ORIGINAL ANALYSIS:
  - We plot the full 2017-2024 trajectory, not just the 2023-2024 jump
  - We overlay GenAI adoption on the same chart for comparison
  - We compute year-over-year growth rates not shown in Stanford charts
  - This dataset is later compared against energy data in summary_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path

# PATH SETUP
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
CSV_PATH    = DATA_DIR / "corporate_adoption.csv"

# LOAD
if CSV_PATH.exists():
    df = pd.read_csv(CSV_PATH, skipinitialspace=True)
    df.columns = df.columns.str.strip()
    print(f"Loaded CSV: {CSV_PATH}")
    print(f"Columns found: {list(df.columns)}")
else:
    raise FileNotFoundError(
        f"Could not find {CSV_PATH}. "
        "Save your Stanford CSV as data/corporate_adoption.csv and re-run."
    )

# CLEAN: strip % sign and convert to float
pct_col = "% of respondents"
df[pct_col] = (
    df[pct_col].astype(str)
    .str.replace("%", "", regex=False)
    .str.strip()
)
df[pct_col] = pd.to_numeric(df[pct_col], errors="coerce")

# SPLIT by Label column
ai_df  = df[df["Label"] == "AI"][["Year", pct_col]].copy()
gen_df = df[df["Label"] == "GenAI"][["Year", pct_col]].copy()

ai_df  = ai_df.rename(columns={"Year": "year", pct_col: "adoption_pct"})
gen_df = gen_df.rename(columns={"Year": "year", pct_col: "gen_ai_pct"})

ai_df  = ai_df.sort_values("year").reset_index(drop=True)
gen_df = gen_df.sort_values("year").reset_index(drop=True)

# DESCRIPTIVE STATS
print("\nOrganizational AI adoption (any function) over time:")
print(ai_df.to_string(index=False))

ai_df["yoy_change"] = ai_df["adoption_pct"].diff()
print("\nYear-over-year change (percentage points):")
print(ai_df[["year","adoption_pct","yoy_change"]].dropna().to_string(index=False))

print("\nGenerative AI adoption:")
print(gen_df.to_string(index=False))

# Save a clean version for summary_analysis.py
ai_df[["year","adoption_pct"]].to_csv(DATA_DIR / "corporate_adoption_clean.csv", index=False)
print(f"\nClean version saved -> data/corporate_adoption_clean.csv")

# PLOT
fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor("#f5f2eb")
ax.set_facecolor("#f5f2eb")

# Main AI adoption line
ax.plot(
    ai_df["year"], ai_df["adoption_pct"],
    color="#2d4a5c", linewidth=2.8, marker="o",
    markersize=7, zorder=5, label="Any AI adoption"
)
ax.fill_between(
    ai_df["year"], ai_df["adoption_pct"],
    alpha=0.08, color="#2d4a5c", zorder=0
)

# Generative AI line
if not gen_df.empty:
    ax.plot(
        gen_df["year"], gen_df["gen_ai_pct"],
        color="#c84b2f", linewidth=2.2, marker="s",
        markersize=7, zorder=5, linestyle="--",
        label="Generative AI specifically"
    )
    for _, row in gen_df.iterrows():
        ax.text(
            row["year"], row["gen_ai_pct"] + 1.5,
            f"{row['gen_ai_pct']:.0f}%",
            ha="center", fontsize=8, color="#c84b2f"
        )

# Annotate 2023->2024 jump
val_2023 = ai_df.loc[ai_df["year"] == 2023, "adoption_pct"].values
val_2024 = ai_df.loc[ai_df["year"] == 2024, "adoption_pct"].values
if len(val_2023) and len(val_2024):
    ax.annotate(
        f"+{val_2024[0] - val_2023[0]:.0f}pp in one year",
        xy=(2024, val_2024[0]),
        xytext=(2022.2, val_2024[0] + 4),
        fontsize=9, color="#0f1117",
        arrowprops=dict(arrowstyle="->", color="#555", lw=1.1),
    )

# ChatGPT launch marker
ax.axvline(x=2022.9, color="#c84b2f", linewidth=0.9, linestyle=":", alpha=0.45)
ax.annotate(
    "ChatGPT\n(Nov 2022)",
    xy=(2022.9, 15),
    xytext=(2021.4, 24),
    fontsize=7.5, color="#c84b2f", alpha=0.8, style="italic",
    arrowprops=dict(arrowstyle="->", color="#c84b2f", lw=1.0),
)

# Value labels on main line
for _, row in ai_df.iterrows():
    ax.text(
        row["year"], row["adoption_pct"] + 1.5,
        f"{row['adoption_pct']:.0f}%",
        ha="center", fontsize=8, color="#333"
    )

# STYLING
ax.set_title(
    "Organizational AI Adoption Rate, 2017-2024",
    fontsize=13, fontweight="bold", pad=14, color="#0f1117"
)
ax.set_xlabel("Year", fontsize=10, color="#555")
ax.set_ylabel("% of Organizations Using AI", fontsize=10, color="#555")
ax.set_xticks(ai_df["year"])
ax.set_ylim(0, 95)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=100, decimals=0, symbol="%"))
ax.tick_params(colors="#555")
ax.spines[["top","right"]].set_visible(False)
ax.spines[["left","bottom"]].set_color("#d4cfc6")
ax.grid(axis="y", color="#d4cfc6", linewidth=0.8, alpha=0.7, zorder=0)
ax.legend(loc="upper left", fontsize=9, framealpha=0.6)

fig.text(
    0.99, 0.01,
    "Source: McKinsey Global Survey on AI, via Stanford AI Index 2025\n"
    "hai.stanford.edu/ai-index/2025-ai-index-report",
    ha="right", va="bottom", fontsize=7, color="#999", style="italic"
)

plt.tight_layout()
out_path = VISUALS_DIR / "corporate_adoption.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\nChart saved -> {out_path}")
plt.show()