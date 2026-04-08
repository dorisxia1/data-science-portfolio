# Dementia Visualization Dashboard

> An interactive Vue.js dashboard for exploring geographic disparities in dementia prevalence and associated risk factors across the United States.

Live Demo: https://dsci-554.github.io/project-vizrd/

---

## Overview

This project visualizes the spatial and contextual dimensions of dementia in the U.S. by integrating multiple datasets into a unified interactive dashboard.

Users can explore relationships between dementia prevalence and:

* demographic patterns
* health risk factors
* environmental conditions
* Medicare coverage

The goal is to help identify regions where dementia burden is unusually high and understand potential contributing factors.

---

## Dashboard Views

* **Risk Hotspots (Mismatch Index)**
* **Demographics**
* **Medicare Coverage**
* **Environmental Risks**
* **Overview**

---

## My Contributions

My primary contributions focused on the **Mismatch Index pipeline and visualization**:

* Built the **Risk Hotspots choropleth map** (`RiskHotspotsView.vue`)
* Developed `dementia_mismatch_index.py` to compute a regression-based mismatch metric
* Modeled expected dementia prevalence using:

  * stroke rate
  * diabetes rate
  * cognitive disability rate
* Designed interaction and visual encoding to highlight geographic disparities

---

## Key Files (My Work)

* `scripts/dementia_mismatch_index.py`
  → Builds linear regression model and computes mismatch index

* `src/views/RiskHotspotsView.vue`
  → Interactive hotspot visualization with choropleth + user interaction

---

## Featured Visualization: Mismatch Index

The **Mismatch Index** measures how dementia prevalence differs from what would be expected based on major health risk factors.

* **Green** → lower than expected
* **Yellow** → near expected
* **Red** → higher than expected

This helps identify counties where dementia burden may reflect hidden risks, care gaps, or underdiagnosis.

---

## Data Sources

* NORC Dementia DataHub
* CDC PLACES
* Environmental datasets
* Medicare data
* Demographic datasets

---

## Technical Stack

* Vue.js
* D3.js
* Bootstrap
* Mapbox GL
* deck.gl
* Python (pandas, scikit-learn)

---

## Repository Structure

```text
dementia-visualization-dashboard/
│
├── public/
│   ├── data/
│   └── scripts/
│       └── dementia_mismatch_index.py   ⭐
│
├── src/
│   ├── assets/
│   ├── components/
│   ├── router/
│   └── views/
│       └── RiskHotspotsView.vue   ⭐
│
├── docs/
│   ├── final_report.pdf
│   ├── presentation.pdf
│   └── wireframe.pdf
│
├── README.md
├── package.json
└── vue.config.js
```

---

## How to Run

```bash
npm install
npm run serve
```

Then open the local development server in your browser.

---

## Notes

* This project was developed as part of a team dashboard; some components reflect shared infrastructure across views
* The portfolio version emphasizes my contributions to the hotspot analysis and modeling pipeline
