from __future__ import annotations

import streamlit as st

from utils.financial_health import (
    calculate_financial_health_score,
    get_score_status,
)
from utils.pdf_report import (
    create_pdf_filename,
    generate_mortgage_pdf,
)
from utils.session import (
    clear_analysis_result,
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


def build_banking_summary(result: dict) -> list[str]:
    """
    Generate a banking-oriented interpretation based on
    the applicant's financial indicators.
    """
    conclusions: list[str] = []

    payment_ratio = float(result["payment_to_income_ratio"])
    ltv_ratio = float(result["loan_to_value_ratio"])
    dti_ratio = float(result["debt_to_income_ratio"])

    if payment_ratio <= 28:
        conclusions.append(
            "The estimated mortgage payment represents a healthy "
            "share of the applicant's monthly income."
        )
    elif payment_ratio <= 36:
        conclusions.append(
            "The estimated mortgage payment is within a moderate "
            "affordability range."
        )
    else:
        conclusions.append(
            "The estimated mortgage payment represents a relatively "
            "high share of the applicant's monthly income."
        )

    if ltv_ratio <= 80:
        conclusions.append(
            "The loan-to-value ratio indicates a relatively strong "
            "equity position."
        )
    elif ltv_ratio <= 90:
        conclusions.append(
            "The loan-to-value ratio is elevated but remains within "
            "a commonly observed lending range."
        )
    else:
        conclusions.append(
            "The high loan-to-value ratio may increase lending risk "
            "and reduce the applicant's financial flexibility."
        )

    if dti_ratio <= 36:
        conclusions.append(
            "The reported debt-to-income ratio suggests a manageable "
            "overall debt burden."
        )
    elif dti_ratio <= 43:
        conclusions.append(
            "The reported debt-to-income ratio should be reviewed "
            "carefully during lender verification."
        )
    else:
        conclusions.append(
            "The reported debt-to-income ratio may represent a "
            "significant affordability concern."
        )

    return conclusions


def build_pdf_data(
    result: dict,
    financial_health: dict,
) -> tuple[dict, dict]:
    """
    Convert the NOVA result into the structure required by
    the professional PDF generator.
    """
    applicant_data = {
        "applicant_name": result.get(
            "applicant_name",
            result.get("full_name", "Applicant"),
        ),
        "applicant_age": result.get(
            "applicant_age",
            "Not provided",
        ),
        "annual_income": result.get(
            "annual_income",
            0,
        ),
        "income": result.get(
            "annual_income",
            0,
        ),
        "derived_sex": result.get(
            "derived_sex",
            "Not provided",
        ),
        "derived_race": result.get(
            "derived_race",
            "Not provided",
        ),
        "derived_ethnicity": result.get(
            "derived_ethnicity",
            "Not provided",
        ),
        "loan_amount": result.get(
            "loan_amount",
            0,
        ),
        "property_value": result.get(
            "property_value",
            0,
        ),
        "interest_rate": result.get(
            "interest_rate",
            0,
        ),
        "loan_term": result.get(
            "loan_term_years",
            30,
        ),
        "loan_term_years": result.get(
            "loan_term_years",
            30,
        ),
        "debt_to_income_ratio": result.get(
            "debt_to_income_ratio",
            0,
        ),
        "loan_purpose": result.get(
            "loan_purpose",
            "Mortgage financing",
        ),
        "property_type": result.get(
            "property_type",
            "Residential property",
        ),
    }

    result_data = {
        **result,
        "decision": result.get(
            "predicted_decision",
            (
                "Approved"
                if int(result.get("prediction", 0)) == 1
                else "Declined"
            ),
        ),
        "approval_probability": result.get(
            "approval_probability",
            0,
        ),
        "decline_probability": result.get(
            "decline_probability",
            0,
        ),
        "risk_level": result.get(
            "risk_level",
            "Moderate",
        ),
        "monthly_payment": result.get(
            "monthly_payment",
            0,
        ),
        "total_interest": result.get(
            "total_interest",
            0,
        ),
        "total_repayment": result.get(
            "total_payment",
            result.get("total_repayment", 0),
        ),
        "total_payment": result.get(
            "total_payment",
            0,
        ),
        "loan_to_value_ratio": result.get(
            "loan_to_value_ratio",
            0,
        ),
        "debt_to_income_ratio": result.get(
            "debt_to_income_ratio",
            0,
        ),
        "payment_to_income_ratio": result.get(
            "payment_to_income_ratio",
            0,
        ),
        "payment_to_income": result.get(
            "payment_to_income_ratio",
            0,
        ),
        "financial_health_score": financial_health["score"],
        "financial_health_classification": (
            financial_health["classification"]
        ),
        "financial_health_risk_band": (
            financial_health["risk_band"]
        ),
    }

    return applicant_data, result_data


def create_pdf_report(
    result: dict,
    financial_health: dict,
) -> tuple[bytes | None, str | None]:
    """
    Generate the NOVA PDF report safely.
    """
    try:
        applicant_data, result_data = build_pdf_data(
            result=result,
            financial_health=financial_health,
        )

        feature_importance = result.get(
            "feature_importance",
            {},
        )

        pdf_bytes = generate_mortgage_pdf(
            applicant_data=applicant_data,
            result_data=result_data,
            feature_importance=feature_importance,
            logo_path=None,
        )

        pdf_filename = create_pdf_filename(
            applicant_data=applicant_data,
        )

        return pdf_bytes, pdf_filename

    except Exception as error:
        st.error(
            "The PDF report could not be generated. "
            f"Technical details: {error}"
        )
        return None, None


def show_financial_health_score(
    financial_health: dict,
) -> None:
    """
    Display the NOVA Financial Health Score using stable
    Streamlit components.
    """
    score = int(financial_health["score"])
    classification = str(
        financial_health["classification"]
    )
    risk_band = str(
        financial_health["risk_band"]
    )
    summary = str(
        financial_health["summary"]
    )

    status = get_score_status(score)

    st.subheader("NOVA Financial Health Score")

    score_column, profile_column = st.columns(
        [1, 2.4],
        gap="large",
        vertical_alignment="center",
    )

    with score_column:
        st.metric(
            label="Financial Health Index",
            value=f"{score}/100",
        )

        progress_value = max(
            0.0,
            min(1.0, score / 100),
        )

        st.progress(progress_value)

        st.caption(
            f"{status['icon']} {status['label']} profile"
        )

    with profile_column:
        if score >= 80:
            st.success(
                f"### {classification}\n\n"
                f"**{risk_band}**\n\n"
                f"{summary}"
            )
        elif score >= 60:
            st.warning(
                f"### {classification}\n\n"
                f"**{risk_band}**\n\n"
                f"{summary}"
            )
        else:
            st.error(
                f"### {classification}\n\n"
                f"**{risk_band}**\n\n"
                f"{summary}"
            )

    st.markdown("#### Score Components")

    component_scores = financial_health["component_scores"]

    first_row_left, first_row_middle, first_row_right = st.columns(
        3,
        gap="medium",
    )

    with first_row_left:
        approval_score = float(
            component_scores["Approval Strength"]
        )

        st.metric(
            label="Approval Strength",
            value=f"{approval_score:.0f}/100",
        )

        st.progress(
            max(
                0.0,
                min(1.0, approval_score / 100),
            )
        )

    with first_row_middle:
        debt_score = float(
            component_scores["Debt Management"]
        )

        st.metric(
            label="Debt Management",
            value=f"{debt_score:.0f}/100",
        )

        st.progress(
            max(
                0.0,
                min(1.0, debt_score / 100),
            )
        )

    with first_row_right:
        equity_score = float(
            component_scores["Equity Position"]
        )

        st.metric(
            label="Equity Position",
            value=f"{equity_score:.0f}/100",
        )

        st.progress(
            max(
                0.0,
                min(1.0, equity_score / 100),
            )
        )

    second_row_left, second_row_right = st.columns(
        2,
        gap="medium",
    )

    with second_row_left:
        affordability_score = float(
            component_scores["Mortgage Affordability"]
        )

        st.metric(
            label="Mortgage Affordability",
            value=f"{affordability_score:.0f}/100",
        )

        st.progress(
            max(
                0.0,
                min(1.0, affordability_score / 100),
            )
        )

    with second_row_right:
        income_score = float(
            component_scores["Income Capacity"]
        )

        st.metric(
            label="Income Capacity",
            value=f"{income_score:.0f}/100",
        )

        st.progress(
            max(
                0.0,
                min(1.0, income_score / 100),
            )
        )

    with st.expander(
        "View Financial Strengths and Areas for Attention"
    ):
        strengths_column, concerns_column = st.columns(
            2,
            gap="large",
        )

        with strengths_column:
            st.markdown("#### Financial Strengths")

            for strength in financial_health["strengths"]:
                st.success(strength)

        with concerns_column:
            st.markdown("#### Areas for Attention")

            concerns = financial_health["concerns"]

            no_major_concerns = (
                len(concerns) == 1
                and concerns[0].startswith(
                    "No major affordability concerns"
                )
            )

            for concern in concerns:
                if no_major_concerns:
                    st.info(concern)
                else:
                    st.warning(concern)

    st.caption(
        "The NOVA Financial Health Score combines predictive approval "
        "strength, debt burden, borrower equity, mortgage affordability, "
        "and income capacity. It is an analytical indicator and does not "
        "replace formal lender underwriting."
    )


def show_results() -> None:
    """
    Display the main mortgage analysis results summary.
    """
    result = get_analysis_result()

    if result is None:
        st.warning(
            "No mortgage analysis is currently available. "
            "Please complete an application first."
        )

        if st.button(
            "Start Mortgage Analysis",
            key="results_start_analysis",
            type="primary",
            width="stretch",
        ):
            set_page("approval")

        return

    financial_health = calculate_financial_health_score(
        result
    )

    top_left, home_column, new_analysis_column = st.columns(
        [5, 1, 1.35],
        vertical_alignment="center",
    )

    with top_left:
        st.markdown(
            "<p class='nova-kicker'>NOVA MORTGAGE INTELLIGENCE</p>",
            unsafe_allow_html=True,
        )
        st.title("Mortgage Analysis Results")

    with home_column:
        if st.button(
            "🏠 Home",
            key="results_home_top",
            width="stretch",
        ):
            set_page("home")

    with new_analysis_column:
        if st.button(
            "🔄 New Analysis",
            key="results_new_analysis_top",
            type="primary",
            width="stretch",
        ):
            clear_analysis_result()
            set_page("approval")

    st.divider()

    prediction = int(
        result["prediction"]
    )

    approval_probability = float(
        result["approval_probability"]
    )

    decline_probability = float(
        result["decline_probability"]
    )

    if prediction == 1:
        st.success(
            f"### ✓ {result['predicted_decision']}\n\n"
            "The applicant's current profile demonstrates a "
            "favorable mortgage approval outlook."
        )
    else:
        st.error(
            f"### ⚠ {result['predicted_decision']}\n\n"
            "The applicant's current profile contains factors that "
            "may reduce the likelihood of mortgage approval."
        )

    st.caption(
        "This result is a machine-learning estimate and does not "
        "represent an official lender decision."
    )

    st.subheader("Decision Overview")

    (
        decision_column,
        approval_column,
        decline_column,
        risk_column,
    ) = st.columns(
        4,
        gap="medium",
    )

    with decision_column:
        st.metric(
            label="Predicted Decision",
            value=(
                "Approved Profile"
                if prediction == 1
                else "Higher-Risk Profile"
            ),
        )

    with approval_column:
        st.metric(
            label="Approval Probability",
            value=format_percentage(
                approval_probability
            ),
        )

    with decline_column:
        st.metric(
            label="Decline Risk",
            value=format_percentage(
                decline_probability
            ),
        )

    with risk_column:
        st.metric(
            label="Risk Level",
            value=result["risk_level"],
        )

    st.divider()

    show_financial_health_score(
        financial_health
    )

    st.divider()

    st.subheader("Mortgage Summary")

    (
        payment_column,
        term_column,
        interest_column,
        repayment_column,
    ) = st.columns(
        4,
        gap="medium",
    )

    with payment_column:
        st.metric(
            label="Estimated Monthly Payment",
            value=format_currency(
                float(result["monthly_payment"])
            ),
        )

    with term_column:
        st.metric(
            label="Loan Duration",
            value=f"{result['loan_term_years']} years",
        )

    with interest_column:
        st.metric(
            label="Total Estimated Interest",
            value=format_currency(
                float(result["total_interest"])
            ),
        )

    with repayment_column:
        st.metric(
            label="Total Estimated Repayment",
            value=format_currency(
                float(result["total_payment"])
            ),
        )

    st.divider()

    summary_left, summary_right = st.columns(
        [1.3, 1],
        gap="large",
    )

    with summary_left:
        st.subheader("Quick Banking Summary")

        banking_summary = build_banking_summary(
            result
        )

        for conclusion in banking_summary:
            st.write(
                f"• {conclusion}"
            )

    with summary_right:
        st.subheader("Key Financial Indicators")

        st.metric(
            label="Payment-to-Income Ratio",
            value=(
                f"{float(result['payment_to_income_ratio']):.1f}%"
            ),
        )

        indicator_left, indicator_right = st.columns(
            2
        )

        with indicator_left:
            st.metric(
                label="Loan-to-Value",
                value=(
                    f"{float(result['loan_to_value_ratio']):.1f}%"
                ),
            )

        with indicator_right:
            st.metric(
                label="Debt-to-Income",
                value=(
                    f"{float(result['debt_to_income_ratio']):.1f}%"
                ),
            )

    st.divider()

    with st.expander(
        "View Applicant and Loan Details"
    ):
        details_left, details_right = st.columns(
            2,
            gap="large",
        )

        with details_left:
            st.write(
                f"**Loan Amount:** "
                f"{format_currency(float(result['loan_amount']))}"
            )

            st.write(
                f"**Property Value:** "
                f"{format_currency(float(result['property_value']))}"
            )

            st.write(
                f"**Annual Income:** "
                f"{format_currency(float(result['annual_income']))}"
            )

            st.write(
                f"**Interest Rate:** "
                f"{float(result['interest_rate']):.2f}%"
            )

            st.write(
                f"**Prediction Confidence:** "
                f"{result['confidence']}"
            )

        with details_right:
            st.write(
                f"**Applicant Age:** "
                f"{result['applicant_age']}"
            )

            st.write(
                f"**Applicant Sex:** "
                f"{result['derived_sex']}"
            )

            st.write(
                f"**Applicant Race:** "
                f"{result['derived_race']}"
            )

            st.write(
                f"**Applicant Ethnicity:** "
                f"{result['derived_ethnicity']}"
            )

    st.divider()

    st.subheader("Decision Support Center")

    (
        analysis_column,
        advisor_column,
        simulator_column,
        report_column,
    ) = st.columns(
        4,
        gap="medium",
    )

    with analysis_column:
        if st.button(
            "Detailed Analysis",
            key="results_open_detailed_analysis",
            type="primary",
            width="stretch",
        ):
            set_page(
                "detailed_analysis"
            )

    with advisor_column:
        if st.button(
            "AI Advisor",
            key="results_open_ai_advisor",
            type="primary",
            width="stretch",
        ):
            set_page(
                "advisor"
            )

    with simulator_column:
        if st.button(
            "Scenario Analysis",
            key="results_open_simulator",
            type="primary",
            width="stretch",
        ):
            set_page(
                "simulator"
            )

    pdf_bytes, pdf_filename = create_pdf_report(
        result=result,
        financial_health=financial_health,
    )

    with report_column:
        if (
            pdf_bytes is not None
            and pdf_filename is not None
        ):
            st.download_button(
                label="Professional Report",
                data=pdf_bytes,
                file_name=pdf_filename,
                mime="application/pdf",
                key="results_download_pdf_report",
                type="primary",
                width="stretch",
            )
        else:
            st.button(
                "Report Unavailable",
                key="results_pdf_unavailable",
                type="primary",
                disabled=True,
                width="stretch",
            )

    st.caption(
        "Review the detailed analysis, receive personalized guidance, "
        "test alternative scenarios, or download the professional NOVA report."
    )