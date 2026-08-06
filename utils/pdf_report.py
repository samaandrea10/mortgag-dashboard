from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Mapping

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PAGE_WIDTH, PAGE_HEIGHT = A4

NAVY = colors.HexColor("#0B1F33")
BLUE = colors.HexColor("#1769E0")
LIGHT_BLUE = colors.HexColor("#EAF2FF")
VERY_LIGHT_BLUE = colors.HexColor("#F6F9FE")
GREEN = colors.HexColor("#14804A")
LIGHT_GREEN = colors.HexColor("#E8F5EE")
RED = colors.HexColor("#C9362B")
LIGHT_RED = colors.HexColor("#FDEDEC")
ORANGE = colors.HexColor("#C76A00")
LIGHT_ORANGE = colors.HexColor("#FFF3E2")
GRAY = colors.HexColor("#667085")
LIGHT_GRAY = colors.HexColor("#EAECF0")
DARK_GRAY = colors.HexColor("#344054")
WHITE = colors.white


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


def _safe_text(value: Any, default: str = "Not provided") -> str:
    """
    Convert a value to readable text safely.
    """
    if value is None:
        return default

    text = str(value).strip()
    return text if text else default


def _get_value(
    data: Mapping[str, Any] | None,
    *keys: str,
    default: Any = None,
) -> Any:
    """
    Return the first matching value found in a dictionary.
    """
    if not data:
        return default

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    return default


def _format_currency(value: Any) -> str:
    """
    Format a value as US dollars.
    """
    number = _safe_float(value)

    if abs(number) >= 1_000_000:
        return f"${number:,.0f}"

    return f"${number:,.2f}"


def _format_percentage(value: Any) -> str:
    """
    Format a probability or percentage.

    Values between 0 and 1 are interpreted as probabilities.
    Values above 1 are interpreted as percentages.
    """
    number = _safe_float(value)

    if 0 <= number <= 1:
        number *= 100

    return f"{number:.1f}%"


def _normalize_percentage(value: Any) -> float:
    """
    Convert a probability or percentage to the range 0–100.
    """
    number = _safe_float(value)

    if 0 <= number <= 1:
        number *= 100

    return max(0.0, min(100.0, number))


def _format_ratio(value: Any) -> str:
    """
    Format a financial ratio as a percentage.
    """
    return _format_percentage(value)


def _humanize_key(key: str) -> str:
    """
    Convert a dictionary key into a readable label.
    """
    return key.replace("_", " ").strip().title()


def _decision_details(
    decision: Any,
) -> tuple[str, colors.Color, colors.Color]:
    """
    Return normalized decision text and matching colors.
    """
    decision_text = (
        _safe_text(decision, "Pending")
        .strip()
        .lower()
    )

    positive_decision = (
        decision_text in {
            "approved",
            "approve",
            "approval",
            "accepted",
            "eligible",
            "1",
            "true",
            "yes",
        }
        or decision_text.startswith("likely approved")
        or decision_text.startswith("approval possible")
    )

    negative_decision = (
        decision_text in {
            "denied",
            "declined",
            "rejected",
            "not approved",
            "0",
            "false",
            "no",
        }
        or "decline risk" in decision_text
    )

    if positive_decision:
        return decision_text.upper(), GREEN, LIGHT_GREEN

    if negative_decision:
        return decision_text.upper(), RED, LIGHT_RED

    return decision_text.upper(), ORANGE, LIGHT_ORANGE


def _risk_details(risk_level: Any) -> tuple[str, colors.Color, colors.Color]:
    """
    Return normalized risk label and matching colors.
    """
    risk_text = _safe_text(risk_level, "Moderate").strip().lower()

    if risk_text in {"low", "low risk", "excellent", "very low"}:
        return "LOW RISK", GREEN, LIGHT_GREEN

    if risk_text in {
        "high",
        "high risk",
        "very high",
        "critical",
        "severe",
    }:
        return "HIGH RISK", RED, LIGHT_RED

    return "MODERATE RISK", ORANGE, LIGHT_ORANGE


