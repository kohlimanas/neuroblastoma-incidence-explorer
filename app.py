from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Childhood Cancer Incidence",
    layout="wide"
)

st.title("Childhood Cancer Incidence Across Age Groups")
st.subheader("Neuroblastoma and ganglioneuroblastoma")

st.write(
    "Explore how reported incidence rates differ across age groups "
    "and registry populations. This app is intended for students "
    "and others interested in understanding childhood cancer data."
)

data_path = Path(__file__).resolve().parent / "neuroblastoma_clean.csv"
df = pd.read_csv(data_path)

st.caption(
    "Source: IARC, International Incidence of Childhood Cancer, "
    "Volume III, Table 8.12. Age-specific rates are per million."
)

st.info(
    "These are historical registry data. Reporting periods differ, "
    "some populations overlap, and unavailable rates are not zeros."
)

st.subheader("Explore a registry entry")

selected_entry = st.selectbox(
    "Choose a registry population and reporting period",
    options=df["registry_period"].tolist(),
    index=df["registry_period"].tolist().index("USA (1998-2012)")
)

selected_row = df.loc[df["registry_period"] == selected_entry]
# READABLE_REGISTRY_TABLE
registry_table = pd.DataFrame({
    "Age group (years)": ["0–4", "5–9", "10–14", "15–19"],
    "Incidence rate per million": selected_row[
        ["rate_0_4", "rate_5_9", "rate_10_14", "rate_15_19"]
    ].iloc[0].to_numpy(dtype=float)
})

st.dataframe(
    registry_table.style.format(
        {"Incidence rate per million": "{:.1f}"},
        na_rep="Unavailable"
    ),
    hide_index=True
)


# AGE_GROUP_CHART
import matplotlib.pyplot as plt

age_columns = ["rate_0_4", "rate_5_9", "rate_10_14", "rate_15_19"]
age_labels = ["0–4", "5–9", "10–14", "15–19"]

rates = selected_row[age_columns].iloc[0].to_numpy(dtype=float)

st.subheader("How does incidence differ across age groups?")
st.write(selected_entry)

fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(age_labels, rates, color="#3274A1")

ax.set_xlabel("Age group (years)")
ax.set_ylabel("Age-specific incidence rate per million")
ax.set_ylim(0, max(rates[~pd.isna(rates)]) * 1.2)

for bar, rate in zip(bars, rates):
    if pd.notna(rate):
        ax.annotate(
            f"{rate:.1f}",
            (bar.get_x() + bar.get_width() / 2, rate),
            ha="center", va="bottom",
            xytext=(0, 4), textcoords="offset points"
        )
    else:
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            0.03,
            "Unavailable",
            transform=ax.get_xaxis_transform(),
            ha="center", fontsize=9
        )

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    "Compare the bar heights within this registry entry. "
    "Unavailable rates are left blank and labelled; they are not zeros. "
    "This chart compares age groups, not changes over time."
)


# REGISTRY_COMPARISON
st.subheader("Compare registry age patterns")

comparison_entries = st.multiselect(
    "Choose up to three registry entries",
    options=df["registry_period"].tolist(),
    default=["USA (1998-2012)", "KUWAIT (1994-2012)"],
    max_selections=3
)

if comparison_entries:
    comparison_data = (
        df.set_index("registry_period")
        .loc[comparison_entries, age_columns]
        .T
    )
    comparison_data.index = age_labels

    fig, ax = plt.subplots(figsize=(10, 5))

    comparison_data.plot.bar(
        ax=ax,
        rot=0,
        color=["#3274A1", "#D87928", "#3A8067"]
    )

    for container, entry in zip(ax.containers, comparison_entries):
        entry_rates = comparison_data[entry].to_numpy(dtype=float)

        labels = [
            f"{rate:.1f}" if pd.notna(rate) else "N/A"
            for rate in entry_rates
        ]
        ax.bar_label(container, labels=labels, padding=3, fontsize=9)

    maximum = comparison_data.max().max()
    ax.set_ylim(0, maximum * 1.2)
    ax.set_xlabel("Age group (years)")
    ax.set_ylabel("Age-specific incidence rate per million")
    ax.legend(title="Registry and reporting period", fontsize=8)

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.dataframe(comparison_data.style.format("{:.1f}", na_rep="Unavailable"))

    st.caption(
        "N/A indicates an unavailable rate. Reporting periods and "
        "population coverage differ, and selected entries may overlap. "
        "Differences do not establish their causes."
    )
else:
    st.info("Select at least one registry entry to show the comparison.")


# OVERALL_DISTRIBUTION
import numpy as np

st.subheader("Is the youngest-group pattern consistent?")

complete_rates = df.dropna(subset=age_columns)[age_columns]

youngest_highest = (
    complete_rates["rate_0_4"]
    > complete_rates[age_columns[1:]].max(axis=1)
)

