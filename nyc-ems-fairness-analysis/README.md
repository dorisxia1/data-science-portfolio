# NYC EMS Fairness Analysis

> A severity-controlled audit of emergency response fairness using real-world NYC EMS data.

This project evaluates whether disparities exist in emergency response times across neighborhoods in New York City using publicly available EMS dispatch data and demographic proxies.

The analysis focuses on **conditional fairness** — comparing response outcomes across demographic groups for incidents of similar medical severity.

---

## Motivation

Emergency response systems increasingly rely on data-driven decision support.
While these systems aim to optimize efficiency, they may unintentionally produce unequal outcomes across communities.

This project asks:

> Do neighborhoods receive comparable emergency response times for similar levels of medical urgency?

---

## Data

* **NYC EMS Incident Dispatch Data (2024 Q1)**
* **American Community Survey (ACS) 2022 (ZIP/ZCTA-level demographics)**

Data source: https://data.cityofnewyork.us/Public-Safety/EMS-Incident-Dispatch-Data/76xm-jjuj/data_preview

Because individual-level demographics are unavailable, demographic characteristics are approximated at the neighborhood (ZIP/ZCTA) level.

---

## Analysis Pipeline

The project is structured as a reproducible pipeline:

1. **Data Ingestion**

   * Collect NYC EMS dispatch data and ACS demographic data

2. **Data Cleaning & Merging**

   * Standardize ZIP codes and merge EMS with demographic data
   * Create key variables such as income quartiles and demographic indicators

3. **Severity Stratification**

   * Group incidents into clinically meaningful tiers (High, Medium, Low)

4. **Fairness Evaluation**

   * Compare response times across demographic groups within severity tiers
   * Perform statistical testing (Welch’s t-test, Mann–Whitney U, ANOVA)

5. **Regression & Robustness**

   * Estimate models controlling for severity, time-of-day, and borough
   * Conduct MAUP sensitivity analysis

6. **Final Outputs**

   * Generate publication-ready tables and figures

---

## Methods

* Severity-stratified analysis (clinical control)
* Welch’s t-test (heteroskedastic data)
* Mann–Whitney U test (distribution robustness)
* One-way ANOVA (income group comparisons)
* False Discovery Rate (FDR) correction
* OLS regression with operational controls (severity, borough, time-of-day)
* MAUP robustness checks

---

## Key Findings

* Response times are **consistently higher in high-Black ZIP codes**, even when controlling for severity
* Disparities increase as clinical urgency decreases
* Lower-income neighborhoods experience **longer delays**, especially for non-critical calls
* Demographic composition remains a **statistically significant predictor** of response time after controlling for operational factors

These results suggest that efficiency-driven systems may still produce **systematic geographic disparities**.

---

## Repository Structure

```id="8v0l1y"
nyc-ems-fairness-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_ingest.ipynb
│   ├── 02_cleaning_and_merging.ipynb
│   ├── 03_severity_grouping.ipynb
│   ├── 04_fairness_evaluation.ipynb
│   ├── 05_regression_and_robustness.ipynb
│   └── 06_generate_final_tables_figures.ipynb
│
├── outputs/
│   ├── figures/
│   └── tables/
│
├── project_proposal.pdf
├── midterm_report.pdf
├── literature_review.pdf
└── requirements.txt
```

---

## How to Run

1. Clone the repository:

```id="xvwvku"
git clone <repo_url>
cd nyc-ems-fairness-analysis
```

2. Create and activate a virtual environment:

```id="y76y59"
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```id="g3xtw1"
pip install -r requirements.txt
```

4. Run notebooks in order:

```id="fsh1xy"
01 → 02 → 03 → 04 → 05 → 06
```

---

## My Contributions

* Designed severity-tier framework for conditional fairness analysis
* Implemented statistical testing pipeline (Welch’s t-test, Mann–Whitney U, ANOVA)
* Built conditional disparity analysis within severity tiers
* Generated key tables and visualizations used in the final report
* Contributed to literature review and project write-up

---

## Paper

Full report: [midterm_report.pdf](midterm_report.pdf)

---

## Notes

* Analysis is conducted at the ZIP/ZCTA level (not individual-level data)
* Results should be interpreted as **area-level associations**
* Underlying EMS decision systems are not observable; analysis uses **outcome-based auditing**

---

## Tech Stack

* Python (pandas, numpy)
* Statistical analysis (scipy, statsmodels)
* Data processing (pyarrow)
* Visualization (matplotlib)
* Jupyter notebooks

---

## Environment Setup Notes

To regenerate ACS data using the Census API:

1. Get an API key: https://api.census.gov/data/key_signup.html
2. Create a `.env` file:

```id="nfw6mp"
CENSUS_API_KEY=your_key_here
```

Ensure `.env` is included in `.gitignore`.

---