def _calculate_monthly_payment(
    loan_amount: float,
    annual_interest_rate: float,
    loan_term_years: float,
) -> float:
    """
    Calculate the estimated monthly mortgage payment.
    """
    if loan_amount <= 0 or loan_term_years <= 0:
        return 0.0

    monthly_rate = annual_interest_rate / 100 / 12
    number_of_payments = loan_term_years * 12

    if monthly_rate == 0:
        return loan_amount / number_of_payments

    payment = (
        loan_amount
        * monthly_rate
        * (1 + monthly_rate) ** number_of_payments
        / ((1 + monthly_rate) ** number_of_payments - 1)
    )

    return payment


def _calculate_financial_values(
    applicant_data: Mapping[str, Any],
    result_data: Mapping[str, Any],
) -> dict[str, float]:
    """
    Calculate missing financial values from the available application data.
    """
    income = _safe_float(
        _get_value(
            applicant_data,
            "income",
            "annual_income",
            "applicant_income",
            default=0,
        )
    )

    loan_amount = _safe_float(
        _get_value(
            applicant_data,
            "loan_amount",
            "requested_loan_amount",
            default=0,
        )
    )

    property_value = _safe_float(
        _get_value(
            applicant_data,
            "property_value",
            "home_value",
            default=0,
        )
    )

    interest_rate = _safe_float(
        _get_value(
            applicant_data,
            "interest_rate",
            "rate",
            default=0,
        )
    )

    loan_term = _safe_float(
        _get_value(
            applicant_data,
            "loan_term",
            "loan_term_years",
            "term",
            default=30,
        )
    )

    monthly_payment = _safe_float(
        _get_value(
            result_data,
            "monthly_payment",
            "estimated_monthly_payment",
            default=0,
        )
    )

    if monthly_payment <= 0:
        monthly_payment = _calculate_monthly_payment(
            loan_amount=loan_amount,
            annual_interest_rate=interest_rate,
            loan_term_years=loan_term,
        )

    total_repayment = _safe_float(
        _get_value(
            result_data,
            "total_repayment",
            "total_payment",
            default=0,
        )
    )

    if total_repayment <= 0 and loan_term > 0:
        total_repayment = monthly_payment * loan_term * 12

    total_interest = _safe_float(
        _get_value(
            result_data,
            "total_interest",
            "estimated_total_interest",
            default=0,
        )
    )

    if total_interest <= 0:
        total_interest = max(total_repayment - loan_amount, 0)

    ltv = _safe_float(
        _get_value(
            result_data,
            "ltv",
            "loan_to_value_ratio",
            default=0,
        )
    )

    if ltv <= 0 and property_value > 0:
        ltv = loan_amount / property_value * 100

    dti = _safe_float(
        _get_value(
            result_data,
            "dti",
            "debt_to_income_ratio",
            default=_get_value(
                applicant_data,
                "debt_to_income_ratio",
                "dti",
                default=0,
            ),
        )
    )

    payment_to_income = _safe_float(
        _get_value(
            result_data,
            "payment_to_income",
            "payment_to_income_ratio",
            default=0,
        )
    )

    if payment_to_income <= 0 and income > 0:
        payment_to_income = monthly_payment / (income / 12) * 100

    return {
        "income": income,
        "loan_amount": loan_amount,
        "property_value": property_value,
        "interest_rate": interest_rate,
        "loan_term": loan_term,
        "monthly_payment": monthly_payment,
        "total_repayment": total_repayment,
        "total_interest": total_interest,
        "ltv": ltv,
        "dti": dti,
        "payment_to_income": payment_to_income,
    }


