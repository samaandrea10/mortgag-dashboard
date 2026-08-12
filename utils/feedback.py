from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
FEEDBACK_PATH = BASE_DIR / "feedback_data.csv"


FEEDBACK_COLUMNS = [
    "feedback_timestamp_utc",
    "verified_outcome",
    "predicted_outcome",
    "predicted_target",
    "actual_outcome",
    "actual_target",
    "prediction_correct",
    "approval_probability",
    "decline_probability",
    "risk_level",
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


def _safe_value(value: Any, default: Any = "") -> Any:
    if value is None:
        return default

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    return value


def build_feedback_record(
    analysis_result: dict[str, Any],
    actual_outcome: str,
    reviewer_note: str = "",
    verified_outcome: bool = True,
) -> dict[str, Any]:
    """
    Build one verified feedback record from the current prediction.
    """

    if not isinstance(analysis_result, dict):
        raise TypeError("analysis_result must be a dictionary.")

    actual_outcome = str(actual_outcome).strip()

    if actual_outcome not in {"Approved", "Denied"}:
        raise ValueError(
            "actual_outcome must be 'Approved' or 'Denied'."
        )

    actual_target = 1 if actual_outcome == "Approved" else 0

    predicted_target = int(
        analysis_result.get("prediction", 0)
    )

    predicted_target = 1 if predicted_target == 1 else 0

    predicted_outcome = (
        "Approved"
        if predicted_target == 1
        else "Denied"
    )

    approval_probability = analysis_result.get(
        "approval_probability"
    )

    decline_probability = analysis_result.get(
        "decline_probability"
    )

    if approval_probability is not None:
        approval_probability = float(approval_probability)

    if decline_probability is not None:
        decline_probability = float(decline_probability)

    if (
        approval_probability is not None
        and decline_probability is None
    ):
        decline_probability = 1.0 - approval_probability

    if (
        decline_probability is not None
        and approval_probability is None
    ):
        approval_probability = 1.0 - decline_probability

    return {
        "feedback_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),

        "verified_outcome": bool(verified_outcome),

        "predicted_outcome": predicted_outcome,
        "predicted_target": predicted_target,

        "actual_outcome": actual_outcome,
        "actual_target": actual_target,

        "prediction_correct": (
            predicted_target == actual_target
        ),

        "approval_probability": _safe_value(
            approval_probability
        ),

        "decline_probability": _safe_value(
            decline_probability
        ),

        "risk_level": _safe_value(
            analysis_result.get("risk_level")
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
            analysis_result.get("loan_term_months")
        ),

        "loan_to_value_ratio": _safe_value(
            analysis_result.get("loan_to_value_ratio")
        ),

        "debt_to_income_ratio": _safe_value(
            analysis_result.get("debt_to_income_ratio")
        ),

        "monthly_payment": _safe_value(
            analysis_result.get("monthly_payment")
        ),

        "payment_to_income_ratio": _safe_value(
            analysis_result.get("payment_to_income_ratio")
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
            analysis_result.get("derived_ethnicity")
        ),

        "reviewer_note": str(
            reviewer_note or ""
        ).strip(),
    }


def load_feedback_data() -> pd.DataFrame:
    """
    Load the locally stored feedback dataset.
    """

    if not FEEDBACK_PATH.exists():
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)

    try:
        data = pd.read_csv(FEEDBACK_PATH)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=FEEDBACK_COLUMNS)

    for column in FEEDBACK_COLUMNS:
        if column not in data.columns:
            data[column] = ""

    return data[FEEDBACK_COLUMNS]


def save_feedback_record(
    feedback_record: dict[str, Any],
) -> None:
    """
    Append one feedback record to feedback_data.csv.
    """

    existing_data = load_feedback_data()

    new_row = pd.DataFrame(
        [
            {
                column: _safe_value(
                    feedback_record.get(column, "")
                )
                for column in FEEDBACK_COLUMNS
            }
        ]
    )

    updated_data = pd.concat(
        [
            existing_data,
            new_row,
        ],
        ignore_index=True,
    )

    updated_data.to_csv(
        FEEDBACK_PATH,
        index=False,
        encoding="utf-8",
    )


def get_feedback_summary() -> dict[str, Any]:
    """
    Return monitoring statistics for stored feedback.
    """

    data = load_feedback_data()

    if data.empty:
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
        data["verified_outcome"]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    verified_data = data.loc[verified_mask].copy()

    total_feedback = len(data)
    verified_feedback = len(verified_data)

    if verified_feedback == 0:
        return {
            "total_feedback": total_feedback,
            "verified_feedback": 0,
            "correct_predictions": 0,
            "incorrect_predictions": 0,
            "feedback_accuracy": None,
            "actual_approved": 0,
            "actual_denied": 0,
        }

    correct_mask = (
        verified_data["prediction_correct"]
        .astype(str)
        .str.lower()
        .isin(["true", "1", "yes"])
    )

    correct_predictions = int(correct_mask.sum())

    incorrect_predictions = (
        verified_feedback - correct_predictions
    )

    feedback_accuracy = (
        correct_predictions / verified_feedback
    )

    actual_outcome = (
        verified_data["actual_outcome"]
        .astype(str)
        .str.strip()
    )

    actual_approved = int(
        (actual_outcome == "Approved").sum()
    )

    actual_denied = int(
        (actual_outcome == "Denied").sum()
    )

    return {
        "total_feedback": total_feedback,
        "verified_feedback": verified_feedback,
        "correct_predictions": correct_predictions,
        "incorrect_predictions": incorrect_predictions,
        "feedback_accuracy": feedback_accuracy,
        "actual_approved": actual_approved,
        "actual_denied": actual_denied,
    }


def feedback_to_csv_bytes() -> bytes:
    """
    Convert the feedback dataset to downloadable CSV bytes.
    """

    data = load_feedback_data()

    return data.to_csv(
        index=False
    ).encode("utf-8-sig")