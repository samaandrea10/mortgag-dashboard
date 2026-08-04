from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.session import set_page


# ---------------------------------------------------------
# Final model metrics
# Values were obtained from the final project notebook.
# ---------------------------------------------------------

FINAL_MODEL_METRICS = {
    "accuracy": 0.9708,
    "denied_precision": 0.9369,
    "denied_recall": 0.9651,
    "denied_f1": 0.9508,
    "roc_auc": 0.9950,
    "average_precision": 0.9967,
    "cv_mean_accuracy": 0.9703,
    "cv_standard_deviation": 0.00054,
}


# ---------------------------------------------------------
# Confusion matrix
# Rows: actual classes
# Columns: predicted classes
# ---------------------------------------------------------

FINAL_CONFUSION_MATRIX = [
    [2822, 102],
    [190, 6886],
]


# ---------------------------------------------------------
# Baseline model comparison
# ---------------------------------------------------------

BASELINE_COMPARISON = pd.DataFrame(
    {
        "Model": [
            "Logistic Regression",
            "Original Random Forest",
        ],
        "Accuracy": [
            0.7868,
            0.9678,
        ],
        "Precision": [
            0.7936,
            0.9830,
        ],
        "Recall": [
            0.9443,
            0.9713,
        ],
        "F1-Score": [
            0.8624,
            0.9771,
        ],
        "ROC-AUC": [
            0.7555,
            0.9930,
        ],
    }
)


# ---------------------------------------------------------
# Hyperparameter-tuning comparison
# Minority-class metrics refer to denied applications.
# ---------------------------------------------------------

TUNING_COMPARISON = pd.DataFrame(
    {
        "Model": [
            "Original Random Forest",
            "Tuned Random Forest",
        ],
        "Accuracy": [
            0.9678,
            0.9708,
        ],
        "Precision — Denied": [
            0.9325,
            0.9369,
        ],
        "Recall — Denied": [
            0.9593,
            0.9651,
        ],
        "F1 — Denied": [
            0.9457,
            0.9508,
        ],
        "ROC-AUC": [
            0.9930,
            0.9950,
        ],
    }
)


# ---------------------------------------------------------
# Feature importance
# ---------------------------------------------------------

FEATURE_IMPORTANCE = pd.DataFrame(
    {
        "Feature": [
            "Interest Rate",
            "Debt-to-Income Ratio",
            "Loan Amount",
            "Annual Income",
            "Loan-to-Value Ratio",
            "Property Value",
            "Loan Term",
            "Applicant Sex — Joint",
            "Applicant Race — White",
            "Applicant Race — Black or African American",
        ],
        "Importance": [
            0.594310,
            0.138525,
            0.066173,
            0.054109,
            0.043149,
            0.033540,
            0.014377,
            0.006831,
            0.006542,
            0.005751,
        ],
    }
)


def format_percentage(value: float) -> str:
    """
    Convert a decimal score into a percentage.
    """
    return f"{value * 100:.2f}%"


def style_metric_table(dataframe: pd.DataFrame) -> pd.io.formats.style.Styler:
    """
    Format evaluation scores as percentages.
    """

    percentage_columns = [
        column
        for column in dataframe.columns
        if column != "Model"
    ]

    return (
        dataframe.style
        .format(
            {
                column: "{:.2%}"
                for column in percentage_columns
            }
        )
        .highlight_max(
            subset=percentage_columns,
            axis=0,
        )
    )