def _build_styles() -> dict[str, ParagraphStyle]:
    """
    Create all paragraph styles used in the report.
    """
    base_styles = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            name="NOVA_Title",
            parent=base_styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=28,
            textColor=NAVY,
            alignment=TA_LEFT,
            spaceAfter=2,
        ),
        "subtitle": ParagraphStyle(
            name="NOVA_Subtitle",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=GRAY,
            alignment=TA_LEFT,
        ),
        "section": ParagraphStyle(
            name="NOVA_Section",
            parent=base_styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=8,
        ),
        "body": ParagraphStyle(
            name="NOVA_Body",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14,
            textColor=DARK_GRAY,
        ),
        "body_small": ParagraphStyle(
            name="NOVA_BodySmall",
            parent=base_styles["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=11,
            textColor=GRAY,
        ),
        "label": ParagraphStyle(
            name="NOVA_Label",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=GRAY,
        ),
        "value": ParagraphStyle(
            name="NOVA_Value",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=NAVY,
        ),
        "metric_value": ParagraphStyle(
            name="NOVA_MetricValue",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=19,
            textColor=NAVY,
            alignment=TA_CENTER,
        ),
        "metric_label": ParagraphStyle(
            name="NOVA_MetricLabel",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=GRAY,
            alignment=TA_CENTER,
        ),
        "decision": ParagraphStyle(
            name="NOVA_Decision",
            parent=base_styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
        ),
        "center": ParagraphStyle(
            name="NOVA_Center",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=DARK_GRAY,
            alignment=TA_CENTER,
        ),
        "right": ParagraphStyle(
            name="NOVA_Right",
            parent=base_styles["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=GRAY,
            alignment=TA_RIGHT,
        ),
    }


def _create_header(
    styles: dict[str, ParagraphStyle],
    logo_path: str | Path | None,
) -> Table:
    """
    Create the NOVA report header.
    """
    logo_element: Any = ""

    if logo_path:
        logo_file = Path(logo_path)

        if logo_file.exists() and logo_file.is_file():
            try:
                logo_element = Image(
                    str(logo_file),
                    width=28 * mm,
                    height=16 * mm,
                )
            except Exception:
                logo_element = ""

    title_block = [
        Paragraph("NOVA", styles["title"]),
        Paragraph(
            "Mortgage Intelligence & Decision Support",
            styles["subtitle"],
        ),
    ]

    metadata_block = [
        Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            styles["right"],
        ),
        Paragraph(
            f"Report time: {datetime.now().strftime('%H:%M')}",
            styles["right"],
        ),
    ]

    header_data = [[logo_element, title_block, metadata_block]]

    header_table = Table(
        header_data,
        colWidths=[32 * mm, 92 * mm, 50 * mm],
        hAlign="LEFT",
    )

    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    return header_table


def _create_section_title(
    title: str,
    styles: dict[str, ParagraphStyle],
) -> list[Any]:
    """
    Create a standard report section heading.
    """
    return [
        Paragraph(title, styles["section"]),
        HRFlowable(
            width="100%",
            thickness=0.8,
            color=LIGHT_GRAY,
            spaceAfter=8,
        ),
    ]


def _create_decision_card(
    decision: Any,
    approval_probability: Any,
    risk_level: Any,
    styles: dict[str, ParagraphStyle],
) -> Table:
    """
    Create the primary mortgage decision card.
    """
    decision_text, decision_color, decision_background = _decision_details(
        decision
    )

    risk_text, risk_color, risk_background = _risk_details(risk_level)

    probability = _normalize_percentage(approval_probability)

    decision_style = ParagraphStyle(
        name="DecisionDynamic",
        parent=styles["decision"],
        textColor=decision_color,
    )

    risk_style = ParagraphStyle(
        name="RiskDynamic",
        parent=styles["value"],
        textColor=risk_color,
        alignment=TA_CENTER,
    )

    card_data = [
        [
            Paragraph("MODEL DECISION", styles["metric_label"]),
            Paragraph("APPROVAL PROBABILITY", styles["metric_label"]),
            Paragraph("RISK CLASSIFICATION", styles["metric_label"]),
        ],
        [
            Paragraph(decision_text, decision_style),
            Paragraph(
                f"{probability:.1f}%",
                styles["metric_value"],
            ),
            Paragraph(risk_text, risk_style),
        ],
    ]

    card_table = Table(
        card_data,
        colWidths=[58 * mm, 58 * mm, 58 * mm],
        rowHeights=[10 * mm, 20 * mm],
        hAlign="LEFT",
    )

    card_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), decision_background),
                ("BACKGROUND", (1, 0), (1, -1), LIGHT_BLUE),
                ("BACKGROUND", (2, 0), (2, -1), risk_background),
                ("BOX", (0, 0), (0, -1), 0.7, decision_color),
                ("BOX", (1, 0), (1, -1), 0.7, BLUE),
                ("BOX", (2, 0), (2, -1), 0.7, risk_color),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    return card_table


