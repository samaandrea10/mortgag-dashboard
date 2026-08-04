import streamlit as st

from components.logo import create_logo
from utils.session import set_page


def show_home() -> None:
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
            max-width: 820px;
            margin: 0 auto;
            text-align: center;
            color: #b9c4d4;
            font-size: 18px;
            line-height: 1.8;
        ">
            NOVA is a machine-learning mortgage analytics platform
            that estimates approval probability, evaluates lending
            risk, presents model-performance evidence, and supports
            controlled feedback learning.
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

    (
        analysis_column,
        performance_column,
        feedback_column,
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
                    min-height:145px;
                    margin-bottom:22px;
                ">
                    Enter applicant and loan information to generate
                    approval probability, decline risk, affordability
                    indicators, and the estimated mortgage outcome.
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
                    min-height:145px;
                    margin-bottom:22px;
                ">
                    Review Accuracy, Precision, Recall, F1, ROC-AUC,
                    model comparisons, confusion matrix, validation
                    evidence, and feature importance.
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
                    prediction errors, and prepare observations for
                    controlled future model retraining.
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

    st.write("")

    metric_left, metric_center, metric_right = st.columns(
        3
    )

    with metric_left:
        st.metric(
            label="Model Output",
            value="Decision",
            help="Predicted mortgage application outcome.",
        )

    with metric_center:
        st.metric(
            label="Probability Analysis",
            value="Approval %",
            help="Estimated probability of approval.",
        )

    with metric_right:
        st.metric(
            label="Risk Analysis",
            value="Decline %",
            help="Estimated probability of decline.",
        )

    st.divider()

    st.caption(
        "NOVA provides predictive analytics for educational and "
        "analytical purposes. It does not replace an official lender "
        "decision."
    )