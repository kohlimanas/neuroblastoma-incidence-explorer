# Childhood Cancer Incidence Across Age Groups

CMSE 830 midterm project by Manas Kohli.

## Purpose and audience

This app helps students and others interested in childhood cancer
explore reported neuroblastoma and ganglioneuroblastoma incidence.

Main question: How do rates differ across age groups, and how
consistently does the youngest group have the highest rate?

## Data source

International Agency for Research on Cancer.
International Incidence of Childhood Cancer, Volume III.
Table 8.12, printed pages 514–515.

Official website: https://iicc.iarc.fr/

neuroblastoma_clean.csv contains 121 registry entries and 16 columns.
Each entry represents a registry population over a reporting period,
not an individual patient. Rates are age-specific rates per million.

Selected values were checked against the source table.
Full cell-by-cell verification has not been completed.

## Project files

Keep these files together:

- app.py
- neuroblastoma_clean.csv
- neuroblastoma_analysis.ipynb
- requirements.txt
- README.md

## Setup and run on macOS

Development environment: Python 3.14.

Open Terminal in the project folder and run:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

If your Python command is python3, use python3 for the first command.

Open the local URL printed by Streamlit.
Stop the server with Control+C.

To open the analysis notebook:

```bash
python -m pip install jupyterlab
python -m jupyter lab
```

Open neuroblastoma_analysis.ipynb from the project folder.
The CSV must be in the notebook's working directory.

The later notebook setup cells write app files and can launch a server.
They are not required to run the existing app.py.

## App features

- Explore rates for one registry entry.
- Compare up to three registry entries.
- View distributions across 98 complete entries.
- Review missing data, preparation decisions, and limitations.

Unavailable rates are distinguished from reported zeros.

## Main findings

- Ages 0–4 have higher rates than ages 5–9 and 10–14 in all 121 entries.
- Ages 0–4 have the highest rate across all four groups in 95 of
  the 98 complete entries (96.9%).
- The exceptions are Kuwait overall and its two population subgroups.
- Median rates across the same 98 entries are 19.05, 2.95, 0.80,
  and 0.40 per million across successive age groups.

## Limitations

Registry populations can overlap and reporting periods differ.
Entries are not independent countries. Adolescent rates are missing
in 23 entries. Summaries are unweighted, not global incidence estimates.
The analysis does not establish causes, statistical significance,
current rates, or individual risk.

## AI-use disclosure

See the Sources and AI-use disclosure section of the analysis notebook
for the tool/model, purposes, verification, and my contribution.
