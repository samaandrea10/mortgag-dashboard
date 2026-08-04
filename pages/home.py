import streamlit as st

from components.logo import create_logo
from utils.session import set_page


def show_home() -> None:
    """
    Display the NOVA home page and main navigation.
    """

    st.markdown(
        """
        <p style="
            text-align: center;
            color: #d7b76c;
            font-weight: 800;
            letter-spacing: 3px;
            margin-bottom: 8px;
        ">
            AI-POWERED MORTGAGE INTELLIGENCE
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <h1 style="
            text-align: center;
            font-size: 64px;
            margin-top: 0;
            margin-bottom: 12px;
        ">
            Welcome to
            <span style="color:#d7b76c;">NOVA</span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="
            max-width: 900px;
            margin: 0 auto;
            text-align: center;
            color: #b9c4d4;
            font-size: 18px;
            line-height: 1.8;
        ">
            NOVA is an end-to-end Machine Learning mortgage analytics
            platform that combines approval prediction, financial-risk
            assessment, interactive data exploration, model-performance
            evaluation, and controlled feedback learning.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    left_space, logo_column, right_space = st.columns(
        [2, 1, 2]
    )

    with logo_column:
        st.image(
            create_logo(),
            width="stretch",
        )

    st.divider()

    # ---------------------------------------------------------
    # Main platform statistics
    # ---------------------------------------------------------

    (
        dataset_column,
        accuracy_column,
        auc_column,
        model_column,
    ) = st.columns(
        4,
        gap="small",
    )

    with dataset_column:
        st.metric(
            label="Processed Applications",
            value="50,000",
            help=(
                "Representative mortgage applications from the "
                "processed 2023 HMDA dataset."
            ),
        )

    with accuracy_column:
        st.metric(
            label="Final Model Accuracy",
            value="97.08%",
            help=(
                "Accuracy achieved by the tuned Random Forest "
                "on the held-out testing dataset."
            ),
        )

    with auc_column:
        st.metric(
            label="ROC-AUC",
            value="0.995",
            help=(
                "The final model's ability to distinguish between "
                "approved and denied applications."
            ),
        )

    with model_column:
        st.metric(
            label="Production Model",
            value="Random Forest",
            help=(
                "The tuned Random Forest classifier selected "
                "for deployment."
            ),
        )

    st.divider()

    # ---------------------------------------------------------
    # Primary navigation row
    # ---------------------------------------------------------

    (
        analysis_column,
        performance_column,
        insights_column,
    ) = st.columns(
        3,
        gap="large",
    )

    with analysis_column:
        with st.container(border=True):
            st.markdown(
                """
                <h2 style="
                    text-align:center;
                    margin-bottom:8px;
                ">
                     Mortgage Analysis
                </h2>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="
                    text-align:center;
                    color:#b9c4d4;
                    line-height:1.7;
                    min-height:150px;
                    margin-bottom:22px;
                ">
                    Enter applicant and loan information to generate
                    approval probability, decline risk, affordability
                    indicators, financial health analysis, and the
                    estimated mortgage outcome.
                </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Analyze Application",
                key="home_analysis_button",
                width="stretch",
                type="primary",
            ):
                set_page("approval")

    with performance_column:
        with st.container(border=True):
            st.markdown(
                """
                <h2 style="
                    text-align:center;
                    margin-bottom:8px;
                ">
                    Model Performance
                </h2>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="
                    text-align:center;
                    color:#b9c4d4;
                    line-height:1.7;
                    min-height:150px;
                    margin-bottom:22px;
                ">
                    Review Accuracy, Precision, Recall, F1-Score,
                    ROC-AUC, confusion matrix, model comparisons,
                    cross-validation evidence, and feature importance.
                </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "View Model Performance",
                key="home_model_performance_button",
                width="stretch",
            ):
                set_page("model_performance")

    with insights_column:
        with st.container(border=True):
            st.markdown(
                """
                <h2 style="
                    text-align:center;
                    margin-bottom:8px;
                ">
                     Data Insights
                </h2>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="
                    text-align:center;
                    color:#b9c4d4;
                    line-height:1.7;
                    min-height:150px;
                    margin-bottom:22px;
                ">
                    Explore interactive HMDA visualizations, approval
                    patterns, financial-variable distributions, and
                    relationships between applicant characteristics
                    and historical mortgage outcomes.
                </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Explore Data Insights",
                key="home_data_insights_button",
                width="stretch",
            ):
                set_page("data_insights")

    st.write("")

    # ---------------------------------------------------------
    # Secondary navigation row
    # ---------------------------------------------------------

    left_space, feedback_column, about_column, right_space = (
        st.columns(
            [0.35, 1, 1, 0.35],
            gap="large",
        )
    )

    with feedback_column:
        with st.container(border=True):
            st.markdown(
                """
                <h2 style="
                    text-align:center;
                    margin-bottom:8px;
                ">
                     Model Feedback
                </h2>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="
                    text-align:center;
                    color:#b9c4d4;
                    line-height:1.7;
                    min-height:145px;
                    margin-bottom:22px;
                ">
                    Record verified real-world outcomes, monitor
                    prediction errors, evaluate feedback accuracy,
                    and prepare reliable observations for controlled
                    future model retraining.
                </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Open Feedback Center",
                key="home_model_feedback_button",
                width="stretch",
            ):
                set_page("model_feedback")

    with about_column:
        with st.container(border=True):
            st.markdown(
                """
                <h2 style="
                    text-align:center;
                    margin-bottom:8px;
                ">
                    About NOVA
                </h2>
                """,
                unsafe_allow_html=True,
            )

            st.markdown(
                """
                <p style="
                    text-align:center;
                    color:#b9c4d4;
                    line-height:1.7;
                    min-height:145px;
                    margin-bottom:22px;
                ">
                    Discover the project objective, HMDA dataset,
                    Machine Learning lifecycle, platform architecture,
                    technology stack, academic contribution, and
                    responsible-use principles.
                </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Explore the Project",
                key="home_about_button",
                width="stretch",
            ):
                set_page("about")

    st.divider()

    # ---------------------------------------------------------
    # Platform capabilities
    # ---------------------------------------------------------

    st.subheader("NOVA Platform Capabilities")

    capability_left, capability_center, capability_right = st.columns(
        3,
        gap="large",
    )

    with capability_left:
        with st.container(border=True):
            st.markdown("### Predictive Intelligence")
            st.markdown(
                """
                - Mortgage outcome prediction
                - Approval probability
                - Decline probability
                - Risk classification
                - Prediction confidence
                """
            )

    with capability_center:
        with st.container(border=True):
            st.markdown("### Financial Intelligence")
            st.markdown(
                """
                - Monthly payment estimation
                - Total repayment calculation
                - LTV and DTI assessment
                - Financial Health Score
                - Banking-oriented conclusions
                """
            )

    with capability_right:
        with st.container(border=True):
            st.markdown("### Model Governance")
            st.markdown(
                """
                - Performance monitoring
                - Fairness analysis
                - Feature importance
                - Verified outcome feedback
                - Controlled retraining workflow
                """
            )

    st.divider()

    st.caption(
        "NOVA provides predictive analytics for academic, educational, "
        "and analytical purposes. It does not replace an official lender "
        "decision, formal underwriting, or professional financial advice."
    )