from __future__ import annotations

from typing import Any

import streamlit as st

from utils.financial_health import (
    calculate_financial_health_score,
)
from utils.prediction import (
    run_mortgage_analysis,
)
from utils.session import (
    get_analysis_result,
    set_page,
)


def format_currency(value: float) -> str:
    """
    Format a numeric value as US currency.
    """
    return f"${value:,.0f}"


def format_percentage(value: float) -> str:
    """
    Convert a decimal probability into a percentage.
    """
    return f"{value * 100:.1f}%"


def calculate_percentage_change(
    current_value: float,
    simulated_value: float,
) -> float:
    """
    Calculate the percentage change between two values.
    """
    if current_value == 0:
        return 0.0

    return (
        (simulated_value - current_value)
        / abs(current_value)
        * 100
    )


def calculate_difference(
    current_value: float,
    simulated_value: float,
) -> float:
    """
    Calculate the absolute difference between two values.
    """
    return simulated_value - current_value


def format_probability_delta(
    current_value: float,
    simulated_value: float,
) -> str:
    """
    Format probability difference as percentage points.
    """
    delta = (
        simulated_value - current_value
    ) * 100

    return f"{delta:+.1f} percentage points"


def format_score_delta(
    current_value: float,
    simulated_value: float,
) -> str:
    """
    Format financial health score difference.
    """
    delta = simulated_value - current_value

    return f"{delta:+.0f} points"


def format_currency_delta(
    current_value: float,
    simulated_value: float,
) -> str:
    """
    Format a currency difference.
    """
    delta = simulated_value - current_value

    return f"{delta:+,.0f}"


def format_ratio_delta(
    current_value: float,
    simulated_value: float,
) -> str:
    """
    Format ratio difference in percentage points.
    """
    delta = simulated_value - current_value

    return f"{delta:+.1f} percentage points"


def get_delta_type(
    current_value: float,
    simulated_value: float,
    higher_is_better: bool,
) -> str:
    """
    Return the Streamlit metric delta color direction.
    """
    if simulated_value == current_value:
        return "off"

    if higher_is_better:
        return "normal"

    return "inverse"


def get_numeric_value(
    result: dict[str, Any],
    key: str,
    default: float,
) -> float:
    """
    Read a numeric result value safely.
    """
    try:
        return float(
            result.get(
                key,
                default,
            )
        )
    except (
        TypeError,
        ValueError,
    ):
        return float(default)


