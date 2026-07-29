from pathlib import Path
from typing import Any

import joblib
import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "mortgage_pipeline.pkl"
COLUMNS_PATH = BASE_DIR / "model_columns.pkl"


# ---------------------------------------------------------
# Load model
# ---------------------------------------------------------

@st.cache_resource
def load_model() -> tuple[Any, list[str]]:
    """
    Load the trained mortgage pipeline and the saved feature columns.
    """

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file was not found: {MODEL_PATH}"
        )

    model = joblib.load(MODEL_PATH)

    if COLUMNS_PATH.exists():
        saved_columns = list(
            joblib.load(COLUMNS_PATH)
        )
    else:
        saved_columns = list(
            getattr(model, "feature_names_in_", [])
        )

    return model, saved_columns


# ---------------------------------------------------------
# Expected model columns
# ---------------------------------------------------------

def get_expected_columns(
    model: Any,
    saved_columns: list[str],
) -> list[str]:
    """
    Return the exact feature names expected by the model.
    """

    model_feature_names = getattr(
        model,
        "feature_names_in_",
        None,
    )

    if model_feature_names is not None:
        return list(model_feature_names)

    if hasattr(model, "named_steps"):
        for step in reversed(
            list(model.named_steps.values())
        ):
            step_feature_names = getattr(
                step,
                "feature_names_in_",
                None,
            )

            if step_feature_names is not None:
                return list(step_feature_names)

    return list(saved_columns)


# ---------------------------------------------------------
# Input preparation
# ---------------------------------------------------------

def prepare_input(
    loan_amount: float,
    income: float,
    interest_rate: float,
    loan_to_value_ratio: float,
    debt_to_income_ratio: float,
    property_value: float,
    loan_term: int,
    applicant_age: str,
    derived_race: str,
    derived_sex: str,
    derived_ethnicity: str,
    model: Any,
    saved_columns: list[str],
) -> pd.DataFrame:
    """
    Convert user input into the structure expected by the model.

    Supports:
    1. A Pipeline trained on raw columns.
    2. A model trained on one-hot encoded columns.
    """

    raw_values = {
        "loan_amount": float(loan_amount),
        "income": float(income),
        "interest_rate": float(interest_rate),
        "loan_to_value_ratio": float(
            loan_to_value_ratio
        ),
        "debt_to_income_ratio": float(
            debt_to_income_ratio
        ),
        "property_value": float(property_value),
        "loan_term": int(loan_term),
        "applicant_age": str(applicant_age),
        "derived_race": str(derived_race),
        "derived_sex": str(derived_sex),
        "derived_ethnicity": str(
            derived_ethnicity
        ),
    }

    expected_columns = get_expected_columns(
        model=model,
        saved_columns=saved_columns,
    )

    categorical_columns = [
        "applicant_age",
        "derived_race",
        "derived_sex",
        "derived_ethnicity",
    ]

    expects_raw_categories = all(
        column in expected_columns
        for column in categorical_columns
    )

    # Pipeline trained on original columns
    if expects_raw_categories:
        raw_dataframe = pd.DataFrame(
            [raw_values]
        )

        return raw_dataframe.reindex(
            columns=expected_columns
        )

    # Model trained on one-hot encoded columns
    prepared_row = {
        column: 0
        for column in expected_columns
    }

    numerical_values = {
        "loan_amount": float(loan_amount),
        "income": float(income),
        "interest_rate": float(interest_rate),
        "loan_to_value_ratio": float(
            loan_to_value_ratio
        ),
        "debt_to_income_ratio": float(
            debt_to_income_ratio
        ),
        "property_value": float(property_value),
        "loan_term": int(loan_term),
    }

    for column_name, value in numerical_values.items():
        if column_name in prepared_row:
            prepared_row[column_name] = value

    categorical_values = {
        "applicant_age": str(applicant_age),
        "derived_race": str(derived_race),
        "derived_sex": str(derived_sex),
        "derived_ethnicity": str(
            derived_ethnicity
        ),
    }

    for feature_name, selected_value in categorical_values.items():
        dummy_column = (
            f"{feature_name}_{selected_value}"
        )

        if dummy_column in prepared_row:
            prepared_row[dummy_column] = 1

    return pd.DataFrame(
        [prepared_row],
        columns=expected_columns,
    )


