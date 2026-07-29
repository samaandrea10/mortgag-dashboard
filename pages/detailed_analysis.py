from typing import Any

import plotly.graph_objects as go
import streamlit as st

from utils.session import get_analysis_result, set_page


def format_currency(value: float) -> str:
    """
    Format a numeric value as US currency.
    """
    return f"${value:,.0f}"


def format_probability(value: float) -> str:
    """
    Convert a decimal probability into a percentage.
    """
    return f"{value * 100:.1f}%"


def create_approval_gauge(
    approval_probability: float,
) -> go.Figure:
    """
    Create an interactive gauge showing approval probability.
    """
    approval_percentage = approval_probability * 100

    figure = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=approval_percentage,
            number={
                "suffix": "%",
                "font": {
                    "size": 42,
                },
            },
            title={
                "text": "Approval Probability",
                "font": {
                    "size": 20,
                },
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                },
                "bar": {
                    "color": "#D4AF5A",
                    "thickness": 0.28,
                },
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {
                        "range": [0, 40],
                        "color": "rgba(220, 53, 69, 0.30)",
                    },
                    {
                        "range": [40, 70],
                        "color": "rgba(255, 193, 7, 0.25)",
                    },
                    {
                        "range": [70, 100],
                        "color": "rgba(40, 167, 69, 0.25)",
                    },
                ],
                "threshold": {
                    "line": {
                        "color": "#FFFFFF",
                        "width": 3,
                    },
                    "thickness": 0.75,
                    "value": approval_percentage,
                },
            },
        )
    )

    figure.update_layout(
        height=350,
        margin={
            "l": 25,
            "r": 25,
            "t": 70,
            "b": 20,
        },
        paper_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "#F5F7FA",
        },
    )

    return figure


def create_probability_chart(
    approval_probability: float,
    decline_probability: float,
) -> go.Figure:
    """
    Create a donut chart comparing approval and decline probability.
    """
    figure = go.Figure(
        data=[
            go.Pie(
                labels=[
                    "Approval Probability",
                    "Decline Risk",
                ],
                values=[
                    approval_probability * 100,
                    decline_probability * 100,
                ],
                hole=0.68,
                textinfo="label+percent",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "%{value:.1f}%"
                    "<extra></extra>"
                ),
                marker={
                    "colors": [
                        "#D4AF5A",
                        "#A94442",
                    ],
                    "line": {
                        "color": "rgba(255,255,255,0.15)",
                        "width": 1,
                    },
                },
            )
        ]
    )

    figure.update_layout(
        title={
            "text": "Decision Probability Distribution",
            "x": 0.5,
            "xanchor": "center",
        },
        height=350,
        margin={
            "l": 20,
            "r": 20,
            "t": 70,
            "b": 20,
        },
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "#F5F7FA",
        },
        annotations=[
            {
                "text": "NOVA",
                "x": 0.5,
                "y": 0.5,
                "font": {
                    "size": 18,
                    "color": "#D4AF5A",
                },
                "showarrow": False,
            }
        ],
    )

    return figure


def create_loan_breakdown_chart(
    loan_amount: float,
    total_interest: float,
) -> go.Figure:
    """
    Create a chart showing principal and total estimated interest.
    """
    figure = go.Figure(
        data=[
            go.Bar(
                x=[
                    "Loan Principal",
                    "Total Interest",
                ],
                y=[
                    loan_amount,
                    total_interest,
                ],
                text=[
                    format_currency(loan_amount),
                    format_currency(total_interest),
                ],
                textposition="outside",
                marker={
                    "color": [
                        "#D4AF5A",
                        "#7A8799",
                    ],
                },
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "$%{y:,.0f}"
                    "<extra></extra>"
                ),
            )
        ]
    )

    figure.update_layout(
        title={
            "text": "Loan Cost Breakdown",
            "x": 0.5,
            "xanchor": "center",
        },
        height=390,
        margin={
            "l": 30,
            "r": 30,
            "t": 70,
            "b": 40,
        },
        yaxis={
            "title": "Amount ($)",
            "gridcolor": "rgba(255,255,255,0.08)",
            "tickprefix": "$",
            "tickformat": ",.0f",
        },
        xaxis={
            "title": "",
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "#F5F7FA",
        },
    )

    return figure


