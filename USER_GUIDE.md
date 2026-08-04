#  NOVA Mortgage Intelligence

## Professional User Guide

[![Open Live Application](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mortgage-dashboard-sama.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/Model-Random%20Forest-orange)](https://scikit-learn.org/)
[![Deployment](https://img.shields.io/badge/Deployment-Streamlit-red?logo=streamlit)](https://streamlit.io/)

---

## Welcome to NOVA

**NOVA Mortgage Intelligence** is an interactive Machine Learning platform for mortgage application analysis.

The system enables users to:

- Enter a new mortgage application.
- Receive an estimated approval or decline outcome.
- View approval and decline probabilities.
- Evaluate affordability and lending-risk indicators.
- Review the final model's performance.
- Examine the variables that most influence predictions.
- Record verified actual outcomes for controlled model monitoring.
- Generate a downloadable PDF analysis report.

> **Important:** NOVA is an academic decision-support system.  
> It does not replace formal lender underwriting, legal advice, or an official credit decision.

---

#  Access the Application

## Live Application

### [Launch NOVA Mortgage Intelligence](https://mortgage-dashboard-sama.streamlit.app/)

The application runs directly in a web browser and does not require local installation.

The first opening may take slightly longer because Streamlit Community Cloud may need to wake the application and load the Machine Learning model.

---

#  Quick Start

A complete mortgage analysis can be performed in five steps:

1. Open the live application.
2. Select **Analyze Application**.
3. Enter the financial and applicant information.
4. Select **Analyze Mortgage Application**.
5. Review the prediction, probabilities, risk indicators, financial analysis, and recommendations.

---

#  Application Navigation

The NOVA home page provides access to three central analytical areas.

| Section | Purpose |
|---|---|
| **Mortgage Analysis** | Enter a new mortgage application and receive a complete prediction. |
| **Model Performance** | Review the scientific evaluation of the final Machine Learning model. |
| **Model Feedback** | Record a verified real-world outcome for future monitoring and controlled retraining. |

Additional pages become available after an application is analyzed:

- Results Dashboard
- Detailed Analysis
- Mortgage Simulator
- AI-Oriented Financial Advisor
- PDF Report

---

#  Mortgage Analysis

## Step 1 — Open the Analysis Form

From the home page, select:

```text
Analyze Application
```

The application form contains two sections:

1. Financial Information
2. Applicant Information

---

#  Financial Information

## Loan Amount

The total amount requested by the applicant.

Example:

```text
250000
```

This represents a requested mortgage of **$250,000**.

---

## Annual Income

The applicant's estimated gross annual income.

Example:

```text
120000
```

This represents annual income of **$120,000**.

---

## Property Value

The estimated market value of the property.

Example:

```text
350000
```

This represents a property value of **$350,000**.

---

## Annual Interest Rate

The annual mortgage interest rate expressed as a percentage.

Example:

```text
4.2
```

This represents an annual interest rate of **4.2%**.

---

## Loan Term

The duration of the mortgage.

Available terms may include:

- 10 years
- 15 years
- 20 years
- 25 years
- 30 years

A longer loan term usually reduces the monthly payment but increases the total interest paid over the full loan duration.

---

## Loan-to-Value Ratio — LTV

The Loan-to-Value Ratio compares the requested loan amount with the property value.

```text
LTV = Loan Amount ÷ Property Value × 100
```

Example:

```text
Loan Amount: $250,000
Property Value: $350,000
LTV: approximately 71%
```

General interpretation:

| LTV | General Interpretation |
|---:|---|
| Below 80% | Stronger borrower equity |
| 80%–90% | Moderate equity position |
| Above 90% | Higher lending risk |
| Above 95% | Very high lending risk |

A higher LTV indicates that the borrower contributes less equity relative to the property value.

---

## Debt-to-Income Ratio — DTI

The Debt-to-Income Ratio measures how much of the applicant's income is used for debt obligations.

General interpretation:

| DTI | General Interpretation |
|---:|---|
| Below 30% | Lower debt burden |
| 30%–43% | Moderate debt burden |
| 43%–50% | Elevated affordability concern |
| Above 50% | High financial risk |

A high DTI may indicate reduced repayment capacity.

---

#  Applicant Information

The application accepts the following applicant attributes:

- Age Group
- Sex
- Race
- Ethnicity

These variables are part of the HMDA dataset and were included in the academic modeling process.

They are also examined through fairness analysis to evaluate whether the model behaves differently across demographic groups.

---

#  Demonstration 1 — Stronger Financial Profile

Use the following values to demonstrate a profile that is generally expected to show stronger approval potential:

| Field | Example Value |
|---|---:|
| Loan Amount | 250000 |
| Annual Income | 120000 |
| Property Value | 350000 |
| Interest Rate | 4.2 |
| Loan Term | 360 months |
| LTV | 71 |
| DTI | 25 |
| Applicant Age | 35–44 |
| Sex | Male |
| Race | White |
| Ethnicity | Not Hispanic or Latino |

Possible result:

```text
Likely Approved
```

The exact result may vary according to the trained Machine Learning model.

---

#  Demonstration 2 — Elevated Financial Risk

Use the following values to demonstrate a high-risk profile:

| Field | Example Value |
|---|---:|
| Loan Amount | 900000 |
| Annual Income | 15000 |
| Property Value | 910000 |
| Interest Rate | 12 |
| Loan Term | 360 months |
| LTV | 99 |
| DTI | 65 |
| Applicant Age | <25 |
| Sex | Male |
| Race | Race Not Available |
| Ethnicity | Hispanic or Latino |

Expected result:

```text
Elevated Decline Risk
```

This profile contains several strong risk signals:

- Very high LTV.
- Very high DTI.
- Extremely high payment burden relative to income.
- High interest rate.
- Low annual income relative to the requested loan.

---

#  Understanding the Results Dashboard

After submitting the form, NOVA opens a complete results dashboard.

## Predicted Decision

The principal estimated outcome.

Possible outputs include:

- **Likely Approved**
- **Approval Possible — Further Review Recommended**
- **Approval Possible — Financial Risk Detected**
- **Elevated Decline Risk**

These messages combine the Machine Learning prediction with financial affordability indicators.

---

## Approval Probability

The estimated probability that the mortgage application will be approved.

Example:

```text
Approval Probability: 82%
```

This means the model estimates an 82% probability of approval based on patterns learned from the training data.

It does not guarantee approval.

---

## Decline Probability

The estimated probability that the mortgage application will be denied.

Example:

```text
Decline Probability: 18%
```

Approval and decline probabilities should approximately sum to 100%.

---

## Risk Level

The application translates the estimated decline risk into an interpretable category:

- Low
- Moderate
- High
- Very High

The risk level summarizes the level of lending concern associated with the current application.

---

#  NOVA Financial Health Score

The Financial Health Score summarizes the overall financial condition of the mortgage profile.

The score ranges from:

```text
0 to 100
```

A higher score indicates a stronger financial profile.

A lower score indicates increased affordability or lending-risk concerns.

## Score Components

The score combines:

| Component | Meaning |
|---|---|
| Approval Strength | Strength of the model's approval signal |
| Debt Management | Applicant's DTI position |
| Equity Position | Applicant's LTV and property-equity position |
| Mortgage Affordability | Estimated payment burden |
| Income Capacity | Ability to support the requested mortgage |

The Financial Health Score is a complementary analytical indicator. It is not an official bank credit score.

---

#  Mortgage Summary

## Estimated Monthly Payment

NOVA calculates the estimated monthly principal-and-interest payment using:

- Loan amount
- Interest rate
- Loan term

The estimate does not necessarily include:

- Property taxes
- Insurance
- Legal fees
- Maintenance expenses
- Other lender charges

---

## Total Estimated Interest

The estimated interest paid over the entire mortgage term.

A longer term or higher interest rate generally increases the total interest.

---

## Total Estimated Repayment

The estimated total amount paid during the full mortgage period:

```text
Principal + Interest
```

---

## Payment-to-Income Ratio

The percentage of monthly income required for the estimated mortgage payment.

General interpretation:

| Payment-to-Income | Interpretation |
|---:|---|
| Below 30% | Generally more affordable |
| 30%–40% | Moderate burden |
| 40%–50% | Elevated burden |
| Above 50% | Significant affordability concern |

---

#  Detailed Analysis

The Detailed Analysis page expands the prediction into a more interpretable financial assessment.

It may present:

- Positive financial indicators.
- Areas requiring attention.
- Affordability concerns.
- Equity position.
- Debt burden.
- Banking-oriented conclusions.
- Potential risk-reduction actions.

The purpose is to explain the model output rather than present only a binary decision.

---

#  Mortgage Simulator

The simulator allows the user to explore how changes in the mortgage profile may affect affordability.

Examples of variables that may be adjusted:

- Loan amount
- Interest rate
- Loan term
- Property value
- Income

The simulator can help answer questions such as:

- How would a lower interest rate affect the monthly payment?
- How would a larger down payment reduce the LTV?
- How would a shorter loan term affect total interest?
- How much income would improve affordability?

Simulation outputs are analytical estimates and do not guarantee a different lender decision.

---

#  Financial Advisor

The advisor page provides structured, banking-oriented observations based on the application profile.

Possible recommendations may include:

- Reducing the requested loan amount.
- Increasing the down payment.
- Reducing existing debt.
- Improving the DTI ratio.
- Selecting a longer or shorter loan term.
- Reviewing affordability before formal submission.

These recommendations are educational and analytical.

---

#  Model Performance

The Model Performance page presents the scientific evaluation of the final model.

## Accuracy

The percentage of all testing observations classified correctly.

---

## Precision — Denied

Among applications predicted as denied, the proportion that were actually denied.

High denied-class Precision means the model produces relatively few incorrect decline predictions.

---

## Recall — Denied

Among applications that were actually denied, the proportion detected correctly by the model.

This is particularly important because denied applications represent the more difficult and financially sensitive class.

---

## F1-Score — Denied

A combined measure balancing denied-class Precision and Recall.

A high F1-Score indicates that the model maintains a strong balance between identifying denied applications and avoiding incorrect decline predictions.

---

## ROC-AUC

Measures the ability of the model to distinguish between approved and denied applications across different probability thresholds.

Interpretation:

| ROC-AUC | General Interpretation |
|---:|---|
| 0.50 | No discrimination |
| 0.60–0.70 | Limited |
| 0.70–0.80 | Acceptable |
| 0.80–0.90 | Strong |
| Above 0.90 | Excellent |

---

## Confusion Matrix

The confusion matrix presents:

| Outcome | Meaning |
|---|---|
| True Denied | Correctly identified denial |
| True Approved | Correctly identified approval |
| False Approved | Denied case predicted as approved |
| False Denied | Approved case predicted as denied |

This visualization provides a clearer understanding of the model's errors.

---

## Model Comparison

The application compares:

- Logistic Regression
- Original Random Forest
- Tuned Random Forest

Logistic Regression serves as a baseline model.

Random Forest was selected as the final model after demonstrating stronger overall predictive performance.

---

## Feature Importance

The Feature Importance chart presents the variables with the strongest predictive influence.

Examples may include:

- Interest Rate
- Debt-to-Income Ratio
- Loan Amount
- Annual Income
- Loan-to-Value Ratio
- Property Value

Feature Importance indicates predictive contribution.

It does not prove that a variable directly causes approval or denial.

---

#  Model Feedback

The Model Feedback page supports a controlled human-in-the-loop learning workflow.

## When to Submit Feedback

Feedback should be submitted only when the true mortgage outcome is known and verified.

Examples:

```text
Predicted: Approved
Actual Outcome: Denied
```

or:

```text
Predicted: Denied
Actual Outcome: Denied
```

---

## How to Submit Feedback

1. Complete a mortgage analysis.
2. Open **Model Feedback**.
3. Review the current prediction.
4. Select the verified actual outcome:
   - Approved
   - Denied
5. Confirm that the outcome is verified.
6. Add an optional reviewer note.
7. Select **Submit Verified Feedback**.

---

## Information Stored

The feedback record may contain:

- Original application inputs.
- Model prediction.
- Approval probability.
- Decline probability.
- Verified actual outcome.
- Whether the prediction was correct.
- Risk level.
- Reviewer note.
- Submission timestamp.

---

## Feedback Monitoring

The feedback dashboard displays:

- Total feedback observations.
- Verified outcomes.
- Correct predictions.
- Prediction errors.
- Feedback accuracy.
- Actual approval and denial distribution.
- Recent feedback records.

The feedback dataset can also be downloaded as a CSV file.

---

#  Controlled Model Retraining

NOVA does not automatically retrain the production model after every user submission.

The controlled retraining process is:

```text
Verified Outcome
        ↓
Feedback Collection
        ↓
Quality Review
        ↓
Combine with Original Training Data
        ↓
Train Candidate Model
        ↓
Evaluate on Held-Out Data
        ↓
Deploy Only If Performance Improves
```

This approach helps reduce:

- Incorrect labels
- Data poisoning
- Unstable retraining
- Model degradation
- Accidental replacement of a stronger model

A new production model should be deployed only after formal evaluation.

---

#  PDF Report

The application can generate a structured PDF report.

The report may include:

- Predicted mortgage outcome.
- Approval probability.
- Decline probability.
- Risk classification.
- Financial Health Score.
- Estimated monthly payment.
- Total interest.
- Total repayment.
- Affordability indicators.
- Key conclusions.

The PDF provides a convenient summary for academic demonstrations, documentation, or analysis review.

---

#  Responsible Use

NOVA should be used responsibly.

The application:

- Does not represent an official lender.
- Does not issue binding credit decisions.
- Does not replace human underwriting.
- Does not include every variable used by financial institutions.
- Is trained on historical data.
- May inherit patterns or limitations from the training dataset.
- Should not be used as the only basis for financial decisions.

Human review remains essential.

---

#  Important Limitations

- Historical HMDA data may not fully represent future lending conditions.
- Model probability does not guarantee an outcome.
- Demographic variables require careful fairness evaluation.
- Feature Importance is not causal evidence.
- Financial calculations are estimates.
- Streamlit Community Cloud may temporarily place inactive applications into sleep mode.
- Local feedback storage may be temporary in the cloud environment.
- A production implementation should use persistent database storage.

---

#  Troubleshooting

## The Application Opens Slowly

The cloud application may be waking from sleep mode.

Wait briefly and refresh the page.

---

## The Application Does Not Load

Check:

- Internet connection.
- Streamlit deployment status.
- GitHub repository availability.
- Application logs.

---

## Model Files Are Missing

Verify that the following files exist in the main project folder:

```text
mortgage_pipeline.pkl
model_columns.pkl
```

---

## A Python Package Is Missing

Install all project dependencies:

```bash
pip install -r requirements.txt
```

---

## The Application Displays Old Results

Restart the Streamlit application or use:

```text
Manage App → Reboot App
```

---

## Feedback Disappears After a Cloud Restart

Streamlit Community Cloud may use temporary local storage.

For a production application, feedback should be stored in:

- PostgreSQL
- MySQL
- Firebase
- Supabase
- Cloud storage
- Another persistent database system

---

#  Local Installation

## 1. Clone the Repository

```bash
git clone https://github.com/samaandrea10/mortgag-dashboard.git
```

## 2. Open the Project Folder

```bash
cd mortgag-dashboard
```

## 3. Create a Virtual Environment

```bash
py -3.12 -m venv .venv
```

## 4. Activate the Environment on Windows

```bash
.\.venv\Scripts\Activate.ps1
```

## 5. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

## 6. Run the Application

```bash
python -m streamlit run app.py
```

---

# 📁 Main Project Files

```text
mortgag-dashboard/
│
├── app.py
├── README.md
├── USER_GUIDE.md
├── requirements.txt
├── mortgage_pipeline.pkl
├── model_columns.pkl
│
├── pages/
│   ├── home.py
│   ├── approval.py
│   ├── results.py
│   ├── detailed_analysis.py
│   ├── simulator.py
│   ├── advisor.py
│   ├── model_performance.py
│   └── model_feedback.py
│
├── utils/
│   ├── prediction.py
│   ├── financial_health.py
│   ├── feedback.py
│   ├── pdf_report.py
│   ├── session.py
│   └── styles.py
│
└── components/
    └── logo.py
```

---

# 🔗 Project Links

## Live Application

[https://mortgage-dashboard-sama.streamlit.app/](https://mortgage-dashboard-sama.streamlit.app/)

## GitHub Repository

[https://github.com/samaandrea10/mortgag-dashboard](https://github.com/samaandrea10/mortgag-dashboard)

---

# 🎓 Academic Context

NOVA Mortgage Intelligence was developed as a final Data Science capstone project.

The project demonstrates the integration of:

- Data preprocessing
- Exploratory Data Analysis
- Machine Learning
- Model comparison
- Hyperparameter optimization
- Performance evaluation
- Fairness analysis
- Financial analytics
- Interactive visualization
- Web deployment
- PDF reporting
- Human-in-the-loop feedback
- Controlled model retraining

---

#  Author

**Sama Andrea**

B.Sc. Information Systems  
Data Science Specialization  
Final Capstone Project

---

#  Final Notice

NOVA Mortgage Intelligence is an academic analytical platform.

All predictions, financial scores, simulations, and recommendations should be interpreted as educational decision-support outputs and not as official banking decisions.