def build_scenario_recommendations(
    current_result: dict[str, Any],
    simulated_result: dict[str, Any],
    current_health: dict[str, Any],
    simulated_health: dict[str, Any],
) -> list[str]:
    """
    Generate recommendations based on the simulated changes.
    """
    recommendations: list[str] = []

    current_approval = float(
        current_result["approval_probability"]
    )
    simulated_approval = float(
        simulated_result["approval_probability"]
    )

    current_payment_ratio = float(
        current_result["payment_to_income_ratio"]
    )
    simulated_payment_ratio = float(
        simulated_result["payment_to_income_ratio"]
    )

    current_ltv = float(
        current_result["loan_to_value_ratio"]
    )
    simulated_ltv = float(
        simulated_result["loan_to_value_ratio"]
    )

    current_dti = float(
        current_result["debt_to_income_ratio"]
    )
    simulated_dti = float(
        simulated_result["debt_to_income_ratio"]
    )

    current_score = float(
        current_health["score"]
    )
    simulated_score = float(
        simulated_health["score"]
    )

    if simulated_approval > current_approval:
        approval_gain = (
            simulated_approval - current_approval
        ) * 100

        recommendations.append(
            "The simulated profile improves approval probability "
            f"by approximately {approval_gain:.1f} percentage points."
        )
    elif simulated_approval < current_approval:
        approval_loss = (
            current_approval - simulated_approval
        ) * 100

        recommendations.append(
            "The simulated profile reduces approval probability "
            f"by approximately {approval_loss:.1f} percentage points."
        )
    else:
        recommendations.append(
            "The selected changes do not materially alter the "
            "model's approval probability."
        )

    if simulated_score > current_score:
        recommendations.append(
            "The Financial Health Score improves under this scenario, "
            "indicating a stronger overall borrower profile."
        )
    elif simulated_score < current_score:
        recommendations.append(
            "The Financial Health Score declines under this scenario, "
            "indicating increased financial pressure or lending risk."
        )

    if simulated_payment_ratio < current_payment_ratio:
        recommendations.append(
            "Mortgage affordability improves because the estimated "
            "payment represents a smaller share of monthly income."
        )
    elif simulated_payment_ratio > current_payment_ratio:
        recommendations.append(
            "Mortgage affordability weakens because the estimated "
            "payment consumes a larger share of monthly income."
        )

    if simulated_ltv < current_ltv:
        recommendations.append(
            "The lower loan-to-value ratio strengthens borrower equity "
            "and may reduce lender exposure."
        )
    elif simulated_ltv > current_ltv:
        recommendations.append(
            "The higher loan-to-value ratio reduces borrower equity "
            "and may increase lending risk."
        )

    if simulated_dti < current_dti:
        recommendations.append(
            "The reduced debt-to-income ratio creates a more manageable "
            "overall debt profile."
        )
    elif simulated_dti > current_dti:
        recommendations.append(
            "The increased debt-to-income ratio may require additional "
            "review during underwriting."
        )

    if simulated_payment_ratio > 36:
        recommendations.append(
            "The simulated mortgage payment exceeds a moderate "
            "affordability range and may place pressure on cash flow."
        )

    if simulated_ltv > 90:
        recommendations.append(
            "The simulated loan-to-value ratio is above 90%, indicating "
            "limited borrower equity."
        )

    if simulated_dti > 43:
        recommendations.append(
            "The simulated debt-to-income ratio is above 43%, which may "
            "represent a significant affordability concern."
        )

    return recommendations


def show_decision_comparison(
    current_result: dict[str, Any],
    simulated_result: dict[str, Any],
) -> None:
    """
    Display current and simulated decisions side by side.
    """
    st.subheader("Decision Comparison")

    current_column, simulated_column = st.columns(
        2,
        gap="large",
    )

    with current_column:
        st.markdown("#### Current Application")

        if int(current_result["prediction"]) == 1:
            st.success(
                f"### ✓ {current_result['predicted_decision']}"
            )
        else:
            st.error(
                f"### ⚠ {current_result['predicted_decision']}"
            )

        st.metric(
            label="Approval Probability",
            value=format_percentage(
                float(
                    current_result[
                        "approval_probability"
                    ]
                )
            ),
        )

        st.metric(
            label="Risk Level",
            value=str(
                current_result["risk_level"]
            ),
        )

    with simulated_column:
        st.markdown("#### Simulated Scenario")

        if int(simulated_result["prediction"]) == 1:
            st.success(
                f"### ✓ {simulated_result['predicted_decision']}"
            )
        else:
            st.error(
                f"### ⚠ {simulated_result['predicted_decision']}"
            )

        st.metric(
            label="Approval Probability",
            value=format_percentage(
                float(
                    simulated_result[
                        "approval_probability"
                    ]
                )
            ),
            delta=format_probability_delta(
                float(
                    current_result[
                        "approval_probability"
                    ]
                ),
                float(
                    simulated_result[
                        "approval_probability"
                    ]
                ),
            ),
            delta_color="normal",
        )

        st.metric(
            label="Risk Level",
            value=str(
                simulated_result["risk_level"]
            ),
        )