def _create_information_table(
    rows: list[tuple[str, Any]],
    styles: dict[str, ParagraphStyle],
) -> Table:
    """
    Create a two-column information table.
    """
    table_data: list[list[Any]] = []

    for label, value in rows:
        table_data.append(
            [
                Paragraph(_safe_text(label), styles["label"]),
                Paragraph(_safe_text(value), styles["value"]),
            ]
        )

    table = Table(
        table_data,
        colWidths=[66 * mm, 108 * mm],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), VERY_LIGHT_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return table


def _create_metric_cards(
    metrics: list[tuple[str, str]],
    styles: dict[str, ParagraphStyle],
) -> Table:
    """
    Create a horizontal group of financial metric cards.
    """
    labels = [
        Paragraph(label, styles["metric_label"])
        for label, _ in metrics
    ]

    values = [
        Paragraph(value, styles["metric_value"])
        for _, value in metrics
    ]

    table = Table(
        [labels, values],
        colWidths=[174 * mm / len(metrics)] * len(metrics),
        rowHeights=[9 * mm, 17 * mm],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), VERY_LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 0.7, LIGHT_GRAY),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    return table


def _create_probability_bar(
    approval_probability: Any,
    styles: dict[str, ParagraphStyle],
) -> Table:
    """
    Create a visual approval-probability bar.
    """
    probability = _normalize_percentage(approval_probability)
    remaining = 100 - probability

    probability_label = Paragraph(
        f"Approval probability: <b>{probability:.1f}%</b>",
        styles["body"],
    )

    bar_table = Table(
        [["", ""]],
        colWidths=[
            max(probability, 0.5) * 1.7 * mm,
            max(remaining, 0.5) * 1.7 * mm,
        ],
        rowHeights=[6 * mm],
        hAlign="LEFT",
    )

    bar_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), BLUE),
                ("BACKGROUND", (1, 0), (1, 0), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.5, LIGHT_GRAY),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    return Table(
        [[probability_label], [bar_table]],
        colWidths=[174 * mm],
        hAlign="LEFT",
        style=TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        ),
    )


def _generate_recommendations(
    decision: Any,
    prediction: Any,
    financial_values: Mapping[str, float],
    approval_probability: float,
) -> list[str]:
    """
    Generate practical mortgage recommendations.

    The numeric final prediction is used as the primary source
    of truth. The textual decision is used only as a fallback.
    """
    recommendations: list[str] = []

    decision_text = (
        _safe_text(decision, "")
        .strip()
        .lower()
    )

    try:
        prediction_value = int(prediction)
    except (TypeError, ValueError):
        prediction_value = -1

    if prediction_value in {0, 1}:
        is_approved = prediction_value == 1
    else:
        is_approved = (
            decision_text in {
                "approved",
                "approve",
                "approval",
                "accepted",
                "eligible",
                "1",
                "true",
                "yes",
            }
            or decision_text.startswith("likely approved")
            or decision_text.startswith("approval possible")
        )

    dti = financial_values["dti"]
    ltv = financial_values["ltv"]
    payment_to_income = financial_values["payment_to_income"]
    interest_rate = financial_values["interest_rate"]

    if is_approved:
        recommendations.append(
            "The model indicates that the application currently meets the "
            "system's approval criteria."
        )
    else:
        recommendations.append(
            "The model indicates that the current financial profile may "
            "require improvement before approval."
        )

    if dti > 43:
        recommendations.append(
            "Reduce outstanding monthly debt obligations to improve the "
            "debt-to-income ratio."
        )
    elif dti > 0:
        recommendations.append(
            "The debt-to-income ratio is within a more manageable range, "
            "but it should remain stable before closing."
        )

    if ltv > 80:
        recommendations.append(
            "Consider increasing the down payment to reduce the "
            "loan-to-value ratio and potential lending risk."
        )
    elif ltv > 0:
        recommendations.append(
            "The current loan-to-value ratio reflects a stronger equity "
            "position than a high-LTV application."
        )

    if payment_to_income > 30:
        recommendations.append(
            "The estimated monthly payment consumes a relatively large "
            "share of monthly income. A smaller loan or longer term may "
            "improve affordability."
        )

    if approval_probability < 60:
        recommendations.append(
            "A higher documented income, lower loan amount, or improved "
            "debt profile may increase the model's approval probability."
        )
    elif approval_probability >= 80:
        recommendations.append(
            "The model reports a strong approval probability; final lending "
            "approval may still require document verification and compliance checks."
        )

    if interest_rate > 0:
        recommendations.append(
            "Compare available interest-rate offers because even a small "
            "rate reduction can materially decrease total interest expense."
        )

    recommendations.append(
        "This assessment is generated by a predictive decision-support "
        "system and does not replace formal underwriting or regulatory review."
    )

    return recommendations