st.write(
    f"Ages 0–4 have the highest reported rate in "
    f"{int(youngest_highest.sum())} of {len(complete_rates)} "
    f"complete registry entries "
    f"({youngest_highest.mean() * 100:.1f}%)."
)

fig, ax = plt.subplots(figsize=(9, 5))

ax.boxplot(
    [complete_rates[column].to_numpy() for column in age_columns],
    tick_labels=age_labels,
    showfliers=False
)

rng = np.random.default_rng(42)

for position, column in enumerate(age_columns, start=1):
    values = complete_rates[column].to_numpy()
    offsets = rng.uniform(-0.12, 0.12, len(values))

    ax.scatter(
        position + offsets,
        values,
        alpha=0.45,
        s=20,
        color="#3274A1"
    )

ax.set_xlabel("Age group (years)")
ax.set_ylabel("Age-specific incidence rate per million")
ax.set_ylim(bottom=0)

fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

st.caption(
    "Each point represents one registry entry. Boxes show the middle "
    "50% of values; the line inside each box marks the median. "
    "Horizontal offsets separate points and have no analytical meaning. "
    "All observations are shown, including those beyond the whiskers."
)

median_table = pd.DataFrame({
    "Age group": age_labels,
    "Median rate per million": complete_rates.median().to_numpy()
})

st.dataframe(
    median_table.style.format({"Median rate per million": "{:.2f}"}),
    hide_index=True
)

st.write(
    "The youngest age group has the highest median and the widest "
    "spread in absolute rates. The three exceptions to its having "
    "the highest rate are Kuwait overall and its two population "
    "subgroups, where ages 15–19 have the highest reported rate."
)

st.caption(
    "These are unweighted summaries of overlapping registry entries "
    "with different reporting periods, not worldwide incidence estimates. "
    "The 23 entries without adolescent rates are excluded here."
)


# MISSING_DATA_CHECK
st.subheader("What about entries without adolescent rates?")

younger_columns = ["rate_0_4", "rate_5_9", "rate_10_14"]
younger_complete = df.dropna(subset=younger_columns)

highest_under_15 = (
    younger_complete["rate_0_4"]
    > younger_complete[younger_columns[1:]].max(axis=1)
)

missing_adolescent = younger_complete["rate_15_19"].isna()

st.write(
    f"Ages 0–4 have higher reported rates than both ages 5–9 "
    f"and 10–14 in {int(highest_under_15.sum())} of "
    f"{len(younger_complete)} entries. This includes all "
    f"{int(missing_adolescent.sum())} entries without adolescent rates."
)

st.caption(
    "This supports the pattern among children under 15. "
    "It cannot establish which of all four age groups has the "
    "highest rate where adolescent data are unavailable."
)


# DATA_QUALITY_PANEL
with st.expander("Data quality and preparation"):
    st.write(
        "Each row represents a registry population over a reporting "
        "period, not an individual patient. The dataset combines "
        "neuroblastoma and ganglioneuroblastoma into category IVa."
    )

    quality_table = pd.DataFrame({
        "Age group": age_labels,
        "Available rates": df[age_columns].notna().sum().to_numpy(),
        "Unavailable rates": df[age_columns].isna().sum().to_numpy()
    })

    st.dataframe(quality_table, hide_index=True)

    st.write(
        f"Exact duplicate rows: {int(df.duplicated().sum())}. "
        f"Repeated registry-period labels: "
        f"{int(df['registry_period'].duplicated().sum())}."
    )

    st.markdown(
        """
- Missing rates remain unavailable; they are not replaced or imputed.
- Reported zeros are retained.
- Unusual values are not removed simply because they are high.
- Rates already share the same units, so scaling is unnecessary.
- Overlapping populations remain labelled and are not pooled.
- Selected values were checked against the published table;
  a full cell-by-cell verification has not been completed.
        """
    )


# LIMITATIONS_AND_SOURCE
st.subheader("Limitations")

st.markdown(
    """
- **Overlapping populations:** Entries can include overall populations
  and their subgroups. They are not independent countries.
- **Different coverage and periods:** Geographic coverage and reporting
  periods vary. These data do not establish current rates or time trends.
- **Missing adolescent rates:** Four-group comparisons exclude entries
  without rates for ages 15–19.
- **Unweighted summaries:** Registry entries contribute equally to the
  medians. These are not population-weighted global estimates.
- **Descriptive findings:** The analysis does not explain causes,
  estimate individual risk, or establish statistical significance.
    """
)

st.subheader("Data source")

st.markdown(
    """
International Agency for Research on Cancer,
*International Incidence of Childhood Cancer, Volume III*,
Table 8.12: Neuroblastoma and ganglioneuroblastoma (IVa),
printed pages 514–515.

[Visit the official IICC website](https://iicc.iarc.fr/)
    """
)

st.caption(
    "The app uses a cleaned transcription of the published table. "
    "Selected values were checked against the source; full "
    "cell-by-cell verification has not been completed."
)