def show_financial_comparison(
    current_result: dict[str, Any],
    simulated_result: dict[str, Any],
    current_health: dict[str, Any],
    simulated_health: dict[str, Any],
) -> None:
    """
    Display financial comparison metrics.
    """
    st.subheader("Financial Impact")

    first_row = st.columns(
        4,
        gap="medium",
    )

    with first_row[0]:
        st.metric(
            label="Financial Health Score",
            value=f"{simulated_health['score']}/100",
            delta=format_score_delta(
                float(current_health["score"]),
                float(simulated_health["score"]),
            ),
            delta_color="normal",
        )

    with first_row[1]:
        st.metric(
            label="Monthly Payment",
            value=format_currency(
                float(
                    simulated_result[
                        "monthly_payment"
                    ]
                )
            ),
            delta=format_currency_delta(
                float(
                    current_result[
                        "monthly_payment"
                    ]
                ),
                float(
                    simulated_result[
                        "monthly_payment"
                    ]
                ),
            ),
            delta_color="inverse",
        )

    with first_row[2]:
        st.metric(
            label="Total Interest",
            value=format_currency(
                float(
                    simulated_result[
                        "total_interest"
                    ]
                )
            ),
            delta=format_currency_delta(
                float(
                    current_result[
                        "total_interest"
                    ]
                ),
                float(
                    simulated_result[
                        "total_interest"
                    ]
                ),
            ),
            delta_color="inverse",
        )

    with first_row[3]:
        st.metric(
            label="Total Repayment",
            value=format_currency(
                float(
                    simulated_result[
                        "total_payment"
                    ]
                )
            ),
            delta=format_currency_delta(
                float(
                    current_result[
                        "total_payment"
                    ]
                ),
                float(
                    simulated_result[
                        "total_payment"
                    ]
                ),
            ),
            delta_color="inverse",
        )

    second_row = st.columns(
        3,
        gap="medium",
    )

    with second_row[0]:
        st.metric(
            label="Payment-to-Income",
            value=(
                f"{float(simulated_result['payment_to_income_ratio']):.1f}%"
            ),
            delta=format_ratio_delta(
                float(
                    current_result[
                        "payment_to_income_ratio"
                    ]
                ),
                float(
                    simulated_result[
                        "payment_to_income_ratio"
                    ]
                ),
            ),
            delta_color="inverse",
        )

    with second_row[1]:
        st.metric(
            label="Loan-to-Value",
            value=(
                f"{float(simulated_result['loan_to_value_ratio']):.1f}%"
            ),
            delta=format_ratio_delta(
                float(
                    current_result[
                        "loan_to_value_ratio"
                    ]
                ),
                float(
                    simulated_result[
                        "loan_to_value_ratio"
                    ]
                ),
            ),
            delta_color="inverse",
        )

    with second_row[2]:
        st.metric(
            label="Debt-to-Income",
            value=(
                f"{float(simulated_result['debt_to_income_ratio']):.1f}%"
            ),
            delta=format_ratio_delta(
                float(
                    current_result[
                        "debt_to_income_ratio"
                    ]
                ),
                float(
                    simulated_result[
                        "debt_to_income_ratio"
                    ]
                ),
            ),
            delta_color="inverse",
        )


def show_component_comparison(
    current_health: dict[str, Any],
    simulated_health: dict[str, Any],
) -> None:
    """
    Compare Financial Health Score components.
    """
    st.subheader("Financial Health Components")

    current_components = current_health[
        "component_scores"
    ]
    simulated_components = simulated_health[
        "component_scores"
    ]

    component_names = [
        "Approval Strength",
        "Debt Management",
        "Equity Position",
        "Mortgage Affordability",
        "Income Capacity",
    ]

    component_columns = st.columns(
        5,
        gap="small",
    )

    for column, component_name in zip(
        component_columns,
        component_names,
    ):
        current_value = float(
            current_components[component_name]
        )
        simulated_value = float(
            simulated_components[component_name]
        )

        with column:
            st.metric(
                label=component_name,
                value=f"{simulated_value:.0f}/100",
                delta=(
                    f"{simulated_value - current_value:+.0f}"
                ),
                delta_color="normal",
            )

            progress_value = max(
                0.0,
                min(
                    1.0,
                    simulated_value / 100,
                ),
            )

            st.progress(
                progress_value
            )


