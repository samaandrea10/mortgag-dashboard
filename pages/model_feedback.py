from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.feedback import (
    build_feedback_record,
    feedback_to_csv_bytes,
    get_feedback_summary,
    load_feedback_data,
    save_feedback_record,
)
from utils.session import (
    get_analysis_result,
    mark_feedback_submitted,
    set_page,
    was_feedback_submitted,
)


def _format_probability(
    value: float | int | None,
) -> str:
    """
    Format a decimal probability as a percentage.
    """

    if value is None:
        return "N/A"

    return f"{float(value) * 100:.1f}%"


def _create_feedback_outcome_chart(
    actual_approved: int,
    actual_denied: int,
):
    """
    Create a chart of verified actual outcomes.
    """

    chart_data = pd.DataFrame(
        {
            "Actual Outcome": [
                "Approved",
                "Denied",
            ],
            "Observations": [
                actual_approved,
                actual_denied,
            ],
        }
    )

    figure = px.bar(
        chart_data,
        x="Actual Outcome",
        y="Observations",
        text="Observations",
        title="Verified Actual Outcomes",
    )

    figure.update_traces(
        textposition="outside",
    )

    figure.update_layout(
        showlegend=False,
        height=430,
        yaxis_title="Number of Observations",
        xaxis_title="Actual Mortgage Outcome",
    )

    return figure


