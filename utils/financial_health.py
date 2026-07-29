from __future__ import annotations

from typing import Any, Mapping


def _safe_float(value: Any, default: float = 0.0) -> float:
    """
    Convert a value to float safely.
    """
    if value is None:
        return default

    if isinstance(value, str):
        cleaned_value = (
            value.replace("$", "")
            .replace("₪", "")
            .replace(",", "")
            .replace("%", "")
            .strip()
        )

        if not cleaned_value:
            return default

        value = cleaned_value

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_probability(value: Any) -> float:
    """
    Normalize a probability into the range 0–100.

    Examples
    --------
    0.82 becomes 82
    82 remains 82
    """
    probability = _safe_float(value)

    if 0 <= probability <= 1:
        probability *= 100

    return max(0.0, min(100.0, probability))


def _score_dti(dti_ratio: float) -> float:
    """
    Score the debt-to-income ratio on a 0–100 scale.
    Lower DTI receives a stronger score.
    """
    if dti_ratio <= 20:
        return 100.0

    if dti_ratio <= 28:
        return 92.0

    if dti_ratio <= 36:
        return 82.0

    if dti_ratio <= 43:
        return 65.0

    if dti_ratio <= 50:
        return 42.0

    return 20.0


def _score_ltv(ltv_ratio: float) -> float:
    """
    Score the loan-to-value ratio on a 0–100 scale.
    Lower LTV indicates a stronger equity position.
    """
    if ltv_ratio <= 60:
        return 100.0

    if ltv_ratio <= 70:
        return 92.0

    if ltv_ratio <= 80:
        return 82.0

    if ltv_ratio <= 90:
        return 62.0

    if ltv_ratio <= 95:
        return 42.0

    return 20.0


def _score_payment_to_income(payment_ratio: float) -> float:
    """
    Score the estimated mortgage-payment burden.
    """
    if payment_ratio <= 20:
        return 100.0

    if payment_ratio <= 28:
        return 90.0

    if payment_ratio <= 36:
        return 72.0

    if payment_ratio <= 43:
        return 52.0

    if payment_ratio <= 50:
        return 35.0

    return 15.0


def _score_income_strength(
    annual_income: float,
    monthly_payment: float,
) -> float:
    """
    Score income strength relative to the estimated mortgage payment.
    """
    if annual_income <= 0:
        return 0.0

    monthly_income = annual_income / 12

    if monthly_income <= 0:
        return 0.0

    disposable_income_after_payment = monthly_income - monthly_payment
    remaining_income_ratio = (
        disposable_income_after_payment / monthly_income
    ) * 100

    if remaining_income_ratio >= 80:
        return 100.0

    if remaining_income_ratio >= 72:
        return 90.0

    if remaining_income_ratio >= 64:
        return 78.0

    if remaining_income_ratio >= 55:
        return 62.0

    if remaining_income_ratio >= 45:
        return 42.0

    return 20.0


