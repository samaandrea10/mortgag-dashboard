from __future__ import annotations

import streamlit as st

from utils.session import set_page


def show_about() -> None:
    """
    Display the About NOVA project page.
    """

    back_column, title_column = st.columns(
        [1, 5],
        vertical_alignment="top",
    )

    with back_column:
        if st.button(
            "← Back",
            key="about_back_button",
            width="stretch",
        ):
            set_page("home")

    with title_column:
        st.markdown(
            (
                "<p class='nova-kicker'>"
                "PROJECT OVERVIEW AND ARCHITECTURE"
                "</p>"
            ),
            unsafe_allow_html=True,
        )

        st.title("About NOVA")

        st.write(
            "NOVA Mortgage Intelligence is an end-to-end Machine "
            "Learning platform developed to analyze mortgage "
            "applications, estimate approval probability, evaluate "
            "financial risk, and support transparent decision analysis."
        )

    st.divider()

    # ---------------------------------------------------------
    # Project summary
    # ---------------------------------------------------------

    st.subheader("Project Overview")

    overview_left, overview_center, overview_right = st.columns(
        3,
        gap="large",
    )

    with overview_left:
        with st.container(border=True):
            st.markdown("### 🎯 Objective")
            st.write(
                "Predict mortgage approval outcomes using financial "
                "and demographic applicant information."
            )

    with overview_center:
        with st.container(border=True):
            st.markdown("### 📊 Dataset")
            st.write(
                "2023 Home Mortgage Disclosure Act (HMDA) dataset, "
                "processed into a representative analytical sample."
            )

    with overview_right:
        with st.container(border=True):
            st.markdown("### 🤖 Final Model")
            st.write(
                "A tuned Random Forest classifier integrated into "
                "a complete Scikit-learn preprocessing pipeline."
            )

    st.divider()

    # ---------------------------------------------------------
    # Key performance
    # ---------------------------------------------------------

    st.subheader("Final Model Snapshot")

    metric_left, metric_center, metric_right, metric_fourth = st.columns(
        4,
        gap="small",
    )

    with metric_left:
        st.metric(
            label="Accuracy",
            value="97.08%",
            help="Testing accuracy of the final tuned Random Forest.",
        )

    with metric_center:
        st.metric(
            label="ROC-AUC",
            value="0.995",
            help=(
                "Ability to distinguish approved from denied "
                "applications across probability thresholds."
            ),
        )

    with metric_right:
        st.metric(
            label="Recall — Denied",
            value="96.51%",
            help=(
                "Share of actual denied applications correctly "
                "identified by the final model."
            ),
        )

    with metric_fourth:
        st.metric(
            label="Testing Sample",
            value="10,000",
            help="Held-out observations used for final evaluation.",
        )

    st.divider()

    # ---------------------------------------------------------
    # ML lifecycle
    # ---------------------------------------------------------

    st.subheader("Machine Learning Lifecycle")

    st.markdown(
        """
        ```text
        Original HMDA 2023 Data
                    ↓
        Data Cleaning and Filtering
                    ↓
        Feature Selection and Engineering
                    ↓
        Missing-Value Imputation
                    ↓
        Numerical Scaling and Categorical Encoding
                    ↓
        Logistic Regression Baseline
                    ↓
        Random Forest Training
                    ↓
        Hyperparameter Optimization
                    ↓
        Final Model Evaluation
                    ↓
        Streamlit Deployment
                    ↓
        Performance Monitoring and Controlled Feedback
        ```
        """
    )

    st.divider()

    # ---------------------------------------------------------
    # Architecture
    # ---------------------------------------------------------

    st.subheader("Platform Architecture")

    architecture_left, architecture_right = st.columns(
        2,
        gap="large",
    )

    with architecture_left:
        with st.container(border=True):
            st.markdown("### User Interaction Layer")
            st.markdown(
                """
                - Mortgage application form
                - Prediction results dashboard
                - Financial health analysis
                - Mortgage simulator
                - PDF reporting
                - Model feedback interface
                """
            )

    with architecture_right:
        with st.container(border=True):
            st.markdown("### Analytical Layer")
            st.markdown(
                """
                - Scikit-learn preprocessing pipeline
                - Tuned Random Forest classifier
                - Probability estimation
                - Financial risk rules
                - Model evaluation dashboard
                - Feedback monitoring
                """
            )

    st.markdown(
        """
        ```text
        User Input
            ↓
        Streamlit Interface
            ↓
        Preprocessing Pipeline
            ↓
        Random Forest Model
            ↓
        Probability and Decision
            ↓
        Financial Risk Assessment
            ↓
        Results, Insights, Feedback and PDF Report
        ```
        """
    )

    st.divider()

    # ---------------------------------------------------------
    # Capabilities
    # ---------------------------------------------------------

    st.subheader("Core Capabilities")

    capabilities_left, capabilities_center, capabilities_right = st.columns(
        3,
        gap="large",
    )

    with capabilities_left:
        with st.container(border=True):
            st.markdown("### Predictive Analytics")
            st.markdown(
                """
                - Approval prediction
                - Approval probability
                - Decline probability
                - Risk classification
                - Confidence assessment
                """
            )

    with capabilities_center:
        with st.container(border=True):
            st.markdown("### Financial Analytics")
            st.markdown(
                """
                - Monthly payment estimation
                - Total interest calculation
                - Loan-to-value assessment
                - Debt-to-income assessment
                - Financial Health Score
                """
            )

    with capabilities_right:
        with st.container(border=True):
            st.markdown("### Model Governance")
            st.markdown(
                """
                - Model comparison
                - Confusion matrix
                - ROC-AUC analysis
                - Feature importance
                - Controlled feedback learning
                """
            )

    st.divider()

    # ---------------------------------------------------------
    # Technologies
    # ---------------------------------------------------------

    st.subheader("Technology Stack")

    technology_data = [
        ("Python", "Core programming language"),
        ("Pandas", "Data preparation and analysis"),
        ("NumPy", "Numerical processing"),
        ("Scikit-learn", "Machine Learning pipeline and model"),
        ("Plotly", "Interactive data visualizations"),
        ("Streamlit", "Web application framework"),
        ("Joblib", "Model persistence"),
        ("ReportLab", "PDF report generation"),
        ("GitHub", "Version control and project transparency"),
        ("Streamlit Cloud", "Online deployment"),
    ]

    for row_start in range(0, len(technology_data), 2):
        row_columns = st.columns(2, gap="large")

        for column_index, technology in enumerate(
            technology_data[row_start:row_start + 2]
        ):
            with row_columns[column_index]:
                with st.container(border=True):
                    st.markdown(f"### {technology[0]}")
                    st.write(technology[1])

    st.divider()

    # ---------------------------------------------------------
    # Academic contribution
    # ---------------------------------------------------------

    st.subheader("Academic Contribution")

    st.markdown(
        """
        NOVA demonstrates the complete lifecycle of a modern Data
        Science system. The project integrates data preprocessing,
        exploratory analysis, supervised Machine Learning, model
        comparison, hyperparameter tuning, performance evaluation,
        fairness analysis, financial interpretation, interactive
        deployment, documentation, and controlled feedback collection.

        The system was designed not only to produce a prediction, but
        also to explain the financial context of the result and present
        evidence regarding the quality and stability of the deployed
        model.
        """
    )

    st.divider()

    # ---------------------------------------------------------
    # Responsible use
    # ---------------------------------------------------------

    st.subheader("Responsible Use and Limitations")

    st.warning(
        "NOVA is an academic analytical platform. It does not replace "
        "official lender underwriting, professional financial advice, "
        "or a binding mortgage decision."
    )

    st.markdown(
        """
        Important limitations include:

        - The model was trained on historical HMDA data.
        - Historical patterns may not fully represent future lending.
        - Predictions may reflect limitations present in the dataset.
        - Feature importance does not establish causality.
        - Financial calculations are estimates.
        - Human review remains necessary for high-impact decisions.
        """
    )

    st.divider()

    # ---------------------------------------------------------
    # Links and author
    # ---------------------------------------------------------

    st.subheader("Project Links")

    link_left, link_right = st.columns(
        2,
        gap="large",
    )

    with link_left:
        st.link_button(
            "Open Live Application",
            "https://mortgage-dashboard-sama.streamlit.app/",
            width="stretch",
            type="primary",
        )

    with link_right:
        st.link_button(
            "Open GitHub Repository",
            "https://github.com/samaandrea10/mortgag-dashboard",
            width="stretch",
        )

    st.divider()

    st.subheader("Author")

    with st.container(border=True):
        st.markdown("### Sama Andrea")
        st.write("B.Sc. Information Systems")
        st.write("Data Science Specialization")
        st.write("Final Capstone Project")

    st.caption(
        "NOVA Mortgage Intelligence — End-to-end Machine Learning "
        "mortgage analytics platform."
    )