def create_confusion_matrix_figure() -> go.Figure:
    """
    Create the final tuned-model confusion matrix.
    """

    figure = go.Figure(
        data=go.Heatmap(
            z=FINAL_CONFUSION_MATRIX,
            x=[
                "Predicted Denied",
                "Predicted Approved",
            ],
            y=[
                "Actual Denied",
                "Actual Approved",
            ],
            text=FINAL_CONFUSION_MATRIX,
            texttemplate="%{text:,}",
            textfont={
                "size": 18,
            },
            colorscale="Blues",
            showscale=True,
            hovertemplate=(
                "%{y}<br>"
                "%{x}<br>"
                "Applications: %{z:,}"
                "<extra></extra>"
            ),
        )
    )

    figure.update_layout(
        title={
            "text": (
                "Final Tuned Random Forest — "
                "Confusion Matrix"
            ),
            "x": 0.5,
            "xanchor": "center",
        },
        xaxis_title="Predicted Decision",
        yaxis_title="Actual Decision",
        height=520,
        margin={
            "l": 40,
            "r": 40,
            "t": 80,
            "b": 40,
        },
    )

    return figure


def create_roc_auc_comparison_figure() -> go.Figure:
    """
    Compare ROC-AUC across the evaluated models.
    """

    roc_data = pd.DataFrame(
        {
            "Model": [
                "Logistic Regression",
                "Original Random Forest",
                "Tuned Random Forest",
            ],
            "ROC-AUC": [
                0.7555,
                0.9930,
                0.9950,
            ],
        }
    )

    figure = px.bar(
        roc_data,
        x="Model",
        y="ROC-AUC",
        text="ROC-AUC",
        title="ROC-AUC Model Comparison",
    )

    figure.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "ROC-AUC: %{y:.4f}"
            "<extra></extra>"
        ),
    )

    figure.update_layout(
        yaxis={
            "range": [0.70, 1.01],
            "tickformat": ".0%",
            "title": "ROC-AUC",
        },
        xaxis_title="Model",
        height=500,
        showlegend=False,
        margin={
            "l": 40,
            "r": 40,
            "t": 80,
            "b": 40,
        },
    )

    return figure


def create_feature_importance_figure() -> go.Figure:
    """
    Display the ten most influential model features.
    """

    ordered_data = FEATURE_IMPORTANCE.sort_values(
        by="Importance",
        ascending=True,
    )

    figure = px.bar(
        ordered_data,
        x="Importance",
        y="Feature",
        orientation="h",
        text="Importance",
        title="Top 10 Predictive Features",
    )

    figure.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Importance: %{x:.4f}"
            "<extra></extra>"
        ),
    )

    figure.update_layout(
        xaxis_title="Feature Importance",
        yaxis_title="Feature",
        height=610,
        showlegend=False,
        margin={
            "l": 40,
            "r": 50,
            "t": 80,
            "b": 40,
        },
    )

    return figure


