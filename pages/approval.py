import streamlit as st

from utils.prediction import run_mortgage_analysis
from utils.session import save_analysis_result, set_page


def show_approval() -> None:
    """
    Display the mortgage application analysis form.
    """

    back_column, title_column = st.columns(
        [1, 5],
        vertical_alignment="top",
    )

    with back_column:
        if st.button(
            "← Back",
            key="approval_back_button",
            width="stretch",
        ):
            set_page("home")

    with title_column:
        st.markdown(
            "<p class='nova-kicker'>"
            "MORTGAGE APPLICATION ANALYSIS"
            "</p>",
            unsafe_allow_html=True,
        )

        st.title("Analyze Mortgage Application")

        st.write(
            "Enter the applicant and loan information below. "
            "NOVA will generate a separate results dashboard "
            "with approval probability, decline risk, estimated "
            "monthly payment, and banking-oriented conclusions."
        )

    st.divider()

    with st.form("mortgage_analysis_form"):
        st.subheader("Financial Information")

        financial_left, financial_right = st.columns(
            2,
            gap="large",
        )

        with financial_left:
            loan_amount = st.number_input(
                "Loan Amount ($)",
                min_value=0.0,
                value=250000.0,
                step=5000.0,
            )

            annual_income = st.number_input(
                "Annual Income ($)",
                min_value=0.0,
                value=75000.0,
                step=1000.0,
            )

            property_value = st.number_input(
                "Property Value ($)",
                min_value=0.0,
                value=320000.0,
                step=5000.0,
            )

            loan_term = st.selectbox(
                "Loan Term",
                options=[120, 180, 240, 300, 360],
                index=4,
                format_func=lambda months: (
                    f"{months // 12} years "
                    f"({months} months)"
                ),
            )

        with financial_right:
            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                max_value=30.0,
                value=6.5,
                step=0.1,
            )

            loan_to_value_ratio = st.number_input(
                "Loan-to-Value Ratio (%)",
                min_value=0.0,
                max_value=200.0,
                value=78.0,
                step=1.0,
            )

            debt_to_income_ratio = st.number_input(
                "Debt-to-Income Ratio (%)",
                min_value=0.0,
                max_value=100.0,
                value=35.0,
                step=1.0,
            )

        st.divider()

        st.subheader("Applicant Information")

        applicant_left, applicant_right = st.columns(
            2,
            gap="large",
        )

        with applicant_left:
            applicant_age = st.selectbox(
                "Applicant Age",
                options=[
                    "<25",
                    "25-34",
                    "35-44",
                    "45-54",
                    "55-64",
                    "65-74",
                    ">74",
                    "Unknown",
                ],
                index=2,
            )

            derived_sex = st.selectbox(
                "Applicant Sex",
                options=[
                    "Female",
                    "Male",
                    "Joint",
                    "Sex Not Available",
                ],
            )

        with applicant_right:
            derived_race = st.selectbox(
                "Applicant Race",
                options=[
                    "White",
                    "Black or African American",
                    "Asian",
                    "American Indian or Alaska Native",
                    "Native Hawaiian or Other Pacific Islander",
                    "Joint",
                    "Race Not Available",
                ],
            )

            derived_ethnicity = st.selectbox(
                "Applicant Ethnicity",
                options=[
                    "Not Hispanic or Latino",
                    "Hispanic or Latino",
                    "Joint",
                    "Ethnicity Not Available",
                ],
            )

        submitted = st.form_submit_button(
            "Analyze Mortgage Application",
            width="stretch",
            type="primary",
        )

    if not submitted:
        return

    # -----------------------------------------------------
    # Required-value validation
    # -----------------------------------------------------

    if loan_amount <= 0:
        st.warning(
            "Loan amount must be greater than zero."
        )
        return

    if annual_income <= 0:
        st.warning(
            "Annual income must be greater than zero."
        )
        return

    if property_value <= 0:
        st.warning(
            "Property value must be greater than zero."
        )
        return

    # -----------------------------------------------------
    # Informational notice only
    # This does not block the analysis.
    # -----------------------------------------------------

    calculated_ltv = (
        loan_amount / property_value
    ) * 100

    if calculated_ltv > 100:
        st.info(
            "The requested loan is higher than the stated "
            "property value. The analysis will continue, "
            "and this will be reflected in the risk assessment."
        )

    elif calculated_ltv > 95:
        st.info(
            "The requested loan represents a very high "
            "percentage of the property value. The analysis "
            "will continue, and this may increase lending risk."
        )

    # -----------------------------------------------------
    # Run analysis
    # -----------------------------------------------------

    try:
        analysis_result = run_mortgage_analysis(
            loan_amount=loan_amount,
            annual_income=annual_income,
            property_value=property_value,
            interest_rate=interest_rate,
            loan_term=loan_term,
            loan_to_value_ratio=loan_to_value_ratio,
            debt_to_income_ratio=debt_to_income_ratio,
            applicant_age=applicant_age,
            derived_race=derived_race,
            derived_sex=derived_sex,
            derived_ethnicity=derived_ethnicity,
        )

        save_analysis_result(analysis_result)
        set_page("results")

    except FileNotFoundError:
        st.error(
            "The model files were not found. Make sure "
            "`mortgage_pipeline.pkl` and "
            "`model_columns.pkl` are located in the main "
            "project folder."
        )

    except Exception as error:
        st.error(
            "The analysis could not be completed. "
            f"Technical details: {error}"
        )