def show_model_feedback() -> None:
    """
    Display the controlled model-feedback interface.
    """

    back_column, title_column = st.columns(
        [1, 5],
        vertical_alignment="top",
    )

    with back_column:
        if st.button(
            "← Back",
            key="model_feedback_back_button",
            width="stretch",
        ):
            set_page("home")

    with title_column:
        st.markdown(
            (
                "<p class='nova-kicker'>"
                "CONTROLLED FEEDBACK LEARNING"
                "</p>"
            ),
            unsafe_allow_html=True,
        )

        st.title("Model Feedback")

        st.write(
            "Record a verified real-world mortgage outcome after "
            "the model has produced a prediction. Verified feedback "
            "can later be reviewed and incorporated into a controlled "
            "offline model-retraining process."
        )

    st.divider()

    analysis_result = get_analysis_result()

    if analysis_result is None:
        st.warning(
            "No mortgage prediction is currently available. "
            "Complete a mortgage application analysis before "
            "submitting an actual outcome."
        )

        action_left, action_right = st.columns(2)

        with action_left:
            if st.button(
                "Analyze Mortgage Application",
                key="feedback_start_analysis_button",
                width="stretch",
                type="primary",
            ):
                set_page("approval")

        with action_right:
            if st.button(
                "Return to Home",
                key="feedback_return_home_button",
                width="stretch",
            ):
                set_page("home")

    else:
        st.subheader("Current Prediction")

        (
            prediction_column,
            approval_column,
            decline_column,
            risk_column,
        ) = st.columns(
            4,
            gap="small",
        )

        predicted_target = int(
            analysis_result.get("prediction", 0)
        )

        predicted_outcome = (
            "Approved"
            if predicted_target == 1
            else "Denied"
        )

        with prediction_column:
            st.metric(
                label="Predicted Outcome",
                value=predicted_outcome,
            )

        with approval_column:
            st.metric(
                label="Approval Probability",
                value=_format_probability(
                    analysis_result.get(
                        "approval_probability"
                    )
                ),
            )

        with decline_column:
            st.metric(
                label="Decline Probability",
                value=_format_probability(
                    analysis_result.get(
                        "decline_probability"
                    )
                ),
            )

        with risk_column:
            st.metric(
                label="Risk Level",
                value=str(
                    analysis_result.get(
                        "risk_level",
                        "N/A",
                    )
                ),
            )

        with st.expander(
            "View Application Details"
        ):
            details_data = pd.DataFrame(
                {
                    "Variable": [
                        "Loan Amount",
                        "Annual Income",
                        "Property Value",
                        "Interest Rate",
                        "Loan Term",
                        "Loan-to-Value Ratio",
                        "Debt-to-Income Ratio",
                        "Applicant Age",
                        "Race",
                        "Sex",
                        "Ethnicity",
                    ],
                    "Value": [
                        (
                            f"${float(analysis_result.get('loan_amount', 0)):,.0f}"
                        ),
                        (
                            f"${float(analysis_result.get('annual_income', 0)):,.0f}"
                        ),
                        (
                            f"${float(analysis_result.get('property_value', 0)):,.0f}"
                        ),
                        (
                            f"{float(analysis_result.get('interest_rate', 0)):.2f}%"
                        ),
                        (
                            f"{int(analysis_result.get('loan_term_months', 0))} months"
                        ),
                        (
                            f"{float(analysis_result.get('loan_to_value_ratio', 0)):.1f}%"
                        ),
                        (
                            f"{float(analysis_result.get('debt_to_income_ratio', 0)):.1f}%"
                        ),
                        analysis_result.get(
                            "applicant_age",
                            "N/A",
                        ),
                        analysis_result.get(
                            "derived_race",
                            "N/A",
                        ),
                        analysis_result.get(
                            "derived_sex",
                            "N/A",
                        ),
                        analysis_result.get(
                            "derived_ethnicity",
                            "N/A",
                        ),
                    ],
                }
            )

            st.dataframe(
                details_data,
                width="stretch",
                hide_index=True,
            )

        st.divider()

        st.subheader("Submit Verified Actual Outcome")

        st.info(
            "Feedback should be submitted only when the actual "
            "mortgage decision is known and has been verified."
        )

        if was_feedback_submitted():
            st.success(
                "Feedback has already been submitted for the "
                "current prediction."
            )

        else:
            with st.form(
                "model_feedback_form"
            ):
                actual_outcome = st.radio(
                    "What was the verified actual outcome?",
                    options=[
                        "Approved",
                        "Denied",
                    ],
                    horizontal=True,
                )

                verified_outcome = st.checkbox(
                    (
                        "I confirm that this outcome is verified "
                        "and suitable for model monitoring."
                    ),
                    value=False,
                )

                reviewer_note = st.text_area(
                    "Reviewer Note — Optional",
                    placeholder=(
                        "Add contextual information about the "
                        "actual lending decision."
                    ),
                    max_chars=500,
                )

                submitted = st.form_submit_button(
                    "Submit Verified Feedback",
                    width="stretch",
                    type="primary",
                )

            if submitted:
                if not verified_outcome:
                    st.warning(
                        "Please confirm that the actual outcome "
                        "has been verified."
                    )

                else:
                    try:
                        feedback_record = (
                            build_feedback_record(
                                analysis_result=(
                                    analysis_result
                                ),
                                actual_outcome=(
                                    actual_outcome
                                ),
                                reviewer_note=(
                                    reviewer_note
                                ),
                                verified_outcome=True,
                            )
                        )

                        save_feedback_record(
                            feedback_record
                        )

                        mark_feedback_submitted(
                            feedback_record
                        )

                        if feedback_record[
                            "prediction_correct"
                        ]:
                            st.success(
                                "Feedback saved successfully. "
                                "The prediction matched the "
                                "verified actual outcome."
                            )

                        else:
                            st.warning(
                                "Feedback saved successfully. "
                                "A prediction error was recorded "
                                "for future model review."
                            )

                        st.rerun()

                    except Exception as error:
                        st.error(
                            "The feedback could not be saved. "
                            f"Technical details: {error}"
                        )

    st.divider()

    st.subheader("Feedback Monitoring Dashboard")

    feedback_summary = get_feedback_summary()

    (
        total_column,
        verified_column,
        correct_column,
        error_column,
        accuracy_column,
    ) = st.columns(
        5,
        gap="small",
    )

    with total_column:
        st.metric(
            label="Total Feedback",
            value=feedback_summary[
                "total_feedback"
            ],
        )

    with verified_column:
        st.metric(
            label="Verified Outcomes",
            value=feedback_summary[
                "verified_feedback"
            ],
        )

    with correct_column:
        st.metric(
            label="Correct Predictions",
            value=feedback_summary[
                "correct_predictions"
            ],
        )

    with error_column:
        st.metric(
            label="Prediction Errors",
            value=feedback_summary[
                "incorrect_predictions"
            ],
        )

    with accuracy_column:
        feedback_accuracy = feedback_summary[
            "feedback_accuracy"
        ]

        accuracy_text = (
            f"{feedback_accuracy * 100:.1f}%"
            if feedback_accuracy is not None
            else "N/A"
        )

        st.metric(
            label="Feedback Accuracy",
            value=accuracy_text,
        )

    feedback_data = load_feedback_data()

    if feedback_data.empty:
        st.info(
            "No feedback observations have been stored yet."
        )

    else:
        chart_column, table_column = st.columns(
            [1, 1.5],
            gap="large",
        )

        with chart_column:
            st.plotly_chart(
                _create_feedback_outcome_chart(
                    actual_approved=(
                        feedback_summary[
                            "actual_approved"
                        ]
                    ),
                    actual_denied=(
                        feedback_summary[
                            "actual_denied"
                        ]
                    ),
                ),
                width="stretch",
                config={
                    "displayModeBar": False,
                },
            )

        with table_column:
            st.markdown(
                "#### Most Recent Feedback"
            )

            recent_columns = [
                "feedback_timestamp_utc",
                "predicted_outcome",
                "actual_outcome",
                "prediction_correct",
                "approval_probability",
                "decline_probability",
            ]

            recent_feedback = (
                feedback_data[
                    recent_columns
                ]
                .tail(10)
                .sort_index(
                    ascending=False
                )
            )

            st.dataframe(
                recent_feedback,
                width="stretch",
                hide_index=True,
            )

        st.download_button(
            label="Download Feedback Dataset",
            data=feedback_to_csv_bytes(),
            file_name="feedback_data.csv",
            mime="text/csv",
            width="stretch",
        )

    st.divider()

    st.subheader("Controlled Retraining Policy")

    st.markdown(
        """
        Feedback observations are not used to retrain the production
        model immediately. The NOVA learning workflow follows a
        controlled human-in-the-loop process:

        1. Verified actual outcomes are collected.
        2. Prediction errors and data quality are reviewed.
        3. Verified feedback is combined with the original training data.
        4. A candidate model is trained offline.
        5. The candidate and current models are evaluated on the same
           held-out validation data.
        6. The production model is replaced only when the candidate
           demonstrates acceptable and improved performance.
        """
    )

    st.warning(
        "Streamlit Community Cloud uses temporary local storage. "
        "For a production system, verified feedback should be stored "
        "in a persistent database or managed cloud storage service."
    )

    st.caption(
        "This controlled process reduces the risk of data poisoning, "
        "unstable retraining and accidental degradation of the "
        "production model."
    )