# NOVA Mortgage Intelligence

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
- Examine the variables that have relatively high importance in the model's predictions.
- Record verified actual outcomes for controlled model monitoring.
- Generate a downloadable PDF analysis report.

> **Important:** NOVA is an academic decision-support system.  
> It does not replace formal lender underwriting, legal advice, or an official credit decision.

---

# Access the Application

## Live Application

### [Launch NOVA Mortgage Intelligence](https://mortgage-dashboard-sama.streamlit.app/)

The application runs directly in a web browser and does not require local installation.

The first opening may take slightly longer because Streamlit Community Cloud may need to wake the application and load the Machine Learning model.

---

# Quick Start

A complete mortgage analysis can be performed in five steps:

1. Open the live application.
2. Select **Analyze Application**.
3. Enter the financial and applicant information.
4. Select **Analyze Mortgage Application**.
5. Review the prediction, probabilities, risk indicators, financial analysis, and recommendations.

---

# Application Navigation

The NOVA home page provides access to five central areas:

| Section | Purpose |
|---|---|
| **Mortgage Analysis** | Enter a new mortgage application and receive a complete prediction. |
| **Model Performance** | Review the scientific evaluation of the final Machine Learning model. |
| **Data Insights** | Explore interactive patterns and distributions in the processed HMDA dataset. |
| **Model Feedback** | Record a verified real-world outcome for monitoring and controlled future retraining. |
| **About NOVA** | Review the project objective, architecture, technologies, capabilities, and limitations. |

After a mortgage application is analyzed, the user can also access:

- Results Dashboard
- Detailed Analysis
- Mortgage Simulator
- Financial Advisor
- Verified Outcome Feedback
- PDF Report

---

# Mortgage Analysis

## Step 1 — Open the Analysis Form

From the home page, select:

```text
Analyze Application
```

The application form contains two sections:

1. Financial Information
2. Applicant Information

---

# Financial Information

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

# Applicant Information

The application accepts the following applicant attributes:

- Age Group
- Sex
- Race
- Ethnicity

These variables are part of the HMDA dataset and were included in the academic modeling process.

These variables are also examined as part of a **preliminary fairness analysis** to identify potential differences in model outcomes across demographic groups.

---

# Demonstration 1 — Stronger Financial Profile

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

# Demonstration 2 — Elevated Financial Risk

Use the following values to demonstrate a profile with elevated financial-risk indicators:

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

Possible result:

```text
Elevated Decline Risk
```

This profile contains several financial-risk indicators:

- Very high LTV.
- Very high DTI.
- High estimated payment burden relative to income.
- High interest rate.
- Low annual income relative to the requested loan.

The exact result depends on the trained Machine Learning model and should be interpreted as a model-based prediction rather than an official lending decision.

---

# Understanding the Results Dashboard

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

# NOVA Financial Health Score

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

# Mortgage Summary

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

# Detailed Analysis

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

# Mortgage Simulator

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

# Financial Advisor

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

# Data Insights

The Data Insights page provides interactive exploratory analysis of the processed 2023 HMDA dataset.

Users can:

- Filter applications by mortgage decision, applicant age, and applicant sex.
- Review the total number of applications, approvals, denials, and approval rate.
- Examine median income, loan amount, and interest rate.
- Compare approval patterns across age, sex, race, and ethnicity.
- Explore distributions of income, loan amount, interest rate, LTV, DTI, and property value.
- Review aggregated approval summaries by selected demographic categories.

The displayed results are descriptive and reflect historical patterns in the processed dataset. They should not be interpreted as proof of causality or discrimination.

---

# About NOVA

The About NOVA page summarizes the academic and technical context of the project.

It presents:

- The project objective.
- The HMDA 2023 dataset.
- The selected tuned Random Forest model.
- The Machine Learning lifecycle.
- The platform architecture.
- The technology stack.
- Core analytical capabilities.
- Responsible-use principles and project limitations.
- Links to the live application and GitHub repository.

This page provides a concise overview of how the project combines Data Science, Machine Learning, software engineering, deployment, monitoring, and user interaction.

---

# Model Performance

The Model Performance page presents the scientific evaluation of the final **Tuned Random Forest** model.

The final model was selected after model comparison, **5-Fold Cross Validation**, Hyperparameter Tuning using **RandomizedSearchCV**, and final evaluation on the held-out Test Set.

## Final Model Performance

| Metric | Score |
|---|---:|
| Accuracy | **0.9708 (97.08%)** |
| Precision – Approved | **0.9854** |
| Recall – Approved | **0.9731** |
| F1-Score – Approved | **0.9792** |
| Precision – Denied | **0.9369** |
| Recall – Denied | **0.9651** |
| F1-Score – Denied | **0.9508** |
| ROC-AUC | **0.9950** |

These results indicate strong predictive performance and excellent ability to distinguish between approved and denied mortgage applications.

---

## Cross Validation

A **5-Fold Cross Validation** procedure was used to evaluate model stability.

- **Mean Accuracy:** 96.97%
- **Standard Deviation:** 0.0013

The low variation between folds indicates stable performance across different data partitions.

---

## Hyperparameter Tuning

Hyperparameter Tuning was performed using **RandomizedSearchCV** to efficiently evaluate multiple Random Forest configurations.

The optimized model was selected as the final production model deployed within NOVA.

---

## Model Comparison

The project compared:

- Logistic Regression
- Original Random Forest
- Tuned Random Forest

The **Tuned Random Forest achieved the strongest overall balance of predictive performance and was selected as the final production model deployed within NOVA.**

---

## Feature Importance

The Feature Importance chart highlights variables that have relatively high importance in the model's predictions, including:

