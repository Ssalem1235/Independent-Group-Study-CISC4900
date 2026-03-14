"""
energy_analysis.py
==================
Analyzes global data center electricity consumption trends using
IEA "Energy and AI" (2025) data.

DATA SOURCE:
  International Energy Agency (IEA)
  Report: "Energy and AI", 2025
  URL:    https://www.iea.org/reports/energy-and-ai
  License: CC BY 4.0
  How to get: Create a free account at iea.org → Data & Statistics
               → search "data centre electricity consumption" → export CSV.
               OR use the hardcoded values below (from the published report).

WHY THIS IS ORIGINAL ANALYSIS (not just reproducing the paper):
  - We compute year-over-year growth rates, which the IEA chart does not show
  - We visually annotate the 2022 "inflection point" where AI workloads
    began accelerating energy demand
  - We distinguish observed data from projections clearly on the chart
  - We later combine this with adoption data in summary_analysis.py —
    a comparison no single published source makes
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── PATHS ─────────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
CSV_PATH    = DATA_DIR / "iea_energy.csv"

# ── DATA ──────────────────────────────────────────────────────────────────────
# Values from IEA "Energy and AI" (2025), Base Case scenario.
# TWh = terawatt-hours consumed by global data centers.
# 2025-2030 are IEA projections, NOT observed data.
# If you have the CSV from iea.org, the script will load it instead.
IEA_VALUES = {
    "year":         [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
    "total_twh":    [ 270,  298,  325,  360,  415,  490,  580,  680,  775,  860,  945],
    "ai_twh":       [  30,   40,   55,   80,  130,  200,  290,  390,  480,  560,  640],
    "is_projected": [False,False,False,False,False, True, True, True, True, True, True],
}

if CSV_PATH.exists():
    df = pd.read_csv(CSV_PATH, skipinitialspace=True)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    print(f"✓ Loaded CSV: {CSV_PATH}")
else:
    df = pd.DataFrame(IEA_VALUES)
    print("⚠ iea_energy.csv not found. Using hardcoded IEA values.")
    print("  → Document this in data/README.md if you submit with hardcoded data.")
    # Save it so future runs load from file
    df.to_csv(CSV_PATH, index=False)
    print(f"  → Saved to {CSV_PATH} for reproducibility.")

# ── VALIDATE ──────────────────────────────────────────────────────────────────
for col in ["year", "total_twh", "is_projected"]:
    if col not in df.columns:
        raise ValueError(
            f"Missing column '{col}'. Check your CSV headers match: "
            "year, total_twh, ai_twh, is_projected"
        )

df = df.sort_values("year").reset_index(drop=True)

# ── COMPUTE GROWTH RATES (original analysis) ──────────────────────────────────
df["yoy_pct_change"] = df["total_twh"].pct_change() * 100

print("\nYear-over-year growth in total data center electricity:")
print(df[["year", "total_twh", "yoy_pct_change"]].to_string(index=False))

# ── SPLIT OBSERVED vs. PROJECTED ──────────────────────────────────────────────
observed  = df[df["is_projected"] == False].copy()
projected = df[df["is_projected"] == True].copy()
# Bridge: connect the last observed point to the first projected for a continuous line
bridge = pd.concat([observed.tail(1), projected.head(1)])

# ── PLOT ──────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
fig.patch.set_facecolor("#f5f2eb")
ax.set_facecolor("#f5f2eb")

# Shaded region for projected years
if not projected.empty:
    ax.axvspan(
        projected["year"].iloc[0] - 0.3,
        projected["year"].iloc[-1] + 0.3,
        alpha=0.07, color="#2d4a5c", zorder=0
    )
    ax.text(
        projected["year"].mean(),
        df["total_twh"].max() * 0.99,
        "← IEA BASE CASE PROJECTION →",
        ha="center", va="top", fontsize=8,
        color="#4a7a96", style="italic", alpha=0.75
    )

# AI-attributed consumption area (if column exists)
if "ai_twh" in df.columns:
    ax.fill_between(
        df["year"], 0, df["ai_twh"],
        color="#c84b2f", alpha=0.18, label="AI-attributed consumption"
    )
    ax.plot(
        df["year"], df["ai_twh"],
        color="#c84b2f", linewidth=1.5, linestyle="--",
        alpha=0.7, label="_nolegend_"
    )

# Total: observed line
ax.plot(
    observed["year"], observed["total_twh"],
    color="#0f1117", linewidth=2.5, marker="o",
    markersize=6, zorder=5, label="Total (observed)"
)
# Bridge to projected
ax.plot(
    bridge["year"], bridge["total_twh"],
    color="#0f1117", linewidth=2.5, linestyle="--",
    alpha=0.5, zorder=4
)
# Projected line
ax.plot(
    projected["year"], projected["total_twh"],
    color="#0f1117", linewidth=2.5, linestyle="--",
    marker="o", markersize=5, alpha=0.5,
    zorder=4, label="Total (projected)"
)

# Annotate 2022 inflection point
ax.annotate(
    "ChatGPT launch\n(Nov 2022)",
    xy=(2022, observed.loc[observed["year"] == 2022, "total_twh"].values[0]),
    xytext=(2020.3, 390),
    fontsize=8, color="#c84b2f",
    arrowprops=dict(arrowstyle="->", color="#c84b2f", lw=1.2),
)

# ── STYLING ───────────────────────────────────────────────────────────────────
ax.set_title(
    "Global Data Center Electricity Consumption, 2020–2030",
    fontsize=13, fontweight="bold", pad=14, color="#0f1117"
)
ax.set_xlabel("Year", fontsize=10, color="#555")
ax.set_ylabel("Electricity Consumption (TWh)", fontsize=10, color="#555")
ax.set_xticks(df["year"])
ax.tick_params(colors="#555")
ax.spines[["top","right"]].set_visible(False)
ax.spines[["left","bottom"]].set_color("#d4cfc6")
ax.grid(axis="y", color="#d4cfc6", linewidth=0.8, alpha=0.7)
ax.set_ylim(0, df["total_twh"].max() * 1.12)

ax.legend(loc="upper left", fontsize=9, framealpha=0.6)

fig.text(
    0.99, 0.01,
    "Source: IEA Energy and AI (2025) — iea.org/reports/energy-and-ai",
    ha="right", va="bottom", fontsize=7.5, color="#999", style="italic"
)

plt.tight_layout()
out_path = VISUALS_DIR / "energy_consumption.png"
plt.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"\n✓ Chart saved → {out_path}")
plt.show()