def show_recommendations(
    current_result: dict[str, Any],
    simulated_result: dict[str, Any],
    current_health: dict[str, Any],
    simulated_health: dict[str, Any],
) -> None:
    """
    Display scenario interpretation and recommendations.
    """
    st.subheader("NOVA Scenario Insights")

    recommendations = build_scenario_recommendations(
        current_result=current_result,
        simulated_result=simulated_result,
        current_health=current_health,
        simulated_health=simulated_health,
    )

    current_score = float(
        current_health["score"]
    )
    simulated_score = float(
        simulated_health["score"]
    )

    current_probability = float(
        current_result["approval_probability"]
    )
    simulated_probability = float(
        simulated_result["approval_probability"]
    )

    improved_score = (
        simulated_score > current_score
    )
    improved_probability = (
        simulated_probability > current_probability
    )

    if improved_score and improved_probability:
        st.success(
            "This scenario improves both the model-estimated approval "
            "probability and the NOVA Financial Health Score."
        )
    elif (
        simulated_score < current_score
        and simulated_probability < current_probability
    ):
        st.error(
            "This scenario weakens both the approval outlook and the "
            "overall Financial Health Score."
        )
    else:
        st.info(
            "This scenario creates a mixed financial effect. Review the "
            "individual indicators before making a decision."
        )

    for recommendation in recommendations:
        st.write(
            f"• {recommendation}"
        )

    st.caption(
        "Scenario results are analytical estimates. They do not represent "
        "a guaranteed lender decision or financial advice."
    )


