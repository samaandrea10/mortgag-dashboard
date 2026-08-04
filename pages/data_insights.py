from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.session import set_page


# ---------------------------------------------------------
# File path
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "hmda_2023_processed.csv"


# ---------------------------------------------------------
# Data loading and preparation
# ---------------------------------------------------------

@st.cache_data
def load_insights_data() -> pd.DataFrame:
    """
    Load and prepare the processed HMDA dataset for dashboard analysis.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset was not found: {DATA_PATH}"
        )

    data = pd.read_csv(DATA_PATH)

    # Create one consistent binary target column.
    if "approved" in data.columns:
        data["approved"] = pd.to_numeric(
            data["approved"],
            errors="coerce",
        )

    elif "target" in data.columns:
        data["approved"] = pd.to_numeric(
            data["target"],
            errors="coerce",
        )

    elif "action_taken" in data.columns:
        action_taken = pd.to_numeric(
            data["action_taken"],
            errors="coerce",
        )

        data["approved"] = np.where(
            action_taken == 1,
            1,
            np.where(
                action_taken == 3,
                0,
                np.nan,
            ),
        )

    else:
        raise ValueError(
            "The dataset does not contain an approved, target, "
            "or action_taken column."
        )

    data = data.loc[
        data["approved"].isin([0, 1])
    ].copy()

    data["decision"] = data["approved"].map(
        {
            1: "Approved",
            0: "Denied",
        }
    )

    # Convert regular numerical columns.
    numerical_columns = [
        "loan_amount",
        "income",
        "interest_rate",
        "loan_to_value_ratio",
        "property_value",
        "loan_term",
    ]

    for column in numerical_columns:
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce",
            )

    # Convert HMDA DTI categories into representative percentages.
    if "debt_to_income_ratio" in data.columns:
        data["debt_to_income_ratio"] = (
            data["debt_to_income_ratio"]
            .apply(convert_dti_to_numeric)
        )

    # HMDA income is stored in thousands of dollars.
    if "income" in data.columns:
        data["annual_income_dollars"] = (
            data["income"] * 1000
        )

    return data


def convert_dti_to_numeric(value: object) -> float:
    """
    Convert HMDA debt-to-income values into numeric percentages.
    """

    if pd.isna(value):
        return np.nan

    cleaned_value = str(value).strip()

    if cleaned_value.lower() in {
        "",
        "nan",
        "none",
        "exempt",
        "na",
        "n/a",
    }:
        return np.nan

    dti_mapping = {
        "<20%": 15.0,
        "20%-<30%": 25.0,
        "30%-<36%": 33.0,
        "50%-60%": 55.0,
        ">60%": 65.0,
    }

    if cleaned_value in dti_mapping:
        return dti_mapping[cleaned_value]

    cleaned_value = cleaned_value.replace(
        "%",
        "",
    ).strip()

    return pd.to_numeric(
        cleaned_value,
        errors="coerce",
    )


def calculate_approval_rate(
    data: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    """
    Calculate mortgage approval rate by a categorical variable.
    """

    grouped_data = (
        data.dropna(
            subset=[
                group_column,
                "approved",
            ]
        )
        .groupby(
            group_column,
            observed=False,
        )
        .agg(
            Applications=(
                "approved",
                "size",
            ),
            Approval_Rate=(
                "approved",
                "mean",
            ),
        )
        .reset_index()
    )

    grouped_data["Approval Rate (%)"] = (
        grouped_data["Approval_Rate"] * 100
    )

    return grouped_data


def format_currency(value: float) -> str:
    """
    Format a monetary value.
    """

    if pd.isna(value):
        return "N/A"

    return f"${value:,.0f}"


# ---------------------------------------------------------
# Main page
# ---------------------------------------------------------

def show_data_insights() -> None:
    """
    Display interactive insights from the processed HMDA dataset.
    """

    back_column, title_column = st.columns(
        [1, 5],
        vertical_alignment="top",
    )

    with back_column:
        if st.button(
            "← Back",
            key="data_insights_back_button",
            width="stretch",
        ):
            set_page("home")

    with title_column:
        st.markdown(
            (
                "<p class='nova-kicker'>"
                "HMDA EXPLORATORY DATA ANALYSIS"
                "</p>"
            ),
            unsafe_allow_html=True,
        )

        st.title("Data Insights")

        st.write(
            "Explore the financial and demographic patterns contained "
            "in the processed 2023 HMDA mortgage dataset. The charts "
            "describe historical observations and do not represent "
            "causal relationships."
        )

    st.divider()

    try:
        data = load_insights_data()

    except FileNotFoundError:
        st.error(
            "The processed HMDA dataset was not found. Make sure "
            "`hmda_2023_processed.csv` is located in the main "
            "project folder."
        )
        return

    except Exception as error:
        st.error(
            "The Data Insights dashboard could not be loaded. "
            f"Technical details: {error}"
        )
        return

    # -----------------------------------------------------
    # Filters
    # -----------------------------------------------------

    st.subheader("Interactive Filters")

    filter_left, filter_center, filter_right = st.columns(
        3,
        gap="large",
    )

    with filter_left:
        selected_decisions = st.multiselect(
            "Mortgage Decision",
            options=[
                "Approved",
                "Denied",
            ],
            default=[
                "Approved",
                "Denied",
            ],
        )

    with filter_center:
        if "applicant_age" in data.columns:
            age_options = sorted(
                data["applicant_age"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_ages = st.multiselect(
                "Applicant Age",
                options=age_options,
                default=age_options,
            )
        else:
            selected_ages = []

    with filter_right:
        if "derived_sex" in data.columns:
            sex_options = sorted(
                data["derived_sex"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            selected_sexes = st.multiselect(
                "Applicant Sex",
                options=sex_options,
                default=sex_options,
            )
        else:
            selected_sexes = []

    filtered_data = data.copy()

    if selected_decisions:
        filtered_data = filtered_data.loc[
            filtered_data["decision"].isin(
                selected_decisions
            )
        ]

    if (
        "applicant_age" in filtered_data.columns
        and selected_ages
    ):
        filtered_data = filtered_data.loc[
            filtered_data["applicant_age"]
            .astype(str)
            .isin(selected_ages)
        ]

    if (
        "derived_sex" in filtered_data.columns
        and selected_sexes
    ):
        filtered_data = filtered_data.loc[
            filtered_data["derived_sex"]
            .astype(str)
            .isin(selected_sexes)
        ]

    if filtered_data.empty:
        st.warning(
            "No applications match the selected filters."
        )
        return

    st.caption(
        f"Displaying {len(filtered_data):,} of "
        f"{len(data):,} processed mortgage applications."
    )

    st.divider()

    # -----------------------------------------------------
    # Dataset summary
    # -----------------------------------------------------

    st.subheader("Dataset Overview")

    total_applications = len(filtered_data)
    approved_applications = int(
        filtered_data["approved"].sum()
    )
    denied_applications = (
        total_applications - approved_applications
    )
    approval_rate = (
        approved_applications
        / total_applications
    )

    (
        total_column,
        approved_column,
        denied_column,
        rate_column,
    ) = st.columns(
        4,
        gap="small",
    )

    with total_column:
        st.metric(
            label="Applications",
            value=f"{total_applications:,}",
        )

    with approved_column:
        st.metric(
            label="Approved",
            value=f"{approved_applications:,}",
        )

    with denied_column:
        st.metric(
            label="Denied",
            value=f"{denied_applications:,}",
        )

    with rate_column:
        st.metric(
            label="Approval Rate",
            value=f"{approval_rate * 100:.1f}%",
        )

    summary_left, summary_center, summary_right = st.columns(
        3,
        gap="large",
    )

    with summary_left:
        median_income = (
            filtered_data[
                "annual_income_dollars"
            ].median()
            if "annual_income_dollars"
            in filtered_data.columns
            else np.nan
        )

        st.metric(
            label="Median Annual Income",
            value=format_currency(
                median_income
            ),
        )

    with summary_center:
        median_loan = (
            filtered_data[
                "loan_amount"
            ].median()
            if "loan_amount"
            in filtered_data.columns
            else np.nan
        )

        st.metric(
            label="Median Loan Amount",
            value=format_currency(
                median_loan
            ),
        )

    with summary_right:
        median_interest = (
            filtered_data[
                "interest_rate"
            ].median()
            if "interest_rate"
            in filtered_data.columns
            else np.nan
        )

        interest_text = (
            f"{median_interest:.2f}%"
            if not pd.isna(median_interest)
            else "N/A"
        )

        st.metric(
            label="Median Interest Rate",
            value=interest_text,
        )

    st.divider()

    # -----------------------------------------------------
    # Decision distribution
    # -----------------------------------------------------

    st.subheader("Mortgage Decision Distribution")

    decision_counts = (
        filtered_data["decision"]
        .value_counts()
        .rename_axis("Decision")
        .reset_index(name="Applications")
    )

    decision_chart = px.pie(
        decision_counts,
        names="Decision",
        values="Applications",
        hole=0.55,
        title="Approved and Denied Applications",
    )

    decision_chart.update_traces(
        textinfo="label+percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Applications: %{value:,}<br>"
            "Share: %{percent}"
            "<extra></extra>"
        ),
    )

    decision_chart.update_layout(
        height=470,
        margin={
            "l": 30,
            "r": 30,
            "t": 70,
            "b": 30,
        },
    )

    st.plotly_chart(
        decision_chart,
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )

    st.divider()

    # -----------------------------------------------------
    # Approval by applicant age and sex
    # -----------------------------------------------------

    st.subheader("Approval Patterns by Applicant Characteristics")

    age_column, sex_column = st.columns(
        2,
        gap="large",
    )

    with age_column:
        if "applicant_age" in filtered_data.columns:
            approval_by_age = calculate_approval_rate(
                filtered_data,
                "applicant_age",
            )

            age_chart = px.bar(
                approval_by_age,
                x="applicant_age",
                y="Approval Rate (%)",
                text="Approval Rate (%)",
                title="Approval Rate by Applicant Age",
                hover_data={
                    "Applications": ":,",
                    "Approval Rate (%)": ":.1f",
                },
            )

            age_chart.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
            )

            age_chart.update_layout(
                xaxis_title="Applicant Age",
                yaxis_title="Approval Rate (%)",
                yaxis_range=[0, 100],
                height=500,
                showlegend=False,
            )

            st.plotly_chart(
                age_chart,
                width="stretch",
                config={
                    "displayModeBar": False,
                },
            )

    with sex_column:
        if "derived_sex" in filtered_data.columns:
            approval_by_sex = calculate_approval_rate(
                filtered_data,
                "derived_sex",
            )

            sex_chart = px.bar(
                approval_by_sex,
                x="derived_sex",
                y="Approval Rate (%)",
                text="Approval Rate (%)",
                title="Approval Rate by Applicant Sex",
                hover_data={
                    "Applications": ":,",
                    "Approval Rate (%)": ":.1f",
                },
            )

            sex_chart.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
            )

            sex_chart.update_layout(
                xaxis_title="Applicant Sex",
                yaxis_title="Approval Rate (%)",
                yaxis_range=[0, 100],
                height=500,
                showlegend=False,
            )

            st.plotly_chart(
                sex_chart,
                width="stretch",
                config={
                    "displayModeBar": False,
                },
            )

    st.info(
        "These demographic comparisons describe historical approval "
        "patterns in the processed HMDA sample. Differences should "
        "not automatically be interpreted as evidence of causality "
        "or discrimination."
    )

    st.divider()

    # -----------------------------------------------------
    # Approval by race
    # -----------------------------------------------------

    if "derived_race" in filtered_data.columns:
        st.subheader("Approval Rate by Applicant Race")

        approval_by_race = calculate_approval_rate(
            filtered_data,
            "derived_race",
        ).sort_values(
            by="Approval Rate (%)",
            ascending=True,
        )

        race_chart = px.bar(
            approval_by_race,
            x="Approval Rate (%)",
            y="derived_race",
            orientation="h",
            text="Approval Rate (%)",
            title="Historical Approval Rate by Race Category",
            hover_data={
                "Applications": ":,",
                "Approval Rate (%)": ":.1f",
            },
        )

        race_chart.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
        )

        race_chart.update_layout(
            xaxis_title="Approval Rate (%)",
            yaxis_title="Race Category",
            xaxis_range=[0, 100],
            height=590,
            showlegend=False,
            margin={
                "l": 30,
                "r": 50,
                "t": 70,
                "b": 40,
            },
        )

        st.plotly_chart(
            race_chart,
            width="stretch",
            config={
                "displayModeBar": False,
            },
        )

        st.divider()

    # -----------------------------------------------------
    # Financial distributions
    # -----------------------------------------------------

    st.subheader("Financial Variable Distributions")

    distribution_options = {
        "Annual Income": "annual_income_dollars",
        "Loan Amount": "loan_amount",
        "Interest Rate": "interest_rate",
        "Loan-to-Value Ratio": "loan_to_value_ratio",
        "Debt-to-Income Ratio": "debt_to_income_ratio",
        "Property Value": "property_value",
    }

    available_distributions = {
        label: column
        for label, column in distribution_options.items()
        if column in filtered_data.columns
    }

    selected_distribution = st.selectbox(
        "Select a financial variable",
        options=list(
            available_distributions.keys()
        ),
    )

    selected_column = available_distributions[
        selected_distribution
    ]

    distribution_data = filtered_data.dropna(
        subset=[selected_column]
    ).copy()

    # Limit visual impact of extreme outliers.
    if not distribution_data.empty:
        upper_limit = distribution_data[
            selected_column
        ].quantile(0.99)

        distribution_data = distribution_data.loc[
            distribution_data[
                selected_column
            ] <= upper_limit
        ]

    histogram = px.histogram(
        distribution_data,
        x=selected_column,
        color="decision",
        barmode="overlay",
        opacity=0.68,
        nbins=45,
        title=(
            f"{selected_distribution} Distribution "
            "by Mortgage Decision"
        ),
        labels={
            selected_column: selected_distribution,
            "decision": "Decision",
        },
    )

    histogram.update_layout(
        xaxis_title=selected_distribution,
        yaxis_title="Number of Applications",
        height=540,
        legend_title="Mortgage Decision",
    )

    st.plotly_chart(
        histogram,
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )

    st.caption(
        "The chart excludes values above the 99th percentile only "
        "for clearer visualization. The underlying dataset is not "
        "modified."
    )

    st.divider()

    # -----------------------------------------------------
    # LTV and DTI relationships
    # -----------------------------------------------------

    relationship_left, relationship_right = st.columns(
        2,
        gap="large",
    )

    with relationship_left:
        if (
            "loan_to_value_ratio"
            in filtered_data.columns
        ):
            ltv_data = filtered_data.dropna(
                subset=[
                    "loan_to_value_ratio",
                    "decision",
                ]
            ).copy()

            ltv_data = ltv_data.loc[
                ltv_data[
                    "loan_to_value_ratio"
                ].between(0, 150)
            ]

            ltv_box = px.box(
                ltv_data,
                x="decision",
                y="loan_to_value_ratio",
                color="decision",
                points=False,
                title=(
                    "Loan-to-Value Ratio "
                    "by Mortgage Decision"
                ),
                labels={
                    "decision": "Mortgage Decision",
                    "loan_to_value_ratio": "LTV (%)",
                },
            )

            ltv_box.update_layout(
                height=500,
                showlegend=False,
            )

            st.plotly_chart(
                ltv_box,
                width="stretch",
                config={
                    "displayModeBar": False,
                },
            )

    with relationship_right:
        if (
            "debt_to_income_ratio"
            in filtered_data.columns
        ):
            dti_data = filtered_data.dropna(
                subset=[
                    "debt_to_income_ratio",
                    "decision",
                ]
            ).copy()

            dti_box = px.box(
                dti_data,
                x="decision",
                y="debt_to_income_ratio",
                color="decision",
                points=False,
                title=(
                    "Debt-to-Income Ratio "
                    "by Mortgage Decision"
                ),
                labels={
                    "decision": "Mortgage Decision",
                    "debt_to_income_ratio": "DTI (%)",
                },
            )

            dti_box.update_layout(
                height=500,
                showlegend=False,
            )

            st.plotly_chart(
                dti_box,
                width="stretch",
                config={
                    "displayModeBar": False,
                },
            )

    st.divider()

    # -----------------------------------------------------
    # Aggregated table
    # -----------------------------------------------------

    st.subheader("Aggregated Approval Summary")

    group_variable_options = {
        "Applicant Age": "applicant_age",
        "Applicant Sex": "derived_sex",
        "Applicant Race": "derived_race",
        "Applicant Ethnicity": "derived_ethnicity",
    }

    available_groups = {
        label: column
        for label, column in group_variable_options.items()
        if column in filtered_data.columns
    }

    selected_group_label = st.selectbox(
        "Group the dataset by",
        options=list(
            available_groups.keys()
        ),
        key="data_insights_group_selector",
    )

    selected_group_column = available_groups[
        selected_group_label
    ]

    aggregated_summary = calculate_approval_rate(
        filtered_data,
        selected_group_column,
    )

    aggregated_summary = aggregated_summary.rename(
        columns={
            selected_group_column: selected_group_label,
        }
    )

    aggregated_summary = aggregated_summary[
        [
            selected_group_label,
            "Applications",
            "Approval Rate (%)",
        ]
    ].sort_values(
        by="Applications",
        ascending=False,
    )

    st.dataframe(
        aggregated_summary.style.format(
            {
                "Applications": "{:,.0f}",
                "Approval Rate (%)": "{:.1f}%",
            }
        ),
        width="stretch",
        hide_index=True,
    )

    st.divider()

    # -----------------------------------------------------
    # Academic interpretation
    # -----------------------------------------------------

    st.subheader("Interpretation and Responsible Use")

    st.markdown(
        """
        The Data Insights dashboard provides descriptive evidence
        about the historical HMDA sample used in this project.

        The displayed patterns support exploratory analysis and help
        identify variables associated with mortgage approval outcomes.
        However, observed differences do not establish causality.

        Financial variables such as income, interest rate, loan
        amount, debt-to-income ratio and loan-to-value ratio should be
        interpreted together rather than in isolation. Demographic
        comparisons require additional fairness analysis and careful
        consideration of sample composition.
        """
    )

    st.caption(
        "Charts are based on the processed 2023 HMDA dataset and are "
        "intended for academic and analytical use."
    )