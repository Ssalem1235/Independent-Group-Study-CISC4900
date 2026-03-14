"""
energy_analysis.py
------------------
Analyzes global data center electricity consumption trends.

Data Source:
  International Energy Agency (IEA) - Energy and AI Report (2025)
  URL: https://www.iea.org/reports/energy-and-ai
  Note: Values for 2025-2030 are IEA projections, not observed data.
        This is clearly labeled in the chart.
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)
CSV_PATH    = DATA_DIR / "iea_energy.csv"

# Load data - if no CSV exists, use values from IEA report directly
if CSV_PATH.exists():
    df = pd.read_csv(CSV_PATH)
    print("Loaded iea_energy.csv")
else:
    # Values taken directly from IEA Energy and AI (2025), Base Case scenario
    # ai_twh = portion of total attributed specifically to AI workloads
    df = pd.DataFrame({
        "year":         [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030],
        "total_twh":    [ 270,  298,  325,  360,  415,  490,  580,  680,  775,  860,  945],
        "ai_twh":       [  30,   40,   55,   80,  130,  200,  290,  390,  480,  560,  640],
        "is_projected": [False,False,False,False,False,True,True,True,True,True,True],
    })
    df.to_csv(CSV_PATH, index=False)
    print("No CSV found - using IEA report values. Saved to iea_energy.csv")

# Sort by year
df = df.sort_values("year").reset_index(drop=True)

# Compute year-over-year growth rate (our own calculation, not in the IEA report)
df["yoy_growth_pct"] = df["total_twh"].pct_change() * 100

# Print descriptive stats
print("\nData Center Electricity Consumption (TWh):")
print(df[["year", "total_twh", "yoy_growth_pct"]].to_string(index=False))
print(f"\nTotal growth 2020-2024: {df.loc[df['year']==2024,'total_twh'].values[0] - df.loc[df['year']==2020,'total_twh'].values[0]} TWh")

# Split observed vs projected for the chart
observed  = df[df["is_projected"] == False]
projected = df[df["is_projected"] == True]

# Plot
plt.figure(figsize=(10, 6))

# Total consumption - solid line for observed, dashed for projected
plt.plot(observed["year"], observed["total_twh"],
         marker="o", linewidth=2, label="Total (observed)", color="steelblue")
plt.plot(projected["year"], projected["total_twh"],
         marker="o", linewidth=2, linestyle="--", label="Total (projected)", color="steelblue")

# AI-attributed consumption - separate line showing AI's specific share
if "ai_twh" in df.columns:
    plt.plot(observed["year"], observed["ai_twh"],
             marker="s", linewidth=2, label="AI-attributed (observed)", color="tomato")
    plt.plot(projected["year"], projected["ai_twh"],
             marker="s", linewidth=2, linestyle="--", label="AI-attributed (projected)", color="tomato")

# Shade the projected region so it is clear
plt.axvspan(2024.5, 2030.5, alpha=0.1, color="gray", label="Projection range")

# Note the AI acceleration point
plt.axvline(x=2022, color="gray", linewidth=1, linestyle=":", alpha=0.6)
plt.text(2022.1, 430, "ChatGPT\nlaunched", fontsize=8, color="gray")

plt.title("Global Data Center Electricity Consumption, 2020-2030")
plt.xlabel("Year")
plt.ylabel("Electricity Consumption (TWh)")
plt.xticks(df["year"], rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(VISUALS_DIR / "energy_consumption.png", dpi=150)
print("\nChart saved to visuals/energy_consumption.png")
plt.show()