def _create_recommendations_table(
    recommendations: list[str],
    styles: dict[str, ParagraphStyle],
) -> Table:
    """
    Create a styled list of recommendations.
    """
    rows: list[list[Any]] = []

    for index, recommendation in enumerate(recommendations, start=1):
        number = Paragraph(
            f"<b>{index}</b>",
            styles["center"],
        )
        text = Paragraph(recommendation, styles["body"])
        rows.append([number, text])

    table = Table(
        rows,
        colWidths=[10 * mm, 164 * mm],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return table


def _create_feature_importance_table(
    feature_importance: Mapping[str, Any],
    styles: dict[str, ParagraphStyle],
) -> Table:
    """
    Create a feature-importance table.
    """
    sorted_features = sorted(
        feature_importance.items(),
        key=lambda item: _safe_float(item[1]),
        reverse=True,
    )[:10]

    table_data: list[list[Any]] = [
        [
            Paragraph("<b>Feature</b>", styles["body"]),
            Paragraph("<b>Importance</b>", styles["body"]),
        ]
    ]

    for feature_name, importance in sorted_features:
        importance_value = _safe_float(importance)

        table_data.append(
            [
                Paragraph(
                    _humanize_key(str(feature_name)),
                    styles["body"],
                ),
                Paragraph(
                    f"{importance_value:.4f}",
                    styles["value"],
                ),
            ]
        )

    table = Table(
        table_data,
        colWidths=[124 * mm, 50 * mm],
        hAlign="LEFT",
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GRAY),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 1), (1, -1), "RIGHT"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, VERY_LIGHT_BLUE]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    return table


def _draw_page_footer(canvas: Any, document: Any) -> None:
    """
    Draw a consistent footer on every page.
    """
    canvas.saveState()

    canvas.setStrokeColor(LIGHT_GRAY)
    canvas.setLineWidth(0.5)
    canvas.line(
        20 * mm,
        15 * mm,
        PAGE_WIDTH - 20 * mm,
        15 * mm,
    )

    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRAY)

    canvas.drawString(
        20 * mm,
        10 * mm,
        "NOVA Mortgage Intelligence | Confidential Decision-Support Report",
    )

    canvas.drawRightString(
        PAGE_WIDTH - 20 * mm,
        10 * mm,
        f"Page {document.page}",
    )

    canvas.restoreState()