def show_simulator() -> None:
    """
    Display the NOVA Mortgage Scenario Simulator.
    """
    current_result = get_analysis_result()

    if current_result is None:
        st.warning(
            "No mortgage analysis is currently available. "
            "Please complete an application before opening the simulator."
        )

        if st.button(
            "Start Mortgage Analysis",
            key="simulator_start_analysis",
            type="primary",
            width="stretch",
        ):
            set_page(
                "approval"
            )

        return

    title_column, results_button, home_button = st.columns(
        [5, 1.2, 1],
        vertical_alignment="center",
    )

    with title_column:
        st.markdown(
            "<p class='nova-kicker'>NOVA DECISION LAB</p>",
            unsafe_allow_html=True,
        )
        st.title("Mortgage Scenario Simulator")

    with results_button:
        if st.button(
            "← Results",
            key="simulator_back_results",
            type="primary",
            width="stretch",
        ):
            set_page(
                "results"
            )

    with home_button:
        if st.button(
            "🏠 Home",
            key="simulator_home",
            type="primary",
            width="stretch",
        ):
            set_page(
                "home"
            )

    st.caption(
        "Adjust the applicant and loan assumptions to explore how the "
        "mortgage outlook may change."
    )

    st.divider()

    current_loan_amount = get_numeric_value(
        current_result,
        "loan_amount",
        250000,
    )

    current_income = get_numeric_value(
        current_result,
        "annual_income",
        80000,
    )

    current_property_value = get_numeric_value(
        current_result,
        "property_value",
        350000,
    )

    current_interest_rate = get_numeric_value(
        current_result,
        "interest_rate",
        6.0,
    )

    current_term_months = int(
        get_numeric_value(
            current_result,
            "loan_term_months",
            360,
        )
    )

    current_dti = get_numeric_value(
        current_result,
        "debt_to_income_ratio",
        36,
    )

    st.subheader("Build a New Scenario")

    input_left, input_right = st.columns(
        2,
        gap="large",
    )

    with input_left:
        simulated_income = st.number_input(
            "Annual Income",
            min_value=1000.0,
            max_value=1000000.0,
            value=float(current_income),
            step=5000.0,
            format="%.0f",
            key="simulator_income",
        )

        simulated_loan_amount = st.number_input(
            "Requested Loan Amount",
            min_value=10000.0,
            max_value=5000000.0,
            value=float(current_loan_amount),
            step=10000.0,
            format="%.0f",
            key="simulator_loan_amount",
        )

        simulated_property_value = st.number_input(
            "Property Value",
            min_value=10000.0,
            max_value=10000000.0,
            value=float(current_property_value),
            step=10000.0,
            format="%.0f",
            key="simulator_property_value",
        )

    with input_right:
        simulated_interest_rate = st.slider(
            "Interest Rate",
            min_value=0.0,
            max_value=15.0,
            value=float(
                min(
                    max(
                        current_interest_rate,
                        0.0,
                    ),
                    15.0,
                )
            ),
            step=0.05,
            format="%.2f%%",
            key="simulator_interest_rate",
        )

        available_terms = [
            120,
            180,
            240,
            300,
            360,
        ]

        if current_term_months not in available_terms:
            available_terms.append(
                current_term_months
            )
            available_terms.sort()

        default_term_index = available_terms.index(
            current_term_months
        )

        simulated_term_months = st.select_slider(
            "Loan Term",
            options=available_terms,
            value=available_terms[
                default_term_index
            ],
            format_func=lambda months: (
                f"{months // 12} years"
            ),
            key="simulator_term",
        )

        simulated_dti = st.slider(
            "Debt-to-Income Ratio",
            min_value=0.0,
            max_value=80.0,
            value=float(
                min(
                    max(
                        current_dti,
                        0.0,
                    ),
                    80.0,
                )
            ),
            step=0.5,
            format="%.1f%%",
            key="simulator_dti",
        )

    simulated_ltv = (
        simulated_loan_amount
        / simulated_property_value
        * 100
        if simulated_property_value > 0
        else 0.0
    )

    estimated_equity = max(
        simulated_property_value
        - simulated_loan_amount,
        0.0,
    )

    preview_left, preview_middle, preview_right = st.columns(
        3,
        gap="medium",
    )

    with preview_left:
        st.metric(
            label="Calculated Loan-to-Value",
            value=f"{simulated_ltv:.1f}%",
        )

    with preview_middle:
        st.metric(
            label="Estimated Borrower Equity",
            value=format_currency(
                estimated_equity
            ),
        )

    with preview_right:
        st.metric(
            label="Selected Loan Duration",
            value=(
                f"{simulated_term_months // 12} years"
            ),
        )

    if simulated_loan_amount > simulated_property_value:
        st.warning(
            "The requested loan amount is higher than the property value, "
            "resulting in a loan-to-value ratio above 100%."
        )

    if simulated_income <= 0:
        st.error(
            "Annual income must be greater than zero."
        )
        return

    st.divider()

    try:
        simulated_result = run_mortgage_analysis(
            loan_amount=float(
                simulated_loan_amount
            ),
            annual_income=float(
                simulated_income
            ),
            property_value=float(
                simulated_property_value
            ),
            interest_rate=float(
                simulated_interest_rate
            ),
            loan_term=int(
                simulated_term_months
            ),
            loan_to_value_ratio=float(
                simulated_ltv
            ),
            debt_to_income_ratio=float(
                simulated_dti
            ),
            applicant_age=str(
                current_result.get(
                    "applicant_age",
                    "35-44",
                )
            ),
            derived_race=str(
                current_result.get(
                    "derived_race",
                    "Race Not Available",
                )
            ),
            derived_sex=str(
                current_result.get(
                    "derived_sex",
                    "Sex Not Available",
                )
            ),
            derived_ethnicity=str(
                current_result.get(
                    "derived_ethnicity",
                    "Ethnicity Not Available",
                )
            ),
        )

    except Exception as error:
        st.error(
            "The simulated scenario could not be calculated. "
            f"Technical details: {error}"
        )
        return

    current_health = calculate_financial_health_score(
        current_result
    )

    simulated_health = calculate_financial_health_score(
        simulated_result
    )

    show_decision_comparison(
        current_result=current_result,
        simulated_result=simulated_result,
    )

    st.divider()

    show_financial_comparison(
        current_result=current_result,
        simulated_result=simulated_result,
        current_health=current_health,
        simulated_health=simulated_health,
    )

    st.divider()

    show_component_comparison(
        current_health=current_health,
        simulated_health=simulated_health,
    )

    st.divider()

    show_recommendations(
        current_result=current_result,
        simulated_result=simulated_result,
        current_health=current_health,
        simulated_health=simulated_health,
    )

    st.divider()

    bottom_left, bottom_right = st.columns(
        2,
        gap="medium",
    )

    with bottom_left:
        if st.button(
            "← Return to Results",
            key="simulator_return_results_bottom",
            width="stretch",
        ):
            set_page(
                "results"
            )

    with bottom_right:
        if st.button(
            "Start a New Mortgage Analysis",
            key="simulator_new_analysis",
            type="primary",
            width="stretch",
        ):
            set_page(
                "approval"
            )