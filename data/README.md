# Data Sources — Documentation

This file documents every dataset used in the project: where it came from,
how it was obtained, what it contains, and its known limitations.

This level of documentation addresses a core requirement of rigorous
data analysis: **data provenance**. It answers the question your professor
raised: where does the data come from, and how was it sourced?

---

## ai_data.csv — AI Job Postings by Country

| Field        | Value |
|-------------|-------|
| **Source**  | Stanford AI Index 2025, Chapter 4: Economy |
| **Underlying data** | Lightcast (labor market analytics firm) |
| **URL**     | https://drive.google.com/drive/folders/1AxxxL9-AsaeMdDKtTNHCR1KqEJTsHCod |
| **Report reference** | AI Index 2025 Report, p. 214+ |
| **Coverage** | 2016–2024, multiple countries |
| **Acquisition** | Downloaded from Stanford AI Index public Google Drive (Chapter 4 folder) |
| **License** | CC BY-ND 4.0 (attribution required, no derivatives) |

**What it measures:** The percentage of all job postings in a given country
and year that include AI-related skill requirements, as identified by Lightcast's
natural language processing of job posting text.

**Known limitations:**
- Undercounts roles where AI skills are required but not explicitly named
  in the job title or description (e.g., "data analyst" who uses ML tools)
- Country coverage is uneven: US, UK, India, Canada, Australia, and a
  handful of European countries are most complete
- Methodology may have changed slightly across years — Lightcast periodically
  updates its skill taxonomy

**How we use it:** Tracks AI workforce integration over time; serves as
one axis in the comparative chart (summary_analysis.py)

---

## corporate_adoption.csv — Organizational AI Adoption Rate

| Field        | Value |
|-------------|-------|
| **Source**  | Stanford AI Index 2025, Chapter 4: Economy |
| **Underlying data** | McKinsey Global Survey on AI (annual) |
| **URL**     | https://drive.google.com/drive/folders/1AxxxL9-AsaeMdDKtTNHCR1KqEJTsHCod |
| **Report reference** | AI Index 2025, p. 217 (Figure 4.1.2) |
| **Coverage** | 2017–2024, global (weighted sample) |
| **Acquisition** | Downloaded from Stanford AI Index public Google Drive, OR values extracted from report Figure 4.1.2 |

**What it measures:** The percentage of survey respondents who report that
their organization uses AI in at least one business function.

**Key figures cited directly in report:**
- 2023: 55% of organizations reported AI use
- 2024: 78% of organizations reported AI use (+23pp in one year)
- Generative AI specifically: 33% (2023) → 71% (2024)

**Known limitations:**
- Self-reported — subject to social desirability bias (organizations may
  over-claim AI use)
- Sample composition varies year to year; not a panel study
- "AI use" definition broadened over the survey's history
- Surveys McKinsey clients and network contacts — not a random sample;
  may skew toward larger, more tech-forward organizations

---

## pew_attitudes.csv — U.S. Public Sentiment Toward AI

| Field        | Value |
|-------------|-------|
| **Source**  | Pew Research Center — American Trends Panel |
| **URL (overview)** | https://www.pewresearch.org/topic/internet-technology/emerging-technology/artificial-intelligence/ |
| **Coverage** | 2021–2024, U.S. adults |
| **Acquisition** | **Manually extracted** from four published Pew reports (see below) |
| **License** | Pew data is available for research use with attribution |

**Exact source reports for each year:**

| Year | Report Title | URL | Key Table |
|------|-------------|-----|-----------|
| 2021 | AI and Human Enhancement: Americans' Openness Is Tempered by a Range of Concerns | https://www.pewresearch.org/internet/2022/03/17/ai-and-human-enhancement-americans-openness-is-tempered-by-a-range-of-concerns/ | Figure 1 |
| 2022 | Same report as 2021 | (same URL) | Tracking table |
| 2023 | What the Data Says About Americans' Views of Artificial Intelligence | https://www.pewresearch.org/short-reads/2023/11/21/what-the-data-says-about-americans-views-of-artificial-intelligence/ | Main findings |
| 2024 | How the US Public and AI Experts View Artificial Intelligence | https://www.pewresearch.org/internet/2025/04/03/how-the-us-public-and-ai-experts-view-artificial-intelligence/ | Table 1 |