def generate_mortgage_pdf(
    applicant_data: Mapping[str, Any] | None,
    result_data: Mapping[str, Any] | None,
    feature_importance: Mapping[str, Any] | None = None,
    logo_path: str | Path | None = None,
) -> bytes:
    """
    Generate a professional NOVA mortgage-analysis PDF.

    Parameters
    ----------
    applicant_data:
        Dictionary containing the values entered in the mortgage application.

    result_data:
        Dictionary containing prediction and financial-analysis results.

    feature_importance:
        Optional dictionary containing model features and their importance.

    logo_path:
        Optional path to the NOVA logo image.

    Returns
    -------
    bytes
        PDF file content that can be passed directly to
        Streamlit's st.download_button.
    """
    applicant_data = applicant_data or {}
    result_data = result_data or {}
    feature_importance = feature_importance or {}

    styles = _build_styles()

    financial_values = _calculate_financial_values(
        applicant_data=applicant_data,
        result_data=result_data,
    )

    decision = _get_value(
        result_data,
        "predicted_decision",
        "decision",
        "prediction_label",
        "status",
        "prediction",
        default="Pending",
    )

    approval_probability = _get_value(
        result_data,
        "approval_probability",
        "probability",
        "prediction_probability",
        "approved_probability",
        default=0,
    )

    approval_probability_normalized = _normalize_percentage(
        approval_probability
    )

    risk_level = _get_value(
        result_data,
        "risk_level",
        "risk",
        "risk_classification",
        default="Moderate",
    )

    financial_health_score = _get_value(
        result_data,
        "financial_health_score",
        "health_score",
        default=None,
    )

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=20 * mm,
        leftMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        title="NOVA Mortgage Intelligence Report",
        author="NOVA Mortgage Intelligence",
        subject="Mortgage Approval and Financial Analysis",
    )

    story: list[Any] = []

    story.append(_create_header(styles, logo_path))
    story.append(Spacer(1, 6 * mm))

    story.append(
        HRFlowable(
            width="100%",
            thickness=1.2,
            color=BLUE,
            spaceAfter=8,
        )
    )

    story.append(
        Paragraph(
            "Mortgage Decision Report",
            ParagraphStyle(
                name="ReportHeading",
                parent=styles["section"],
                fontSize=18,
                leading=22,
                spaceAfter=4,
            ),
        )
    )

    story.append(
        Paragraph(
            "Predictive approval assessment, affordability review, "
            "and financial decision support.",
            styles["subtitle"],
        )
    )

    story.append(Spacer(1, 6 * mm))

    story.append(
        _create_decision_card(
            decision=decision,
            approval_probability=approval_probability,
            risk_level=risk_level,
            styles=styles,
        )
    )

    story.append(Spacer(1, 5 * mm))
    story.append(_create_probability_bar(approval_probability, styles))
    story.append(Spacer(1, 6 * mm))

    story.extend(_create_section_title("Applicant Profile", styles))

    applicant_rows = [
        (
            "Applicant Name",
            _get_value(
                applicant_data,
                "applicant_name",
                "full_name",
                "name",
                default="Not provided",
            ),
        ),
        (
            "Applicant Age",
            _get_value(
                applicant_data,
                "applicant_age",
                "age",
                default="Not provided",
            ),
        ),
        (
            "Annual Income",
            _format_currency(financial_values["income"]),
        ),
        (
            "Sex",
            _get_value(
                applicant_data,
                "derived_sex",
                "sex",
                "gender",
                default="Not provided",
            ),
        ),
        (
            "Race",
            _get_value(
                applicant_data,
                "derived_race",
                "race",
                default="Not provided",
            ),
        ),
        (
            "Ethnicity",
            _get_value(
                applicant_data,
                "derived_ethnicity",
                "ethnicity",
                default="Not provided",
            ),
        ),
    ]

    story.append(_create_information_table(applicant_rows, styles))
    story.append(Spacer(1, 6 * mm))

    story.extend(_create_section_title("Loan Overview", styles))

    loan_rows = [
        (
            "Requested Loan Amount",
            _format_currency(financial_values["loan_amount"]),
        ),
        (
            "Property Value",
            _format_currency(financial_values["property_value"]),
        ),
        (
            "Interest Rate",
            _format_percentage(financial_values["interest_rate"]),
        ),
        (
            "Loan Term",
            f"{financial_values['loan_term']:.0f} years",
        ),
        (
            "Loan Purpose",
            _get_value(
                applicant_data,
                "loan_purpose",
                "purpose",
                default="Not provided",
            ),
        ),
        (
            "Property Type",
            _get_value(
                applicant_data,
                "property_type",
                "occupancy_type",
                default="Not provided",
            ),
        ),
    ]

    story.append(_create_information_table(loan_rows, styles))
    story.append(Spacer(1, 6 * mm))

    story.extend(_create_section_title("Financial Summary", styles))

    story.append(
        _create_metric_cards(
            [
                (
                    "MONTHLY PAYMENT",
                    _format_currency(financial_values["monthly_payment"]),
                ),
                (
                    "TOTAL INTEREST",
                    _format_currency(financial_values["total_interest"]),
                ),
                (
                    "TOTAL REPAYMENT",
                    _format_currency(financial_values["total_repayment"]),
                ),
            ],
            styles,
        )
    )

    story.append(Spacer(1, 4 * mm))

    story.append(
        _create_metric_cards(
            [
                (
                    "DEBT-TO-INCOME",
                    _format_ratio(financial_values["dti"]),
                ),
                (
                    "LOAN-TO-VALUE",
                    _format_ratio(financial_values["ltv"]),
                ),
                (
                    "PAYMENT-TO-INCOME",
                    _format_ratio(financial_values["payment_to_income"]),
                ),
            ],
            styles,
        )
    )

    if financial_health_score is not None:
        story.append(Spacer(1, 4 * mm))

        score = _safe_float(financial_health_score)
        score = max(0, min(100, score))

        story.append(
            _create_metric_cards(
                [
                    (
                        "FINANCIAL HEALTH SCORE",
                        f"{score:.0f} / 100",
                    ),
                ],
                styles,
            )
        )

    story.append(Spacer(1, 7 * mm))

    prediction = _get_value(
        result_data,
        "prediction",
        "final_prediction",
        default=None,
    )

    recommendations = _generate_recommendations(
        decision=decision,
        prediction=prediction,
        financial_values=financial_values,
        approval_probability=approval_probability_normalized,
    )

    story.extend(
        _create_section_title(
            "NOVA Decision-Support Recommendations",
            styles,
        )
    )

    story.append(
        _create_recommendations_table(
            recommendations=recommendations,
            styles=styles,
        )
    )

    if feature_importance:
        story.append(PageBreak())

        story.append(_create_header(styles, logo_path))
        story.append(Spacer(1, 6 * mm))

        story.extend(
            _create_section_title(
                "Model Feature Importance",
                styles,
            )
        )

        story.append(
            Paragraph(
                "The following variables had the strongest influence on "
                "the predictive model. Feature importance indicates relative "
                "model contribution and does not establish causation.",
                styles["body"],
            )
        )

        story.append(Spacer(1, 4 * mm))

        story.append(
            _create_feature_importance_table(
                feature_importance=feature_importance,
                styles=styles,
            )
        )

        story.append(Spacer(1, 7 * mm))

    story.append(Spacer(1, 7 * mm))

    disclaimer_block = KeepTogether(
        [
            Paragraph("Important Notice", styles["section"]),
            Table(
                [
                    [
                        Paragraph(
                            "This report was generated by NOVA, an academic "
                            "mortgage decision-support system based on predictive "
                            "analytics. The output is intended for analytical and "
                            "educational purposes only. It does not constitute a "
                            "binding lending decision, credit offer, financial "
                            "advice, or regulatory approval. Final underwriting "
                            "must include verified documentation, institutional "
                            "policies, legal requirements, and human review.",
                            styles["body_small"],
                        )
                    ]
                ],
                colWidths=[174 * mm],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), VERY_LIGHT_BLUE),
                        ("BOX", (0, 0), (-1, -1), 0.6, LIGHT_GRAY),
                        ("LEFTPADDING", (0, 0), (-1, -1), 9),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
                        ("TOPPADDING", (0, 0), (-1, -1), 9),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
                    ]
                ),
            ),
        ]
    )

    story.append(disclaimer_block)

    document.build(
        story,
        onFirstPage=_draw_page_footer,
        onLaterPages=_draw_page_footer,
    )

    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes


def create_pdf_filename(
    applicant_data: Mapping[str, Any] | None = None,
) -> str:
    """
    Create a safe and professional PDF filename.
    """
    applicant_data = applicant_data or {}

    applicant_name = _safe_text(
        _get_value(
            applicant_data,
            "applicant_name",
            "full_name",
            "name",
            default="Applicant",
        ),
        "Applicant",
    )

    safe_name = "".join(
        character
        for character in applicant_name
        if character.isalnum() or character in {" ", "_", "-"}
    ).strip()

    safe_name = safe_name.replace(" ", "_") or "Applicant"

    date_text = datetime.now().strftime("%Y%m%d")

    return f"NOVA_Mortgage_Report_{safe_name}_{date_text}.pdf"