def create_affordability_chart(
    payment_to_income_ratio: float,
    debt_to_income_ratio: float,
    loan_to_value_ratio: float,
) -> go.Figure:
    """
    Compare the applicant's key financial ratios.
    """
    labels = [
        "Payment-to-Income",
        "Debt-to-Income",
        "Loan-to-Value",
    ]

    values = [
        payment_to_income_ratio,
        debt_to_income_ratio,
        loan_to_value_ratio,
    ]

    figure = go.Figure(
        data=[
            go.Bar(
                x=values,
                y=labels,
                orientation="h",
                text=[
                    f"{value:.1f}%"
                    for value in values
                ],
                textposition="outside",
                marker={
                    "color": [
                        "#D4AF5A",
                        "#8FA6BF",
                        "#6B7F95",
                    ],
                },
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "%{x:.1f}%"
                    "<extra></extra>"
                ),
            )
        ]
    )

    figure.update_layout(
        title={
            "text": "Applicant Financial Ratios",
            "x": 0.5,
            "xanchor": "center",
        },
        height=390,
        margin={
            "l": 30,
            "r": 50,
            "t": 70,
            "b": 40,
        },
        xaxis={
            "title": "Ratio (%)",
            "range": [
                0,
                max(
                    100,
                    max(values) + 15,
                ),
            ],
            "gridcolor": "rgba(255,255,255,0.08)",
        },
        yaxis={
            "title": "",
            "autorange": "reversed",
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            "color": "#F5F7FA",
        },
    )

    return figure


def get_ratio_interpretation(
    ratio_name: str,
    ratio_value: float,
) -> tuple[str, str]:
    """
    Return a status and interpretation for a financial ratio.
    """
    if ratio_name == "payment_to_income":
        if ratio_value <= 28:
            return (
                "Favorable",
                "The estimated mortgage payment represents a "
                "manageable portion of monthly income.",
            )

        if ratio_value <= 36:
            return (
                "Moderate",
                "The estimated payment is within a moderate "
                "affordability range.",
            )

        return (
            "Elevated",
            "The estimated payment consumes a relatively high "
            "portion of monthly income.",
        )

    if ratio_name == "debt_to_income":
        if ratio_value <= 36:
            return (
                "Favorable",
                "The applicant reports a manageable overall "
                "debt burden.",
            )

        if ratio_value <= 43:
            return (
                "Review Recommended",
                "The debt burden should be reviewed carefully "
                "during lender verification.",
            )

        return (
            "Elevated",
            "The reported debt-to-income ratio may represent "
            "an affordability concern.",
        )

    if ratio_value <= 80:
        return (
            "Favorable",
            "The loan-to-value ratio indicates a relatively "
            "strong equity position.",
        )

    if ratio_value <= 90:
        return (
            "Moderate",
            "The loan-to-value ratio is elevated and may require "
            "additional lender review.",
        )

    return (
        "Elevated",
        "The applicant has limited equity relative to the "
        "requested loan amount.",
    )


def display_ratio_analysis(
    title: str,
    ratio_name: str,
    ratio_value: float,
) -> None:
    """
    Display one financial ratio and its interpretation.
    """
    status, interpretation = get_ratio_interpretation(
        ratio_name=ratio_name,
        ratio_value=ratio_value,
    )

    st.metric(
        label=title,
        value=f"{ratio_value:.1f}%",
    )

    st.write(f"**Assessment:** {status}")
    st.caption(interpretation)


