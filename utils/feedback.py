from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_FILE_PATH = BASE_DIR / "feedback_data.csv"


FEEDBACK_COLUMNS = [
    "feedback_timestamp_utc",
    "verified_outcome",
    "actual_outcome",
    "actual_target",
    "predicted_outcome",
    "predicted_target",
    "raw_model_prediction",
    "prediction_correct",
    "approval_probability",
    "decline_probability",
    "risk_level",
    "confidence",
    "financial_risk_penalty",
    "loan_amount",
    "annual_income",
    "property_value",
    "interest_rate",
    "loan_term_months",
    "loan_to_value_ratio",
    "debt_to_income_ratio",
    "monthly_payment",
    "payment_to_income_ratio",
    "applicant_age",
    "derived_race",
    "derived_sex",
    "derived_ethnicity",
    "reviewer_note",
]


def _safe_value(
    value: Any,
    default: Any = "",
) -> Any:
    """
    Replace missing values with a CSV-safe default.
    """

    if value is None:
        return default

    return value


def _outcome_to_target(outcome: str) -> int:
    """
    Convert an outcome label into the model target format.

    Approved = 1
    Denied = 0
    """

    normalized_outcome = outcome.strip().lower()

    if normalized_outcome == "approved":
        return 1

    if normalized_outcome == "denied":
        return 0

    raise ValueError(
        "Actual outcome must be either Approved or Denied."
    )


def build_feedback_record(
    analysis_result: dict[str, Any],
    actual_outcome: str,
    reviewer_note: str = "",
    verified_outcome: bool = True,
) -> dict[str, Any]:
    """
    Build a structured feedback observation from a prediction result.
    """

    actual_target = _outcome_to_target(actual_outcome)

    predicted_target = int(
        analysis_result.get(
            "prediction",
            analysis_result.get("raw_model_prediction", 0),
        )
    )

    prediction_correct = (
        predicted_target == actual_target
    )

    predicted_outcome = (
        "Approved"
        if predicted_target == 1
        else "Denied"
    )

    feedback_record = {
        "feedback_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "verified_outcome": bool(verified_outcome),
        "actual_outcome": actual_outcome,
        "actual_target": actual_target,
        "predicted_outcome": predicted_outcome,
        "predicted_target": predicted_target,
        "raw_model_prediction": _safe_value(
            analysis_result.get(
                "raw_model_prediction"
            )
        ),
        "prediction_correct": prediction_correct,
        "approval_probability": _safe_value(
            analysis_result.get(
                "approval_probability"
            )
        ),
        "decline_probability": _safe_value(
            analysis_result.get(
                "decline_probability"
            )
        ),
        "risk_level": _safe_value(
            analysis_result.get("risk_level")
        ),
        "confidence": _safe_value(
            analysis_result.get("confidence")
        ),
        "financial_risk_penalty": _safe_value(
            analysis_result.get(
                "financial_risk_penalty"
            )
        ),
        "loan_amount": _safe_value(
            analysis_result.get("loan_amount")
        ),
        "annual_income": _safe_value(
            analysis_result.get("annual_income")
        ),
        "property_value": _safe_value(
            analysis_result.get("property_value")
        ),
        "interest_rate": _safe_value(
            analysis_result.get("interest_rate")
        ),
        "loan_term_months": _safe_value(
            analysis_result.get(
                "loan_term_months"
            )
        ),
        "loan_to_value_ratio": _safe_value(
            analysis_result.get(
                "loan_to_value_ratio"
            )
        ),
        "debt_to_income_ratio": _safe_value(
            analysis_result.get(
                "debt_to_income_ratio"
            )
        ),
        "monthly_payment": _safe_value(
            analysis_result.get("monthly_payment")
        ),
        "payment_to_income_ratio": _safe_value(
            analysis_result.get(
                "payment_to_income_ratio"
            )
        ),
        "applicant_age": _safe_value(
            analysis_result.get("applicant_age")
        ),
        "derived_race": _safe_value(
            analysis_result.get("derived_race")
        ),
        "derived_sex": _safe_value(
            analysis_result.get("derived_sex")
        ),
        "derived_ethnicity": _safe_value(
            analysis_result.get(
                "derived_ethnicity"
            )
        ),
        "reviewer_note": reviewer_note.strip(),
    }

    return feedback_record


def load_feedback_data() -> pd.DataFrame:
    """
    Load all locally stored feedback observations.
    """

    if not FEEDBACK_FILE_PATH.exists():
        return pd.DataFrame(
            columns=FEEDBACK_COLUMNS
        )

    try:
        feedback_data = pd.read_csv(
            FEEDBACK_FILE_PATH
        )
    except (
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
    ):
        return pd.DataFrame(
            columns=FEEDBACK_COLUMNS
        )

    return feedback_data.reindex(
        columns=FEEDBACK_COLUMNS
    )


def save_feedback_record(
    feedback_record: dict[str, Any],
) -> None:
    """
    Append one verified feedback observation to the CSV file.
    """

    existing_feedback = load_feedback_data()

    new_feedback = pd.DataFrame(
        [feedback_record],
        columns=FEEDBACK_COLUMNS,
    )

    updated_feedback = pd.concat(
        [
            existing_feedback,
            new_feedback,
        ],
        ignore_index=True,
    )

    updated_feedback.to_csv(
        FEEDBACK_FILE_PATH,
        index=False,
    )


def get_feedback_summary() -> dict[str, Any]:
    """
    Calculate monitoring statistics from stored feedback.
    """

    feedback_data = load_feedback_data()

    total_feedback = len(feedback_data)

    if total_feedback == 0:
        return {
            "total_feedback": 0,
            "verified_feedback": 0,
            "correct_predictions": 0,
            "incorrect_predictions": 0,
            "feedback_accuracy": None,
            "actual_approved": 0,
            "actual_denied": 0,
        }

    verified_mask = (
        feedback_data["verified_outcome"]
        .astype(str)
        .str.lower()
        .isin(["true", "1"])
    )

    verified_feedback = feedback_data.loc[
        verified_mask
    ].copy()

    verified_count = len(verified_feedback)

    if verified_count == 0:
        feedback_accuracy = None
        correct_predictions = 0
        incorrect_predictions = 0
    else:
        correctness = (
            verified_feedback[
                "prediction_correct"
            ]
            .astype(str)
            .str.lower()
            .isin(["true", "1"])
        )

        correct_predictions = int(
            correctness.sum()
        )

        incorrect_predictions = (
            verified_count - correct_predictions
        )

        feedback_accuracy = (
            correct_predictions
            / verified_count
        )

    actual_outcomes = (
        verified_feedback["actual_outcome"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    actual_approved = int(
        (actual_outcomes == "approved").sum()
    )

    actual_denied = int(
        (actual_outcomes == "denied").sum()
    )

    return {
        "total_feedback": total_feedback,
        "verified_feedback": verified_count,
        "correct_predictions": correct_predictions,
        "incorrect_predictions": incorrect_predictions,
        "feedback_accuracy": feedback_accuracy,
        "actual_approved": actual_approved,
        "actual_denied": actual_denied,
    }


def feedback_to_csv_bytes() -> bytes:
    """
    Return the feedback dataset as downloadable CSV bytes.
    """

    feedback_data = load_feedback_data()

    return feedback_data.to_csv(
        index=False
    ).encode("utf-8")