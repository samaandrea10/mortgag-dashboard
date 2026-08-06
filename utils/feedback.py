from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from tempfile import NamedTemporaryFile
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


BOOLEAN_COLUMNS = [
    "verified_outcome",
    "prediction_correct",
]


INTEGER_COLUMNS = [
    "actual_target",
    "predicted_target",
    "raw_model_prediction",
    "loan_term_months",
]


NUMERIC_COLUMNS = [
    "approval_probability",
    "decline_probability",
    "financial_risk_penalty",
    "loan_amount",
    "annual_income",
    "property_value",
    "interest_rate",
    "loan_to_value_ratio",
    "debt_to_income_ratio",
    "monthly_payment",
    "payment_to_income_ratio",
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

    try:
        if pd.isna(value):
            return default
    except (TypeError, ValueError):
        pass

    return value


def _normalize_outcome(outcome: str) -> str:
    """
    Normalize and validate a mortgage outcome label.

    Allowed values:
    - Approved
    - Denied
    """
    if not isinstance(outcome, str):
        raise TypeError(
            "Actual outcome must be provided as text."
        )

    normalized_outcome = outcome.strip().lower()

    outcome_mapping = {
        "approved": "Approved",
        "denied": "Denied",
    }

    if normalized_outcome not in outcome_mapping:
        raise ValueError(
            "Actual outcome must be either Approved or Denied."
        )

    return outcome_mapping[normalized_outcome]


def _outcome_to_target(outcome: str) -> int:
    """
    Convert a normalized outcome label into the model target format.

    Approved = 1
    Denied = 0
    """
    normalized_outcome = _normalize_outcome(outcome)

    return 1 if normalized_outcome == "Approved" else 0


def _target_to_outcome(target: int) -> str:
    """
    Convert a binary target into a readable outcome label.
    """
    if target == 1:
        return "Approved"

    if target == 0:
        return "Denied"

    raise ValueError(
        "Predicted target must be either 0 or 1."
    )


def _normalize_boolean_series(
    series: pd.Series,
) -> pd.Series:
    """
    Convert common textual and numeric boolean representations
    into pandas nullable boolean values.
    """
    normalized = (
        series.astype(str)
        .str.strip()
        .str.lower()
    )

    mapping = {
        "true": True,
        "1": True,
        "yes": True,
        "false": False,
        "0": False,
        "no": False,
    }

    return normalized.map(mapping).astype("boolean")


def _prepare_feedback_dataframe(
    feedback_data: pd.DataFrame,
) -> pd.DataFrame:
    """
    Normalize column order and data types in a feedback dataset.
    """
    prepared_data = feedback_data.reindex(
        columns=FEEDBACK_COLUMNS
    ).copy()

    if "feedback_timestamp_utc" in prepared_data.columns:
        prepared_data["feedback_timestamp_utc"] = (
            pd.to_datetime(
                prepared_data["feedback_timestamp_utc"],
                errors="coerce",
                utc=True,
            )
        )

    for column in BOOLEAN_COLUMNS:
        if column in prepared_data.columns:
            prepared_data[column] = _normalize_boolean_series(
                prepared_data[column]
            )

    for column in INTEGER_COLUMNS:
        if column in prepared_data.columns:
            prepared_data[column] = pd.to_numeric(
                prepared_data[column],
                errors="coerce",
            ).astype("Int64")

    for column in NUMERIC_COLUMNS:
        if column in prepared_data.columns:
            prepared_data[column] = pd.to_numeric(
                prepared_data[column],
                errors="coerce",
            )

    for column in [
        "actual_outcome",
        "predicted_outcome",
        "risk_level",
        "confidence",
        "applicant_age",
        "derived_race",
        "derived_sex",
        "derived_ethnicity",
        "reviewer_note",
    ]:
        if column in prepared_data.columns:
            prepared_data[column] = (
                prepared_data[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

    return prepared_data


def build_feedback_record(
    analysis_result: dict[str, Any],
    actual_outcome: str,
    reviewer_note: str = "",
    verified_outcome: bool = True,
) -> dict[str, Any]:
    """
    Build a validated and normalized feedback observation
    from a mortgage prediction result.
    """
    if not isinstance(analysis_result, dict):
        raise TypeError(
            "Analysis result must be provided as a dictionary."
        )

    normalized_actual_outcome = _normalize_outcome(
        actual_outcome
    )

    actual_target = _outcome_to_target(
        normalized_actual_outcome
    )

    raw_prediction = analysis_result.get(
        "prediction",
        analysis_result.get(
            "raw_model_prediction"
        ),
    )

    if raw_prediction is None:
        raise ValueError(
            "The analysis result does not contain a model prediction."
        )

    try:
        predicted_target = int(raw_prediction)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "The model prediction could not be converted to a binary target."
        ) from error

    if predicted_target not in {0, 1}:
        raise ValueError(
            "The model prediction must be either 0 or 1."
        )

    predicted_outcome = _target_to_outcome(
        predicted_target
    )

    prediction_correct = (
        predicted_target == actual_target
    )

    feedback_record = {
        "feedback_timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "verified_outcome": bool(verified_outcome),
        "actual_outcome": normalized_actual_outcome,
        "actual_target": actual_target,
        "predicted_outcome": predicted_outcome,
        "predicted_target": predicted_target,
        "raw_model_prediction": _safe_value(
            analysis_result.get(
                "raw_model_prediction",
                predicted_target,
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
            analysis_result.get(
                "risk_level"
            )
        ),
        "confidence": _safe_value(
            analysis_result.get(
                "confidence"
            )
        ),
        "financial_risk_penalty": _safe_value(
            analysis_result.get(
                "financial_risk_penalty"
            )
        ),
        "loan_amount": _safe_value(
            analysis_result.get(
                "loan_amount"
            )
        ),
        "annual_income": _safe_value(
            analysis_result.get(
                "annual_income"
            )
        ),
        "property_value": _safe_value(
            analysis_result.get(
                "property_value"
            )
        ),
        "interest_rate": _safe_value(
            analysis_result.get(
                "interest_rate"
            )
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
            analysis_result.get(
                "monthly_payment"
            )
        ),
        "payment_to_income_ratio": _safe_value(
            analysis_result.get(
                "payment_to_income_ratio"
            )
        ),
        "applicant_age": _safe_value(
            analysis_result.get(
                "applicant_age"
            )
        ),
        "derived_race": _safe_value(
            analysis_result.get(
                "derived_race"
            )
        ),
        "derived_sex": _safe_value(
            analysis_result.get(
                "derived_sex"
            )
        ),
        "derived_ethnicity": _safe_value(
            analysis_result.get(
                "derived_ethnicity"
            )
        ),
        "reviewer_note": str(
            reviewer_note or ""
        ).strip(),
    }

    return {
        column: feedback_record.get(
            column,
            "",
        )
        for column in FEEDBACK_COLUMNS
    }


def load_feedback_data() -> pd.DataFrame:
    """
    Load and normalize all locally stored feedback observations.
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
        UnicodeDecodeError,
    ):
        return pd.DataFrame(
            columns=FEEDBACK_COLUMNS
        )

    return _prepare_feedback_dataframe(
        feedback_data
    )


def _write_feedback_data_atomically(
    feedback_data: pd.DataFrame,
) -> None:
    """
    Write the feedback dataset safely using an atomic file replacement.
    """
    FEEDBACK_FILE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    export_data = feedback_data.copy()

    if "feedback_timestamp_utc" in export_data.columns:
        export_data["feedback_timestamp_utc"] = (
            export_data["feedback_timestamp_utc"]
            .astype(str)
            .replace(
                {
                    "NaT": "",
                    "<NA>": "",
                }
            )
        )

    for column in BOOLEAN_COLUMNS:
        if column in export_data.columns:
            export_data[column] = (
                export_data[column]
                .astype("boolean")
                .astype(str)
                .replace(
                    {
                        "<NA>": "",
                    }
                )
            )

    temporary_path: Path | None = None

    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="",
            delete=False,
            dir=FEEDBACK_FILE_PATH.parent,
            suffix=".tmp",
        ) as temporary_file:
            temporary_path = Path(
                temporary_file.name
            )

            export_data.to_csv(
                temporary_file,
                index=False,
            )

        temporary_path.replace(
            FEEDBACK_FILE_PATH
        )

    except Exception:
        if (
            temporary_path is not None
            and temporary_path.exists()
        ):
            temporary_path.unlink()

        raise


def save_feedback_record(
    feedback_record: dict[str, Any],
) -> None:
    """
    Append one validated feedback observation to the CSV file.
    """
    if not isinstance(feedback_record, dict):
        raise TypeError(
            "Feedback record must be provided as a dictionary."
        )

    normalized_record = {
        column: feedback_record.get(
            column,
            "",
        )
        for column in FEEDBACK_COLUMNS
    }

    existing_feedback = load_feedback_data()

    new_feedback = _prepare_feedback_dataframe(
        pd.DataFrame(
            [normalized_record],
            columns=FEEDBACK_COLUMNS,
        )
    )

    updated_feedback = pd.concat(
        [
            existing_feedback,
            new_feedback,
        ],
        ignore_index=True,
    )

    updated_feedback = _prepare_feedback_dataframe(
        updated_feedback
    )

    _write_feedback_data_atomically(
        updated_feedback
    )


def get_feedback_summary() -> dict[str, Any]:
    """
    Calculate monitoring statistics from verified feedback records.
    """
    feedback_data = load_feedback_data()

    total_feedback = len(
        feedback_data
    )

    empty_summary = {
        "total_feedback": total_feedback,
        "verified_feedback": 0,
        "correct_predictions": 0,
        "incorrect_predictions": 0,
        "feedback_accuracy": None,
        "actual_approved": 0,
        "actual_denied": 0,
    }

    if total_feedback == 0:
        return empty_summary

    verified_mask = (
        feedback_data["verified_outcome"]
        .fillna(False)
        .astype(bool)
    )

    verified_feedback = feedback_data.loc[
        verified_mask
    ].copy()

    verified_count = len(
        verified_feedback
    )

    if verified_count == 0:
        return empty_summary

    correctness = (
        verified_feedback[
            "prediction_correct"
        ]
        .fillna(False)
        .astype(bool)
    )

    correct_predictions = int(
        correctness.sum()
    )

    incorrect_predictions = int(
        verified_count
        - correct_predictions
    )

    feedback_accuracy = (
        correct_predictions
        / verified_count
    )

    actual_outcomes = (
        verified_feedback[
            "actual_outcome"
        ]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    actual_approved = int(
        (
            actual_outcomes
            == "approved"
        ).sum()
    )

    actual_denied = int(
        (
            actual_outcomes
            == "denied"
        ).sum()
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
    Return the normalized feedback dataset as UTF-8 CSV bytes.
    """
    feedback_data = load_feedback_data()

    export_data = feedback_data.copy()

    if "feedback_timestamp_utc" in export_data.columns:
        export_data["feedback_timestamp_utc"] = (
            export_data["feedback_timestamp_utc"]
            .astype(str)
            .replace(
                {
                    "NaT": "",
                    "<NA>": "",
                }
            )
        )

    return export_data.to_csv(
        index=False,
    ).encode(
        "utf-8-sig"
    )