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
            max-width: 780px;
            margin: 0 auto;
            text-align: center;
            color: #b9c4d4;
            font-size: 18px;
            line-height: 1.8;
        ">
            NOVA is a machine-learning mortgage analytics platform that
            estimates approval probability, decline risk, and the predicted
            outcome of a mortgage application.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    left_space, logo_column, right_space = st.columns([2, 1, 2])

    with logo_column:
        st.image(
            create_logo(),
            width="stretch",
        )

    st.divider()

    left_space, main_column, right_space = st.columns([1, 2.2, 1])

    with main_column:
        with st.container(border=True):
            st.markdown(
                """
                <h2 style="text-align:center; margin-bottom:8px;">
                    Mortgage Application Analysis
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
                    margin-bottom:22px;
                ">
                    Enter the applicant and loan information to generate
                    a complete predictive analysis, including approval
                    probability, decline risk, and estimated decision.
                </p>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                "Analyze Mortgage Application",
                key="home_analysis_button",
                width="stretch",
                type="primary",
            ):
                set_page("approval")

    st.write("")

    metric_left, metric_center, metric_right = st.columns(3)

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
        "NOVA provides predictive analytics for educational and analytical "
        "purposes. It does not replace an official lender decision."
    )