- Interest Rate
- Debt-to-Income Ratio
- Loan Amount
- Annual Income
- Loan-to-Value Ratio
- Property Value

Feature Importance helps us understand which variables the Random Forest relies on more heavily when generating predictions.

However, Feature Importance represents predictive contribution and does not establish causation. A feature with high importance should not be interpreted as directly causing a mortgage application to be approved or denied.

---

# Model Feedback

The Model Feedback page enables the recording of a verified real-world mortgage outcome after the actual decision becomes known.

The user can:

1. Select the verified actual outcome.
2. Add an optional note.
3. Submit the feedback.
4. Compare the verified outcome with the previous model prediction.

The feedback record may include:

- Timestamp.
- Predicted class.
- Predicted probability.
- Actual verified outcome.
- Whether the prediction was correct.
- Relevant application characteristics.

The purpose of this feature is to support model monitoring and provide a structured foundation for future controlled retraining.

---

# Controlled Model Retraining

NOVA does **not** automatically retrain the production model after every feedback submission.

This is intentional.

Automatic retraining based on individual observations may introduce:

- Noise.
- Incorrect labels.
- Bias.
- Model instability.
- Performance degradation.

A safer Machine Learning lifecycle is:

```text
Prediction
   ↓
Verified Outcome
   ↓
Feedback Storage
   ↓
Quality Review
   ↓
Batch Accumulation
   ↓
Controlled Retraining
   ↓
Validation
   ↓
Production Deployment
```

Future retraining should occur only after sufficient verified observations have been collected and the updated model has passed formal evaluation.

---

# PDF Report

NOVA can generate a professional PDF report summarizing the mortgage analysis.

The report may include:

- Predicted decision.
- Approval and decline probabilities.
- Risk level.
- Financial Health Score.
- Mortgage summary.
- Applicant information.
- Financial ratios.
- Estimated monthly payment.
- Total estimated interest.
- Affordability indicators.
- Risk observations.
- Recommendations.
- Model explanation.
- Responsible-use disclaimer.

The report is generated dynamically using the current application data.

---

# Responsible Use

NOVA is designed for educational and academic decision support.

The system should **not** be used as the sole basis for a real mortgage decision.

Real-world mortgage underwriting may require additional information such as:

- Credit history.
- Employment verification.
- Assets.
- Existing liabilities.
- Property appraisal.
- Regulatory requirements.
- Documentation verification.
- Lender-specific policies.

The system therefore provides analytical support rather than an official lending decision.

---

# Troubleshooting

## Application Is Loading Slowly

Streamlit Community Cloud may place inactive applications into a sleep state.

Wait briefly and refresh the page.

---

## Prediction Does Not Appear

Check that all required fields contain valid values.

Pay particular attention to:

- Loan amount.
- Income.
- Property value.
- Interest rate.
- DTI.
- LTV.

---

## Input Validation Warning Appears

NOVA validates financial inputs before prediction.

If an unrealistic or invalid value is entered, the application may display a warning or prevent the analysis from continuing.

Correct the highlighted value and submit the application again.

---

## PDF Report Does Not Download

Make sure a mortgage analysis has already been completed.

The PDF report is generated from the current prediction and financial-analysis data.

---

## Feedback Cannot Be Submitted

A prediction must exist before a verified outcome can be associated with it.

Complete a mortgage analysis first, then open the Model Feedback page.

---

# Local Installation

The project can also be executed locally.

## Clone the Repository

```bash
git clone https://github.com/samaandrea10/mortgag-dashboard.git
```

## Navigate to the Project

```bash
cd mortgag-dashboard
```

## Create a Virtual Environment

```bash
python -m venv .venv
```

## Activate the Environment

### Windows

```bash
.venv\Scripts\activate
```

### macOS / Linux

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run NOVA

```bash
streamlit run app.py
```

The application should open in the default browser.

---

# Project Files

Important files may include:

```text
app.py
mortgage_pipeline.pkl
model_columns.pkl
hmda_2023_processed.csv
requirements.txt
README.md
USER_GUIDE.md

components/
pages/
utils/
assets/
```

The exact repository structure may evolve as the project is improved.

---

# Technologies

NOVA was developed using:

- Python
- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Plotly
- Joblib
- Streamlit
- ReportLab
- Google Colab
- Visual Studio Code
- Git
- GitHub
- Streamlit Community Cloud

---

# Academic Context

NOVA Mortgage Intelligence was developed as a **Final Capstone Project in Information Systems with a Data Science specialization**.

The project demonstrates the complete lifecycle of a modern Machine Learning system:

```text
Data
  ↓
Preprocessing
  ↓
Exploratory Data Analysis
  ↓
Feature Engineering
  ↓
Model Development
  ↓
Model Comparison
  ↓
5-Fold Cross Validation
  ↓
RandomizedSearchCV Hyperparameter Tuning
  ↓
Final Model Evaluation
  ↓
Fairness Analysis
  ↓
External Validation
  ↓
Deployment
  ↓
Monitoring
  ↓
Verified Feedback
```

The project integrates Data Science, Machine Learning, software engineering, interactive visualization, model monitoring, and responsible deployment within a unified decision-support platform.

---

# Important Notice

NOVA is an academic and educational project.

Predictions generated by the system should not be interpreted as financial advice or as a replacement for professional lending decisions.

Real-world mortgage approval requires additional regulatory, legal, financial, and risk-assessment considerations beyond the scope of this academic project.

---

# Author

**Sama Andrea**

**B.Sc. Information Systems**

**Data Science Specialization**

**Final  Project**

---

# NOVA Mortgage Intelligence

### From Data to Decisions You Can Trust
