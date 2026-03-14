"""
summary_analysis.py
-------------------
Comparative dual-axis chart: AI corporate adoption rate vs. global
data center electricity consumption, 2020-2024.

This is the most original chart in the project. No single published
source compares these two datasets on the same chart. The Stanford AI
Index covers adoption, the IEA covers energy. We combine them to ask:
are adoption and environmental cost growing at the same rate?

Required inputs (run other scripts first):
  data/corporate_adoption_clean.csv  - from corporate_adoption.py
  data/iea_energy.csv                - from energy_analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# File paths
BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
VISUALS_DIR = BASE_DIR / "visuals"
VISUALS_DIR.mkdir(exist_ok=True)

# Load adoption data
adopt_path = DATA_DIR / "corporate_adoption_clean.csv"
if not adopt_path.exists():
    raise FileNotFoundError("Run corporate_adoption.py first to generate corporate_adoption_clean.csv")

adopt = pd.read_csv(adopt_path)
print("Loaded corporate_adoption_clean.csv")

# Load energy data (observed only, no projections)
energy_path = DATA_DIR / "iea_energy.csv"
if not energy_path.exists():
    raise FileNotFoundError("Run energy_analysis.py first to generate iea_energy.csv")

energy = pd.read_csv(energy_path)
energy = energy[energy["is_projected"] == False].copy()
print("Loaded iea_energy.csv")

# Merge on shared years
merged = pd.merge(adopt, energy[["year", "total_twh"]], on="year", how="inner")
merged = merged.sort_values("year").reset_index(drop=True)

print("\nMerged dataset:")
print(merged.to_string(index=False))

# Calculate growth rates (original analysis)
merged["adopt_growth"]  = merged["adoption_pct"].pct_change() * 100
merged["energy_growth"] = merged["total_twh"].pct_change() * 100

print("\nYear-over-year growth rates:")
print(merged[["year", "adopt_growth", "energy_growth"]].dropna().to_string(index=False))

avg_adopt  = merged["adopt_growth"].dropna().mean()
avg_energy = merged["energy_growth"].dropna().mean()
print(f"\nAverage annual adoption growth:  {avg_adopt:.1f}%")
print(f"Average annual energy growth:    {avg_energy:.1f}%")
print(f"Energy is growing {avg_energy/avg_adopt:.1f}x faster than adoption")

# Dual-axis plot
fig, ax1 = plt.subplots(figsize=(10, 6))

# Left axis - adoption rate
ax1.plot(merged["year"], merged["adoption_pct"],
         marker="o", linewidth=2, color="steelblue", label="AI adoption rate (%)")
ax1.set_xlabel("Year")
ax1.set_ylabel("% of Organizations Using AI", color="steelblue")
ax1.tick_params(axis="y", labelcolor="steelblue")
ax1.set_ylim(0, 100)

# Right axis - energy consumption
ax2 = ax1.twinx()
ax2.plot(merged["year"], merged["total_twh"],
         marker="s", linewidth=2, linestyle="--", color="tomato", label="Data center energy (TWh)")
ax2.set_ylabel("Data Center Electricity (TWh)", color="tomato")
ax2.tick_params(axis="y", labelcolor="tomato")

# Mark ChatGPT
ax1.axvline(x=2022, color="gray", linewidth=1, linestyle=":", alpha=0.6)
ax1.text(2022.05, 10, "ChatGPT\nlaunched", fontsize=8, color="gray")

# Combined legend
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("AI Adoption Rate vs. Data Center Energy Consumption, 2020-2024")
ax1.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(VISUALS_DIR / "comparative_chart.png", dpi=150)
print("\nChart saved to visuals/comparative_chart.png")
plt.show()