def calculate_financial_health_score(
    result: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Calculate the NOVA Financial Health Score.

    The score combines five financial and predictive factors:

    - Approval probability: 30%
    - Debt-to-income ratio: 20%
    - Loan-to-value ratio: 20%
    - Payment-to-income ratio: 20%
    - Income strength: 10%

    Parameters
    ----------
    result:
        Mortgage analysis result dictionary.

    Returns
    -------
    dict
        Financial score, classification, component scores,
        strengths, concerns, and explanation.
    """
    approval_probability = _normalize_probability(
        result.get("approval_probability", 0)
    )

    dti_ratio = _safe_float(
        result.get("debt_to_income_ratio", 0)
    )

    ltv_ratio = _safe_float(
        result.get("loan_to_value_ratio", 0)
    )

    payment_ratio = _safe_float(
        result.get("payment_to_income_ratio", 0)
    )

    annual_income = _safe_float(
        result.get("annual_income", 0)
    )

    monthly_payment = _safe_float(
        result.get("monthly_payment", 0)
    )

    component_scores = {
        "Approval Strength": approval_probability,
        "Debt Management": _score_dti(dti_ratio),
        "Equity Position": _score_ltv(ltv_ratio),
        "Mortgage Affordability": _score_payment_to_income(
            payment_ratio
        ),
        "Income Capacity": _score_income_strength(
            annual_income=annual_income,
            monthly_payment=monthly_payment,
        ),
    }

    weighted_score = (
        component_scores["Approval Strength"] * 0.30
        + component_scores["Debt Management"] * 0.20
        + component_scores["Equity Position"] * 0.20
        + component_scores["Mortgage Affordability"] * 0.20
        + component_scores["Income Capacity"] * 0.10
    )

    final_score = int(round(max(0.0, min(100.0, weighted_score))))

    classification, risk_band, summary = _classify_score(
        final_score
    )

    strengths = _identify_strengths(
        approval_probability=approval_probability,
        dti_ratio=dti_ratio,
        ltv_ratio=ltv_ratio,
        payment_ratio=payment_ratio,
    )

    concerns = _identify_concerns(
        approval_probability=approval_probability,
        dti_ratio=dti_ratio,
        ltv_ratio=ltv_ratio,
        payment_ratio=payment_ratio,
    )

    return {
        "score": final_score,
        "classification": classification,
        "risk_band": risk_band,
        "summary": summary,
        "component_scores": component_scores,
        "strengths": strengths,
        "concerns": concerns,
        "inputs": {
            "approval_probability": approval_probability,
            "debt_to_income_ratio": dti_ratio,
            "loan_to_value_ratio": ltv_ratio,
            "payment_to_income_ratio": payment_ratio,
            "annual_income": annual_income,
            "monthly_payment": monthly_payment,
        },
    }


def _classify_score(
    score: int,
) -> tuple[str, str, str]:
    """
    Convert the numeric score into a financial-health category.
    """
    if score >= 90:
        return (
            "Excellent Financial Profile",
            "Very Low Financial Risk",
            "The applicant demonstrates strong affordability, "
            "manageable debt exposure, and a highly favorable "
            "mortgage profile.",
        )

    if score >= 80:
        return (
            "Strong Financial Profile",
            "Low Financial Risk",
            "The applicant demonstrates a healthy overall financial "
            "position with only limited areas requiring attention.",
        )

    if score >= 70:
        return (
            "Good Financial Profile",
            "Moderate-Low Financial Risk",
            "The applicant's financial position is generally stable, "
            "although selected affordability indicators may benefit "
            "from improvement.",
        )

    if score >= 60:
        return (
            "Moderate Financial Profile",
            "Moderate Financial Risk",
            "The application shows a mixed financial profile and "
            "should receive additional affordability review.",
        )

    if score >= 45:
        return (
            "Weak Financial Profile",
            "Elevated Financial Risk",
            "Several financial indicators may reduce mortgage "
            "affordability and approval strength.",
        )

    return (
        "High-Risk Financial Profile",
        "High Financial Risk",
        "The applicant's current profile contains significant "
        "affordability or lending-risk concerns.",
    )


def _identify_strengths(
    approval_probability: float,
    dti_ratio: float,
    ltv_ratio: float,
    payment_ratio: float,
) -> list[str]:
    """
    Identify the strongest elements in the applicant's profile.
    """
    strengths: list[str] = []

    if approval_probability >= 80:
        strengths.append(
            "The predictive model reports a strong approval probability."
        )
    elif approval_probability >= 65:
        strengths.append(
            "The predictive model reports a generally favorable "
            "approval outlook."
        )

    if dti_ratio <= 36:
        strengths.append(
            "The debt-to-income ratio indicates manageable "
            "overall debt obligations."
        )

    if ltv_ratio <= 80:
        strengths.append(
            "The loan-to-value ratio reflects a relatively strong "
            "equity position."
        )

    if payment_ratio <= 28:
        strengths.append(
            "The estimated mortgage payment represents a healthy "
            "share of monthly income."
        )

    if not strengths:
        strengths.append(
            "The application contains limited positive indicators, "
            "but selected factors may still support further review."
        )

    return strengths


def _identify_concerns(
    approval_probability: float,
    dti_ratio: float,
    ltv_ratio: float,
    payment_ratio: float,
) -> list[str]:
    """
    Identify financial factors that may require attention.
    """
    concerns: list[str] = []

    if approval_probability < 60:
        concerns.append(
            "The model approval probability is below the preferred range."
        )

    if dti_ratio > 43:
        concerns.append(
            "The debt-to-income ratio may indicate a high overall "
            "debt burden."
        )
    elif dti_ratio > 36:
        concerns.append(
            "The debt-to-income ratio should be reviewed carefully."
        )

    if ltv_ratio > 90:
        concerns.append(
            "The high loan-to-value ratio indicates limited borrower "
            "equity and elevated lending exposure."
        )
    elif ltv_ratio > 80:
        concerns.append(
            "The loan-to-value ratio is above the strongest "
            "equity range."
        )

    if payment_ratio > 36:
        concerns.append(
            "The estimated mortgage payment may place substantial "
            "pressure on monthly income."
        )
    elif payment_ratio > 28:
        concerns.append(
            "The mortgage-payment burden is moderate and should "
            "remain under observation."
        )

    if not concerns:
        concerns.append(
            "No major affordability concerns were identified by the "
            "NOVA scoring framework."
        )

    return concerns


def get_score_status(score: int) -> dict[str, str]:
    """
    Return display settings for the score.

    The color names can be used later in Streamlit charts,
    cards, and PDF sections.
    """
    if score >= 90:
        return {
            "label": "Excellent",
            "color": "#14804A",
            "background": "#E8F5EE",
            "icon": "🏆",
        }

    if score >= 80:
        return {
            "label": "Strong",
            "color": "#14804A",
            "background": "#E8F5EE",
            "icon": "✓",
        }

    if score >= 70:
        return {
            "label": "Good",
            "color": "#1769E0",
            "background": "#EAF2FF",
            "icon": "✓",
        }

    if score >= 60:
        return {
            "label": "Moderate",
            "color": "#C76A00",
            "background": "#FFF3E2",
            "icon": "!",
        }

    if score >= 45:
        return {
            "label": "Weak",
            "color": "#C9362B",
            "background": "#FDEDEC",
            "icon": "⚠",
        }

    return {
        "label": "High Risk",
        "color": "#C9362B",
        "background": "#FDEDEC",
        "icon": "⚠",
    }