#  Mortgage Approval Prediction System

[![Live Application](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mortgage-dashboard-sama.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)]
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.6.1-orange?style=for-the-badge&logo=scikitlearn)]
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?style=for-the-badge&logo=streamlit)]

## Live Application

https://mortgage-dashboard-sama.streamlit.app/
---

##  User Guide

For complete instructions, examples, result interpretation, model feedback, and troubleshooting:

### [Open the NOVA User Guide](USER_GUIDE.md)



# Executive Summary

Mortgage lending represents one of the most critical financial decision-making processes within the banking industry. Evaluating a mortgage application requires the simultaneous analysis of numerous financial and demographic factors while balancing lending risk with responsible credit allocation.

This project presents a complete end-to-end Machine Learning solution for predicting mortgage approval decisions using the Home Mortgage Disclosure Act (HMDA) dataset. The system integrates data preprocessing, feature engineering, predictive modeling, financial risk assessment, and an interactive web application developed with Streamlit.

Unlike a traditional classification model, this application combines predictive analytics with financial indicators to provide a comprehensive decision-support environment. Users receive not only an approval prediction but also an affordability analysis, monthly payment estimation, financial health indicators, and an automatically generated PDF report.

The project demonstrates the complete lifecycle of a modern Data Science application, from raw data acquisition through deployment in a production-ready environment.

---

# Project Objectives

The primary objectives of this project are:

- Develop a reliable Machine Learning model capable of predicting mortgage approval outcomes.
- Analyze how financial and demographic variables influence lending decisions.
- Build an interactive decision-support application using Streamlit.
- Demonstrate an end-to-end Data Science workflow following industry best practices.
- Provide an intuitive interface suitable for both technical and non-technical users.

---

# Dataset

The predictive model was trained using the publicly available Home Mortgage Disclosure Act (HMDA) dataset.

The dataset contains thousands of real mortgage applications and includes variables related to borrower characteristics, loan attributes, and lending decisions.

Examples of input variables include:

- Annual Income
- Loan Amount
- Interest Rate
- Property Value
- Loan-to-Value Ratio (LTV)
- Debt-to-Income Ratio (DTI)
- Loan Term
- Applicant Age
- Race
- Sex
- Ethnicity

---

# Machine Learning Pipeline

The complete workflow consists of the following stages:

1. Data Cleaning
2. Missing Value Imputation
3. Feature Engineering
4. Numerical Transformation
5. Categorical Encoding
6. Model Training
7. Hyperparameter Optimization
8. Prediction Generation
9. Financial Risk Assessment
10. Interactive Deployment

---

# Model

The predictive engine is based on a Random Forest Classifier implemented through a Scikit-Learn Pipeline.

The pipeline performs all preprocessing automatically before generating predictions, ensuring consistency between training and inference.

Model capabilities include:

- Mortgage Approval Prediction
- Approval Probability Estimation
- Financial Risk Classification
- Real-Time Prediction
- Automated Feature Processing

---

# Dashboard Features

The Streamlit dashboard provides:

- Mortgage Approval Prediction
- Financial Health Assessment
- Monthly Mortgage Payment Estimation
- Loan Affordability Analysis
- Debt-to-Income Evaluation
- Loan-to-Value Assessment
- Interactive User Interface
- Automatic PDF Report Generation

---

# Technologies

Programming Language

- Python 3.12

Libraries

- Pandas
- NumPy
- Scikit-Learn
- Joblib
- Streamlit
- Plotly
- ReportLab

Development Environment

- Visual Studio Code
- Git
- GitHub
- Streamlit Community Cloud

---

# Project Structure

```
mortgage_dashboard/
│
├── app.py
├── mortgage_pipeline.pkl
├── model_columns.pkl
├── requirements.txt
├── README.md
│
├── components/
├── pages/
├── utils/
└── assets/
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/samaandrea10/mortgag-dashboard.git
```

Navigate into the project

```bash
cd mortgag-dashboard
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# Live Demonstration

The deployed application is available online:

https://mortgage-dashboard-sama.streamlit.app/

---

# Academic Contribution

This project demonstrates the practical application of modern Machine Learning techniques within the financial services domain.

It combines predictive analytics, feature engineering, statistical preprocessing, supervised learning, interactive visualization, and cloud deployment into a unified decision-support system.

The implementation follows established Data Science practices while emphasizing reproducibility, usability, and deployment readiness.

---

# Author

**Sama Andrea**

Fathe abu hussien

B.Sc. Information Systems

Specialization in Data Science

Final Capstone Project

---

# License

This repository was developed for academic and educational purposes.