def show_detailed_analysis() -> None:
    """
    Display the advanced mortgage analysis dashboard.
    """
    result: dict[str, Any] | None = get_analysis_result()

    if result is None:
        st.warning(
            "No mortgage analysis is currently available. "
            "Please complete an application before opening "
            "the detailed analysis."
        )

        if st.button(
            "Start Mortgage Analysis",
            type="primary",
            width="stretch",
        ):
            set_page("approval")

        return

    navigation_column, title_column = st.columns(
        [1, 5],
        vertical_alignment="center",
    )

    with navigation_column:
        if st.button(
            "← Results",
            key="detailed_analysis_back",
            width="stretch",
        ):
            set_page("results")

    with title_column:
        st.markdown(
            "<p class='nova-kicker'>ADVANCED DECISION SUPPORT</p>",
            unsafe_allow_html=True,
        )

        st.title("Detailed Mortgage Analysis")

        st.write(
            "Explore the prediction, affordability indicators, "
            "loan structure, and applicant profile in greater detail."
        )

    st.divider()

    prediction = int(result["prediction"])
    approval_probability = float(
        result["approval_probability"]
    )
    decline_probability = float(
        result["decline_probability"]
    )

    if prediction == 1:
        st.success(
            "### ✓ Favorable Approval Outlook\n\n"
            "The current financial and applicant profile is "
            "classified by the model as more likely to be approved."
        )
    else:
        st.error(
            "### ⚠ Elevated Decline Risk\n\n"
            "The current financial and applicant profile contains "
            "factors associated with a higher likelihood of decline."
        )

    st.caption(
        "The prediction is an analytical estimate generated by a "
        "machine-learning model. It is not an official credit or "
        "lending decision."
    )

    st.subheader("Prediction Analysis")

    gauge_column, probability_column = st.columns(
        2,
        gap="large",
    )

    with gauge_column:
        gauge_figure = create_approval_gauge(
            approval_probability=approval_probability,
        )

        st.plotly_chart(
            gauge_figure,
            width="stretch",
            config={
                "displayModeBar": False,
            },
        )

    with probability_column:
        probability_figure = create_probability_chart(
            approval_probability=approval_probability,
            decline_probability=decline_probability,
        )

        st.plotly_chart(
            probability_figure,
            width="stretch",
            config={
                "displayModeBar": False,
            },
        )

    probability_left, probability_middle, probability_right = st.columns(
        3,
        gap="medium",
    )

    with probability_left:
        st.metric(
            label="Approval Probability",
            value=format_probability(
                approval_probability
            ),
        )

    with probability_middle:
        st.metric(
            label="Decline Risk",
            value=format_probability(
                decline_probability
            ),
        )

    with probability_right:
        st.metric(
            label="Prediction Confidence",
            value=result["confidence"],
        )

    st.divider()

    st.subheader("Affordability and Risk Indicators")

    ratio_left, ratio_middle, ratio_right = st.columns(
        3,
        gap="large",
    )

    with ratio_left:
        display_ratio_analysis(
            title="Payment-to-Income",
            ratio_name="payment_to_income",
            ratio_value=float(
                result["payment_to_income_ratio"]
            ),
        )

    with ratio_middle:
        display_ratio_analysis(
            title="Debt-to-Income",
            ratio_name="debt_to_income",
            ratio_value=float(
                result["debt_to_income_ratio"]
            ),
        )

    with ratio_right:
        display_ratio_analysis(
            title="Loan-to-Value",
            ratio_name="loan_to_value",
            ratio_value=float(
                result["loan_to_value_ratio"]
            ),
        )

    affordability_figure = create_affordability_chart(
        payment_to_income_ratio=float(
            result["payment_to_income_ratio"]
        ),
        debt_to_income_ratio=float(
            result["debt_to_income_ratio"]
        ),
        loan_to_value_ratio=float(
            result["loan_to_value_ratio"]
        ),
    )

    st.plotly_chart(
        affordability_figure,
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )

    st.divider()

    st.subheader("Mortgage Cost Analysis")

    payment_column, interest_column, repayment_column, term_column = st.columns(
        4,
        gap="medium",
    )

    with payment_column:
        st.metric(
            label="Monthly Payment",
            value=format_currency(
                float(result["monthly_payment"])
            ),
        )

    with interest_column:
        st.metric(
            label="Total Interest",
            value=format_currency(
                float(result["total_interest"])
            ),
        )

    with repayment_column:
        st.metric(
            label="Total Repayment",
            value=format_currency(
                float(result["total_payment"])
            ),
        )

    with term_column:
        st.metric(
            label="Loan Term",
            value=f"{result['loan_term_years']} years",
        )

    loan_breakdown_figure = create_loan_breakdown_chart(
        loan_amount=float(
            result["loan_amount"]
        ),
        total_interest=float(
            result["total_interest"]
        ),
    )

    st.plotly_chart(
        loan_breakdown_figure,
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )

    st.divider()

    applicant_column, loan_column = st.columns(
        2,
        gap="large",
    )

    with applicant_column:
        st.subheader("Applicant Profile")

        st.write(
            f"**Age Group:** {result['applicant_age']}"
        )
        st.write(
            f"**Sex:** {result['derived_sex']}"
        )
        st.write(
            f"**Race:** {result['derived_race']}"
        )
        st.write(
            f"**Ethnicity:** {result['derived_ethnicity']}"
        )
        st.write(
            f"**Annual Income:** "
            f"{format_currency(float(result['annual_income']))}"
        )
        st.write(
            f"**Monthly Income:** "
            f"{format_currency(float(result['monthly_income']))}"
        )

    with loan_column:
        st.subheader("Loan Profile")

        st.write(
            f"**Loan Amount:** "
            f"{format_currency(float(result['loan_amount']))}"
        )
        st.write(
            f"**Property Value:** "
            f"{format_currency(float(result['property_value']))}"
        )
        st.write(
            f"**Interest Rate:** "
            f"{float(result['interest_rate']):.2f}%"
        )
        st.write(
            f"**Loan Duration:** "
            f"{result['loan_term_years']} years "
            f"({result['loan_term_months']} months)"
        )
        st.write(
            f"**Risk Classification:** "
            f"{result['risk_level']}"
        )
        st.write(
            f"**Model Decision:** "
            f"{result['predicted_decision']}"
        )

    st.divider()

    footer_left, footer_right = st.columns(
        [1, 1],
        gap="medium",
    )

    with footer_left:
        if st.button(
            "← Return to Results",
            key="detailed_return_results",
            width="stretch",
        ):
            set_page("results")

    with footer_right:
        if st.button(
            "Open Scenario Simulator →",
            key="detailed_open_simulator",
            type="primary",
            width="stretch",
        ):
            set_page("simulator")
            