# ---------------------------------------------------------
# Financial calculations
# ---------------------------------------------------------

def calculate_monthly_payment(
    principal: float,
    annual_interest_rate: float,
    loan_term_months: int,
) -> float:
    """
    Calculate the estimated monthly mortgage payment.
    """

    if principal <= 0 or loan_term_months <= 0:
        return 0.0

    monthly_rate = (
        annual_interest_rate / 100 / 12
    )

    if monthly_rate == 0:
        return principal / loan_term_months

    growth_factor = (
        1 + monthly_rate
    ) ** loan_term_months

    return principal * (
        monthly_rate * growth_factor
    ) / (
        growth_factor - 1
    )


def calculate_confidence(
    approval_probability: float,
    decline_probability: float,
) -> str:
    """
    Return the confidence level of the final result.
    """

    highest_probability = max(
        approval_probability,
        decline_probability,
    )

    if highest_probability >= 0.85:
        return "High"

    if highest_probability >= 0.70:
        return "Moderate"

    return "Low"


def calculate_risk_level(
    decline_probability: float,
) -> str:
    """
    Convert decline probability into a readable risk level.
    """

    if decline_probability < 0.25:
        return "Low"

    if decline_probability < 0.50:
        return "Moderate"

    if decline_probability < 0.75:
        return "High"

    return "Very High"


def calculate_financial_risk_penalty(
    payment_to_income_ratio: float,
    debt_to_income_ratio: float,
    loan_to_value_ratio: float,
    interest_rate: float,
) -> float:
    """
    Calculate a financial-risk penalty.

    The penalty supplements the machine-learning model when the
    applicant presents severe affordability or equity concerns.
    """

    penalty = 0.0

    # Mortgage payment burden
    if payment_to_income_ratio > 100:
        penalty += 0.45
    elif payment_to_income_ratio > 50:
        penalty += 0.35
    elif payment_to_income_ratio > 40:
        penalty += 0.20
    elif payment_to_income_ratio > 30:
        penalty += 0.10

    # Debt burden
    if debt_to_income_ratio > 60:
        penalty += 0.25
    elif debt_to_income_ratio > 50:
        penalty += 0.20
    elif debt_to_income_ratio > 43:
        penalty += 0.10

    # Borrower equity
    if loan_to_value_ratio > 98:
        penalty += 0.20
    elif loan_to_value_ratio > 95:
        penalty += 0.15
    elif loan_to_value_ratio > 90:
        penalty += 0.08

    # Interest-rate burden
    if interest_rate >= 10:
        penalty += 0.10
    elif interest_rate >= 8:
        penalty += 0.05

    return min(penalty, 0.90)


# ---------------------------------------------------------
# Prediction
# ---------------------------------------------------------