**Values extracted (verify these against the reports):**

| Year | More concerned (%) | More excited (%) | Equal/mixed (%) |
|------|-------------------|-----------------|-----------------|
| 2021 | 37 | 18 | 45 |
| 2022 | 38 | 15 | 47 |
| 2023 | 52 | 10 | 38 |
| 2024 | 52 | 13 | 35 |

**Note on manual extraction:** Pew Research does not provide direct CSV
downloads for all survey waves. Manually transcribing values from published
figures/tables is a standard and legitimate practice in academic research,
provided you document your sources precisely (as done above). If numbers
in your extracted CSV differ slightly from the above, verify against the
report pages linked here and update accordingly.

**Known limitations:**
- U.S. adults only; not generalizable internationally
- Question wording changed slightly across years — "concerned/excited" framing
  was introduced in 2021 and maintained, but exact phrasing should be verified
- Sample sizes ranged from ~5,000 to ~11,000 adults per wave

---

## iea_energy.csv — Global Data Center Electricity Consumption

| Field        | Value |
|-------------|-------|
| **Source**  | International Energy Agency (IEA) |
| **Report**  | Energy and AI, 2025 |
| **URL**     | https://www.iea.org/reports/energy-and-ai |
| **Coverage** | 2020–2030 (observed: 2020–2024; projected: 2025–2030) |
| **Acquisition** | Option A: Free account at iea.org → Data & Statistics → export CSV. Option B: Reconstructed from published report figures (Base Case scenario) |
| **License** | IEA data: CC BY 4.0 |

**What it measures:** Total electricity consumed by global data centers in
terawatt-hours (TWh), with a breakdown attributing a portion to AI-specific
(accelerated server) workloads.

**Key figures:**
- 2024 (observed): ~415 TWh (~1.5% of global electricity)
- 2030 (IEA Base Case projection): ~945 TWh
- AI-attributed share growing from ~30 TWh (2020) to ~640 TWh (2030, projected)

**⚠ Important — projections are NOT observations:**
All values for 2025 and beyond are IEA Base Case scenario projections.
They carry uncertainty and should be clearly labeled as such in any chart
or written analysis. We follow this requirement in all visualizations.

**Known limitations:**
- AI-attributed electricity is estimated based on workload assumptions,
  not metered separately
- Projections assume continued AI scaling trends; policy changes,
  efficiency improvements, or economic slowdowns could alter outcomes
- "Data center" definition includes hyperscalers, colocation, and enterprise;
  exact scope may differ from other energy studies

---

## How to Reproduce This Dataset Collection

1. **Stanford data:** Go to https://hai.stanford.edu/ai-index/2025-ai-index-report
   → Click "ACCESS THE PUBLIC DATA" → Google Drive opens → Download relevant CSVs
   from Chapter 4 folder → save to `/data/`

2. **Pew data:** Visit each URL above → find the question about being
   "more concerned than excited / more excited than concerned about AI in
   daily life" → record the percentage breakdown by year → create
   `/data/pew_attitudes.csv` with columns: year, more_concerned, more_excited, equal_mixed

3. **IEA data:** Go to https://www.iea.org/reports/energy-and-ai → free account
   required → navigate to data explorer → export "data centre electricity
   consumption by equipment, Base Case" → save as `/data/iea_energy.csv`
   with columns: year, total_twh, ai_twh, is_projected

---

*Last updated: [Add your date when you set up the data]*
*Researchers: Saleh Salem & Saisha Wesley — CISC 4900, Brooklyn College*