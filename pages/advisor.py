from __future__ import annotations

from typing import Any

import streamlit as st

from utils.financial_health import calculate_financial_health_score
from utils.session import get_analysis_result, set_page


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _currency(value: float) -> str:
    return f"${value:,.0f}"


def _percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def _load_styles() -> None:
    st.markdown(
        """
        <style>
        .nova-kicker {
            color: #64748b;
            font-size: .75rem;
            font-weight: 800;
            letter-spacing: .14em;
            text-transform: uppercase;
            margin-bottom: .3rem;
        }
        .nova-subtitle {
            color: #64748b;
            font-size: 1rem;
            line-height: 1.6;
            margin-top: -.4rem;
        }
        .nova-hero {
            padding: 1.6rem 1.7rem;
            border: 1px solid #dbeafe;
            border-radius: 22px;
            background: linear-gradient(135deg, #eff6ff, #ffffff);
            box-shadow: 0 18px 45px rgba(37, 99, 235, .08);
        }
        .nova-hero-label {
            color: #2563eb;
            font-size: .74rem;
            font-weight: 800;
            letter-spacing: .12em;
            text-transform: uppercase;
            margin: 0 0 .6rem 0;
        }
        .nova-hero-title {
            color: #0f172a;
            font-size: 1.55rem;
            font-weight: 780;
            line-height: 1.3;
            margin: 0;
        }
        .nova-hero-text {
            color: #475569;
            font-size: .97rem;
            line-height: 1.75;
            margin: .85rem 0 0 0;
        }
        .nova-stat {
            min-height: 145px;
            padding: 1.15rem 1.2rem;
            border: 1px solid #e2e8f0;
            border-radius: 18px;
            background: #ffffff;
            box-shadow: 0 10px 28px rgba(15, 23, 42, .05);
        }
        .nova-stat-label {
            color: #64748b;
            font-size: .75rem;
            font-weight: 750;
            letter-spacing: .08em;
            text-transform: uppercase;
            margin: 0 0 .6rem 0;
        }
        .nova-stat-value {
            color: #0f172a;
            font-size: 1.9rem;
            font-weight: 780;
            letter-spacing: -.04em;
            margin: 0;
        }
        .nova-stat-note {
            color: #64748b;
            font-size: .84rem;
            line-height: 1.45;
            margin: .65rem 0 0 0;
        }
        .nova-section {
            margin-top: 1.35rem;
            padding: 1.25rem 1.35rem;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            background: #ffffff;
            box-shadow: 0 10px 28px rgba(15, 23, 42, .04);
        }
        .nova-section-title {
            color: #0f172a;
            font-size: 1.14rem;
            font-weight: 750;
            margin: 0;
        }
        .nova-section-subtitle {
            color: #64748b;
            font-size: .9rem;
            line-height: 1.55;
            margin: .35rem 0 .95rem 0;
        }
        .nova-card {
            min-height: 145px;
            padding: 1rem 1.05rem;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            background: linear-gradient(160deg, #ffffff, #f8fafc);
        }
        .nova-card-label {
            font-size: .7rem;
            font-weight: 800;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin: 0 0 .5rem 0;
        }
        .nova-positive { color: #15803d; }
        .nova-warning { color: #b45309; }
        .nova-neutral { color: #2563eb; }
        .nova-card-title {
            color: #0f172a;
            font-size: .98rem;
            font-weight: 720;
            margin: 0 0 .45rem 0;
        }
        .nova-card-text {
            color: #64748b;
            font-size: .84rem;
            line-height: 1.55;
            margin: 0;
        }
        .nova-plan {
            min-height: 170px;
            padding: 1.1rem;
            border: 1px solid #dbeafe;
            border-radius: 18px;
            background: #f8fbff;
        }
        .nova-plan-step {
            color: #2563eb;
            font-size: .7rem;
            font-weight: 800;
            letter-spacing: .1em;
            text-transform: uppercase;
            margin: 0 0 .55rem 0;
        }
        .nova-plan-title {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 740;
            margin: 0 0 .5rem 0;
        }
        .nova-plan-text {
            color: #64748b;
            font-size: .85rem;
            line-height: 1.6;
            margin: 0;
        }
        .nova-outlook {
            padding: 1.35rem 1.45rem;
            border: 1px solid #dbeafe;
            border-radius: 20px;
            background: linear-gradient(135deg, #eff6ff, #ffffff);
        }
        .nova-outlook-title {
            color: #0f172a;
            font-size: 1.05rem;
            font-weight: 750;
            margin: 0 0 .45rem 0;
        }
        .nova-outlook-text {
            color: #475569;
            font-size: .92rem;
            line-height: 1.65;
            margin: 0;
        }
        div[data-testid="stButton"] > button {
            min-height: 44px;
            border-radius: 12px;
            font-weight: 650;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _assessment(result: dict[str, Any], health: dict[str, Any]) -> tuple[str, str]:
    probability = _safe_float(result.get("approval_probability"))
    score = int(health.get("score", 0))
    risk = str(result.get("risk_level", "Moderate"))

    if probability >= 0.80 and score >= 80:
        return (
            "Your mortgage profile is currently strong.",
            "The model indicates a favorable approval outlook supported by healthy "
            "financial capacity. Preserve the current profile and avoid new debt "
            f"before underwriting. Current modeled risk level: {risk}.",
        )
    if probability >= 0.65 and score >= 65:
        return (
            "Your profile is promising, with room to strengthen.",
            "The application shows a positive direction, although selected "
            "affordability or equity indicators can still improve. A focused "
            f"adjustment may strengthen the outcome. Current risk level: {risk}.",
        )
    if probability >= 0.50:
        return (
            "Your profile is balanced but requires improvement.",
            "The current application contains several factors that may limit lender "
            "confidence. Focus on debt reduction, equity, and payment affordability. "
            f"Current risk level: {risk}.",
        )

    return (
        "Your current profile needs meaningful strengthening.",
        "The model identifies elevated lending risk under the current structure. "
        "Reducing financial pressure before applying again is the strongest path "
        f"forward. Current risk level: {risk}.",
    )


def _strengths(result: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    probability = _safe_float(result.get("approval_probability"))
    dti = _safe_float(result.get("debt_to_income_ratio"))
    ltv = _safe_float(result.get("loan_to_value_ratio"))
    payment_ratio = _safe_float(result.get("payment_to_income_ratio"))
    income = _safe_float(result.get("annual_income"))

    if probability >= 0.70:
        items.append({
            "title": "Strong model outlook",
            "text": f"The current approval probability is {_percent(probability)}.",
        })
    if dti <= 36:
        items.append({
            "title": "Manageable debt exposure",
            "text": f"DTI is {dti:.1f}%, supporting a healthy affordability profile.",
        })
    if ltv <= 80:
        items.append({
            "title": "Healthy borrower equity",
            "text": f"LTV is {ltv:.1f}%, providing a stronger equity buffer.",
        })
    if payment_ratio <= 28:
        items.append({
            "title": "Comfortable payment burden",
            "text": f"The payment uses {payment_ratio:.1f}% of monthly income.",
        })
    if income >= 100000:
        items.append({
            "title": "Strong income capacity",
            "text": f"Annual income of {_currency(income)} supports repayment capacity.",
        })

    if not items:
        items.append({
            "title": "Clear improvement baseline",
            "text": "The current application provides a measurable foundation for targeted improvement.",
        })

    return items[:3]


def _risks(result: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    dti = _safe_float(result.get("debt_to_income_ratio"))
    ltv = _safe_float(result.get("loan_to_value_ratio"))
    payment_ratio = _safe_float(result.get("payment_to_income_ratio"))
    interest_rate = _safe_float(result.get("interest_rate"))
    total_interest = _safe_float(result.get("total_interest"))

    if dti > 43:
        items.append({
            "title": "High debt-to-income pressure",
            "text": f"DTI is {dti:.1f}%, which may reduce lender confidence.",
        })
    elif dti > 36:
        items.append({
            "title": "Debt level above preferred range",
            "text": f"DTI is {dti:.1f}%, above the strongest affordability zone.",
        })

    if ltv > 90:
        items.append({
            "title": "Limited borrower equity",
            "text": f"LTV is {ltv:.1f}%, leaving little protection against value changes.",
        })
    elif ltv > 80:
        items.append({
            "title": "Equity position can improve",
            "text": f"LTV is {ltv:.1f}%, which may increase lender exposure.",
        })

    if payment_ratio > 36:
        items.append({
            "title": "Elevated payment burden",
            "text": f"The payment represents {payment_ratio:.1f}% of monthly income.",
        })
    elif payment_ratio > 28:
        items.append({
            "title": "Payment burden above ideal",
            "text": f"The payment represents {payment_ratio:.1f}% of monthly income.",
        })

    if interest_rate >= 8:
        items.append({
            "title": "High financing cost",
            "text": (
                f"The interest rate is {interest_rate:.2f}% with estimated total "
                f"interest of {_currency(total_interest)}."
            ),
        })

    if not items:
        items.append({
            "title": "No major structural warning",
            "text": "The main mortgage indicators are currently within a manageable range.",
        })

    return items[:3]


def _plan(result: dict[str, Any]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    dti = _safe_float(result.get("debt_to_income_ratio"))
    ltv = _safe_float(result.get("loan_to_value_ratio"))
    payment_ratio = _safe_float(result.get("payment_to_income_ratio"))
    interest_rate = _safe_float(result.get("interest_rate"))
    loan_amount = _safe_float(result.get("loan_amount"))

    if dti > 36:
        items.append({
            "title": "Reduce monthly debt obligations",
            "text": "Target DTI below 36% by prioritizing high-cost debt and avoiding new credit commitments.",
        })

    if ltv > 80:
        target_loan = loan_amount * 80 / max(ltv, 0.01)
        reduction = max(loan_amount - target_loan, 0)
        items.append({
            "title": "Strengthen borrower equity",
            "text": (
                f"Move LTV toward 80% by increasing the down payment or reducing "
                f"the requested loan by approximately {_currency(reduction)}."
            ),
        })

    if payment_ratio > 28:
        items.append({
            "title": "Lower the payment burden",
            "text": "Compare a lower loan amount, improved rate, or longer term while reviewing lifetime interest.",
        })

    if interest_rate >= 6.5 and len(items) < 3:
        items.append({
            "title": "Improve financing terms",
            "text": f"Compare alternatives below the current {interest_rate:.2f}% interest rate.",
        })

    if not items:
        items.append({
            "title": "Protect the current profile",
            "text": "Maintain stable income, preserve cash reserves, and avoid large new debts before underwriting.",
        })

    return items[:3]


def _improved_outlook(result: dict[str, Any]) -> tuple[float, str]:
    current = _safe_float(result.get("approval_probability"))
    dti = _safe_float(result.get("debt_to_income_ratio"))
    ltv = _safe_float(result.get("loan_to_value_ratio"))
    payment_ratio = _safe_float(result.get("payment_to_income_ratio"))
    interest_rate = _safe_float(result.get("interest_rate"))

    increase = 0.0
    actions: list[str] = []

    if dti > 43:
        increase += 0.08
        actions.append("reduce DTI below 43%")
    elif dti > 36:
        increase += 0.05
        actions.append("reduce DTI toward 36%")

    if ltv > 90:
        increase += 0.08
        actions.append("increase equity materially")
    elif ltv > 80:
        increase += 0.05
        actions.append("move LTV toward 80%")

    if payment_ratio > 36:
        increase += 0.06
        actions.append("reduce payment pressure")
    elif payment_ratio > 28:
        increase += 0.03
        actions.append("lower the payment ratio")

    if interest_rate >= 8:
        increase += 0.03
        actions.append("secure better financing terms")

    improved = min(current + increase, 0.95)

    if actions:
        explanation = "This estimate assumes the applicant can " + ", ".join(actions) + "."
    else:
        explanation = "The current profile is already stable, so the estimate remains conservative."

    return improved, explanation


def _render_cards(items: list[dict[str, str]], tone: str) -> None:
    columns = st.columns(len(items), gap="medium")
    label = "Positive factor" if tone == "positive" else "Area for attention"
    css = "nova-positive" if tone == "positive" else "nova-warning"

    for column, item in zip(columns, items):
        with column:
            st.markdown(
                f"""
                <div class="nova-card">
                    <p class="nova-card-label {css}">{label}</p>
                    <p class="nova-card-title">{item["title"]}</p>
                    <p class="nova-card-text">{item["text"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _render_plan(items: list[dict[str, str]]) -> None:
    columns = st.columns(len(items), gap="medium")

    for index, (column, item) in enumerate(zip(columns, items), start=1):
        with column:
            st.markdown(
                f"""
                <div class="nova-plan">
                    <p class="nova-plan-step">Step {index:02d}</p>
                    <p class="nova-plan-title">{item["title"]}</p>
                    <p class="nova-plan-text">{item["text"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def show_ai_advisor() -> None:
    _load_styles()
    result = get_analysis_result()

    if result is None:
        st.warning(
            "No mortgage analysis is currently available. Please complete an application first."
        )
        if st.button(
            "Start Mortgage Analysis",
            key="advisor_start_analysis",
            type="primary",
            width="stretch",
        ):
            set_page("approval")
        return

    health = calculate_financial_health_score(result)
    probability = _safe_float(result.get("approval_probability"))
    score = int(health.get("score", 0))
    risk = str(result.get("risk_level", "Moderate"))
    payment = _safe_float(result.get("monthly_payment"))

    header_left, header_results, header_home = st.columns(
        [5, 1.15, 1],
        vertical_alignment="center",
    )

    with header_left:
        st.markdown(
            '<p class="nova-kicker">NOVA PERSONALIZED GUIDANCE</p>',
            unsafe_allow_html=True,
        )
        st.title("AI Mortgage Advisor")
        st.markdown(
            '<p class="nova-subtitle">'
            "Personalized mortgage guidance based on your current financial profile, "
            "model outcome, and affordability indicators."
            "</p>",
            unsafe_allow_html=True,
        )

    with header_results:
        if st.button(
            "Return to Results",
            key="advisor_return_results",
            width="stretch",
        ):
            set_page("results")

    with header_home:
        if st.button(
            "Home",
            key="advisor_home",
            width="stretch",
        ):
            set_page("home")

    title, text = _assessment(result, health)

    st.markdown(
        f"""
        <div class="nova-hero">
            <p class="nova-hero-label">Overall Assessment</p>
            <p class="nova-hero-title">{title}</p>
            <p class="nova-hero-text">{text}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    cols = st.columns(4, gap="medium")
    values = [
        ("Approval Outlook", _percent(probability), "Current machine-learning estimate"),
        ("Financial Health", f"{score}/100", health["classification"]),
        ("Risk Profile", risk, "Based on the current application"),
        ("Monthly Payment", _currency(payment), "Estimated contractual payment"),
    ]

    for column, (label, value, note) in zip(cols, values):
        with column:
            st.markdown(
                f"""
                <div class="nova-stat">
                    <p class="nova-stat-label">{label}</p>
                    <p class="nova-stat-value">{value}</p>
                    <p class="nova-stat-note">{note}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div class="nova-section">
            <p class="nova-section-title">What Supports Your Application</p>
            <p class="nova-section-subtitle">
                The strongest financial factors currently contributing to mortgage readiness.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_cards(_strengths(result), "positive")

    st.markdown(
        """
        <div class="nova-section">
            <p class="nova-section-title">What Requires Attention</p>
            <p class="nova-section-subtitle">
                The main factors that may limit affordability or lender confidence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_cards(_risks(result), "warning")

    st.markdown(
        """
        <div class="nova-section">
            <p class="nova-section-title">Personalized Improvement Plan</p>
            <p class="nova-section-subtitle">
                A focused sequence of actions designed to strengthen the mortgage profile.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    _render_plan(_plan(result))

    improved, explanation = _improved_outlook(result)

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    outlook_left, outlook_right = st.columns(
        [1.3, 1],
        gap="large",
        vertical_alignment="center",
    )

    with outlook_left:
        st.markdown(
            f"""
            <div class="nova-outlook">
                <p class="nova-outlook-title">Estimated Improved Outlook</p>
                <p class="nova-outlook-text">
                    The current modeled probability is <strong>{_percent(probability)}</strong>.
                    Under a stronger affordability structure, the planning estimate may
                    improve toward <strong>{_percent(improved)}</strong>. {explanation}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with outlook_right:
        st.progress(
            improved,
            text=f"Potential planning outlook: {_percent(improved)}",
        )
        st.caption(
            "This is a transparent planning estimate, not a guaranteed lender decision."
        )

    st.markdown("<div style='height:1.2rem'></div>", unsafe_allow_html=True)

    footer_left, footer_middle, footer_right = st.columns(3, gap="medium")

    with footer_left:
        if st.button(
            "Detailed Analysis",
            key="advisor_detailed_analysis",
            type="primary",
            width="stretch",
        ):
            set_page("detailed_analysis")

    with footer_middle:
        if st.button(
            "Scenario Analysis",
            key="advisor_scenario_analysis",
            type="primary",
            width="stretch",
        ):
            set_page("simulator")

    with footer_right:
        if st.button(
            "Back to Results",
            key="advisor_back_results",
            type="primary",
            width="stretch",
        ):
            set_page("results")

    st.caption(
        "NOVA provides analytical guidance and does not replace formal underwriting or lender approval."
    )