def run_mortgage_analysis(
    loan_amount: float,
    annual_income: float,
    property_value: float,
    interest_rate: float,
    loan_term: int,
    loan_to_value_ratio: float,
    debt_to_income_ratio: float,
    applicant_age: str,
    derived_race: str,
    derived_sex: str,
    derived_ethnicity: str,
) -> dict[str, Any]:
    """
    Run the complete mortgage analysis.

    The final result combines:
    1. The machine-learning model probability.
    2. Financial affordability and lending-risk rules.
    """

    model, saved_columns = load_model()

    # HMDA income is represented in thousands of dollars.
    model_income = annual_income / 1000

    model_input = prepare_input(
        loan_amount=loan_amount,
        income=model_income,
        interest_rate=interest_rate,
        loan_to_value_ratio=loan_to_value_ratio,
        debt_to_income_ratio=debt_to_income_ratio,
        property_value=property_value,
        loan_term=loan_term,
        applicant_age=applicant_age,
        derived_race=derived_race,
        derived_sex=derived_sex,
        derived_ethnicity=derived_ethnicity,
        model=model,
        saved_columns=saved_columns,
    )

    raw_prediction = int(
        model.predict(model_input)[0]
    )

    model_approval_probability = (
        1.0 if raw_prediction == 1 else 0.0
    )

    model_decline_probability = (
        1.0 - model_approval_probability
    )

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(
            model_input
        )[0]

        classes = list(model.classes_)

        if 1 in classes:
            model_approval_probability = float(
                probabilities[
                    classes.index(1)
                ]
            )

        if 0 in classes:
            model_decline_probability = float(
                probabilities[
                    classes.index(0)
                ]
            )
        else:
            model_decline_probability = (
                1.0 - model_approval_probability
            )

    monthly_payment = calculate_monthly_payment(
        principal=loan_amount,
        annual_interest_rate=interest_rate,
        loan_term_months=loan_term,
    )

    monthly_income = (
        annual_income / 12
        if annual_income > 0
        else 0.0
    )

    payment_to_income_ratio = (
        monthly_payment / monthly_income * 100
        if monthly_income > 0
        else 999.0
    )

    total_payment = (
        monthly_payment * loan_term
    )

    total_interest = max(
        total_payment - loan_amount,
        0.0,
    )

    financial_risk_penalty = (
        calculate_financial_risk_penalty(
            payment_to_income_ratio=(
                payment_to_income_ratio
            ),
            debt_to_income_ratio=(
                debt_to_income_ratio
            ),
            loan_to_value_ratio=(
                loan_to_value_ratio
            ),
            interest_rate=interest_rate,
        )
    )

    # Combined final probability
    approval_probability = max(
        0.01,
        min(
            0.99,
            model_approval_probability
            - financial_risk_penalty,
        ),
    )

    decline_probability = (
        1.0 - approval_probability
    )

    critical_financial_risk = (
        annual_income <= 0
        or payment_to_income_ratio > 50
        or debt_to_income_ratio > 50
        or loan_to_value_ratio > 95
    )

    elevated_financial_risk = (
        payment_to_income_ratio > 40
        or debt_to_income_ratio > 43
        or loan_to_value_ratio > 90
    )

    if critical_financial_risk:
        final_prediction = 0
        predicted_decision = (
            "Elevated Decline Risk"
        )

        approval_probability = min(
            approval_probability,
            0.35,
        )

        decline_probability = (
            1.0 - approval_probability
        )

    elif approval_probability < 0.50:
        final_prediction = 0
        predicted_decision = (
            "Elevated Decline Risk"
        )

    elif elevated_financial_risk:
        final_prediction = 1
        predicted_decision = (
            "Approval Possible — "
            "Financial Risk Detected"
        )

    elif approval_probability >= 0.75:
        final_prediction = 1
        predicted_decision = (
            "Likely Approved"
        )

    else:
        final_prediction = 1
        predicted_decision = (
            "Approval Possible — "
            "Further Review Recommended"
        )

    return {
        "prediction": final_prediction,
        "raw_model_prediction": raw_prediction,
        "predicted_decision": predicted_decision,

        "approval_probability": (
            approval_probability
        ),
        "decline_probability": (
            decline_probability
        ),

        "model_approval_probability": (
            model_approval_probability
        ),
        "model_decline_probability": (
            model_decline_probability
        ),

        "financial_risk_penalty": (
            financial_risk_penalty
        ),

        "confidence": calculate_confidence(
            approval_probability,
            decline_probability,
        ),

        "risk_level": calculate_risk_level(
            decline_probability
        ),

        "loan_amount": loan_amount,
        "annual_income": annual_income,
        "monthly_income": monthly_income,
        "property_value": property_value,
        "interest_rate": interest_rate,

        "loan_term_months": loan_term,
        "loan_term_years": loan_term // 12,

        "loan_to_value_ratio": (
            loan_to_value_ratio
        ),

        "debt_to_income_ratio": (
            debt_to_income_ratio
        ),

        "monthly_payment": monthly_payment,

        "payment_to_income_ratio": (
            payment_to_income_ratio
        ),

        "total_payment": total_payment,
        "total_interest": total_interest,

        "applicant_age": applicant_age,
        "derived_race": derived_race,
        "derived_sex": derived_sex,

        "derived_ethnicity": (
            derived_ethnicity
        ),
    }