def show_model_performance() -> None:
    """
    Display the final mortgage-model evaluation dashboard.
    """

    back_column, title_column = st.columns(
        [1, 5],
        vertical_alignment="top",
    )

    with back_column:
        if st.button(
            "← Back",
            key="model_performance_back_button",
            width="stretch",
        ):
            set_page("home")

    with title_column:
        st.markdown(
            (
                "<p class='nova-kicker'>"
                "MODEL VALIDATION AND PERFORMANCE"
                "</p>"
            ),
            unsafe_allow_html=True,
        )

        st.title("Model Performance")

        st.write(
            "This dashboard summarizes the evaluation of the "
            "machine-learning models developed for mortgage approval "
            "prediction. All displayed values were produced using the "
            "held-out testing dataset from the final project notebook."
        )

    st.divider()

    # -----------------------------------------------------
    # Final model summary
    # -----------------------------------------------------

    st.subheader("Final Model Summary")

    st.success(
        "The tuned Random Forest was selected as the final deployment "
        "model because it achieved the strongest overall performance "
        "and improved the identification of denied applications."
    )

    summary_left, summary_middle, summary_right = st.columns(
        3,
        gap="large",
    )

    with summary_left:
        st.metric(
            label="Selected Model",
            value="Tuned Random Forest",
            help=(
                "The model selected after comparative evaluation "
                "and hyperparameter optimization."
            ),
        )

    with summary_middle:
        st.metric(
            label="Testing Observations",
            value="10,000",
            help=(
                "Number of mortgage applications in the held-out "
                "testing dataset."
            ),
        )

    with summary_right:
        st.metric(
            label="Cross-Validation Accuracy",
            value=format_percentage(
                FINAL_MODEL_METRICS["cv_mean_accuracy"]
            ),
            help=(
                "Mean accuracy obtained across the cross-validation "
                "folds."
            ),
        )

    st.divider()

    # -----------------------------------------------------
    # Final metrics
    # -----------------------------------------------------

    st.subheader("Final Tuned Random Forest Metrics")

    st.caption(
        "Precision, Recall and F1 below focus on denied applications, "
        "the minority class and the more challenging outcome to detect."
    )

    (
        accuracy_column,
        precision_column,
        recall_column,
        f1_column,
        auc_column,
    ) = st.columns(
        5,
        gap="small",
    )

    with accuracy_column:
        st.metric(
            label="Accuracy",
            value=format_percentage(
                FINAL_MODEL_METRICS["accuracy"]
            ),
            help=(
                "Percentage of all testing applications classified "
                "correctly."
            ),
        )

    with precision_column:
        st.metric(
            label="Precision — Denied",
            value=format_percentage(
                FINAL_MODEL_METRICS["denied_precision"]
            ),
            help=(
                "Among applications predicted as denied, the share "
                "that were actually denied."
            ),
        )

    with recall_column:
        st.metric(
            label="Recall — Denied",
            value=format_percentage(
                FINAL_MODEL_METRICS["denied_recall"]
            ),
            help=(
                "Among applications actually denied, the share "
                "correctly identified by the model."
            ),
        )

    with f1_column:
        st.metric(
            label="F1 — Denied",
            value=format_percentage(
                FINAL_MODEL_METRICS["denied_f1"]
            ),
            help=(
                "Harmonic balance between denied-class Precision "
                "and Recall."
            ),
        )

    with auc_column:
        st.metric(
            label="ROC-AUC",
            value=f"{FINAL_MODEL_METRICS['roc_auc']:.3f}",
            help=(
                "Overall ability to distinguish approved from "
                "denied applications across decision thresholds."
            ),
        )

    st.info(
        "The final model achieved 97.08% testing accuracy and a "
        "ROC-AUC of 0.995. It correctly identified 96.51% of the "
        "applications that were actually denied."
    )

    st.divider()

    # -----------------------------------------------------
    # Baseline model comparison
    # -----------------------------------------------------

    st.subheader("Baseline Model Comparison")

    st.write(
        "Logistic Regression was used as the baseline classifier. "
        "The original Random Forest demonstrated a substantial "
        "improvement across all primary evaluation measures."
    )

    st.dataframe(
        style_metric_table(BASELINE_COMPARISON),
        width="stretch",
        hide_index=True,
    )

    st.plotly_chart(
        create_roc_auc_comparison_figure(),
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )

    st.divider()

    # -----------------------------------------------------
    # Hyperparameter tuning
    # -----------------------------------------------------

    st.subheader("Hyperparameter-Tuning Evaluation")

    st.write(
        "RandomizedSearchCV was used to optimize the Random Forest. "
        "The tuned model improved Accuracy, minority-class Precision, "
        "minority-class Recall, minority-class F1 and ROC-AUC."
    )

    st.dataframe(
        style_metric_table(TUNING_COMPARISON),
        width="stretch",
        hide_index=True,
    )

    with st.expander(
        "View Selected Hyperparameters"
    ):
        parameter_data = pd.DataFrame(
            {
                "Hyperparameter": [
                    "Number of Trees",
                    "Maximum Depth",
                    "Minimum Samples Split",
                    "Minimum Samples Leaf",
                    "Maximum Features",
                    "Class Weight",
                ],
                "Selected Value": [
                    "300",
                    "20",
                    "10",
                    "1",
                    "All Features",
                    "None",
                ],
            }
        )

        st.dataframe(
            parameter_data,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            "The best cross-validation F1-macro score during "
            "RandomizedSearchCV was 0.9666."
        )

    st.divider()

    # -----------------------------------------------------
    # Confusion matrix
    # -----------------------------------------------------

    st.subheader("Confusion Matrix")

    matrix_column, interpretation_column = st.columns(
        [1.7, 1],
        gap="large",
        vertical_alignment="center",
    )

    with matrix_column:
        st.plotly_chart(
            create_confusion_matrix_figure(),
            width="stretch",
            config={
                "displayModeBar": False,
            },
        )

    with interpretation_column:
        st.markdown("#### Testing Outcomes")

        st.metric(
            label="Correctly Identified Denials",
            value="2,822",
        )

        st.metric(
            label="Correctly Identified Approvals",
            value="6,886",
        )

        st.metric(
            label="Denied but Predicted Approved",
            value="102",
        )

        st.metric(
            label="Approved but Predicted Denied",
            value="190",
        )

        st.write(
            "The model correctly classified 9,708 of the 10,000 "
            "testing applications."
        )

    st.divider()

    # -----------------------------------------------------
    # Precision-recall and validation
    # -----------------------------------------------------

    st.subheader("Additional Validation Evidence")

    validation_left, validation_center, validation_right = st.columns(
        3,
        gap="large",
    )

    with validation_left:
        st.metric(
            label="Average Precision",
            value=(
                f"{FINAL_MODEL_METRICS['average_precision']:.4f}"
            ),
            help=(
                "Summary of the Precision–Recall relationship "
                "across decision thresholds."
            ),
        )

    with validation_center:
        st.metric(
            label="Mean CV Accuracy",
            value=format_percentage(
                FINAL_MODEL_METRICS["cv_mean_accuracy"]
            ),
            help=(
                "Average accuracy across the cross-validation folds."
            ),
        )

    with validation_right:
        st.metric(
            label="CV Standard Deviation",
            value=(
                f"{FINAL_MODEL_METRICS['cv_standard_deviation']:.5f}"
            ),
            help=(
                "Low variation indicates stable performance across "
                "the validation folds."
            ),
        )

    st.write(
        "The high Average Precision score and the very small "
        "cross-validation standard deviation provide additional "
        "evidence that the selected model is both accurate and stable."
    )

    st.divider()

    # -----------------------------------------------------
    # Feature importance
    # -----------------------------------------------------

    st.subheader("Feature Importance")

    st.write(
        "Feature importance describes the contribution of each "
        "input variable to the Random Forest predictions. It reflects "
        "predictive influence and should not be interpreted as proof "
        "of causality."
    )

    st.plotly_chart(
        create_feature_importance_figure(),
        width="stretch",
        config={
            "displayModeBar": False,
        },
    )

    st.info(
        "Interest rate was the strongest predictive feature, followed "
        "by debt-to-income ratio, loan amount, annual income and "
        "loan-to-value ratio. Financial variables contributed much "
        "more strongly than demographic variables."
    )

    st.divider()

    # -----------------------------------------------------
    # Academic interpretation
    # -----------------------------------------------------

    st.subheader("Academic Interpretation")

    st.markdown(
        """
        The evaluation demonstrates that the tuned Random Forest
        provides strong discrimination between approved and denied
        mortgage applications.

        Its high ROC-AUC indicates excellent ranking capability,
        while the denied-class Recall confirms that the model detects
        most applications that were actually denied. The confusion
        matrix further shows that errors represent a relatively small
        proportion of the held-out testing sample.

        These results support the use of the tuned Random Forest as
        the final predictive component of the NOVA mortgage analytics
        platform.
        """
    )

    st.caption(
        "Performance statistics were calculated on a held-out testing "
        "dataset. The application is an academic analytical tool and "
        "does not replace official lender underwriting."
    )