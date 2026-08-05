# NOVA Mortgage Intelligence

### End-to-End Machine Learning Dashboard for Mortgage Approval Prediction

[![Live Application](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mortgage-dashboard-sama.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)]
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-orange?style=for-the-badge&logo=scikitlearn)]
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?style=for-the-badge&logo=streamlit)]

---

# Live Application

**NOVA Mortgage Intelligence**

https://mortgage-dashboard-sama.streamlit.app/

---

# User Guide

Complete operating instructions, workflow explanations, prediction interpretation, model feedback procedures, and troubleshooting documentation are available in:

**USER_GUIDE.md**

---

# Executive Summary

NOVA Mortgage Intelligence is a comprehensive end-to-end Machine Learning decision-support platform developed for mortgage approval prediction using the Home Mortgage Disclosure Act (HMDA) dataset. The project demonstrates the complete lifecycle of a modern Data Science solution, integrating data acquisition, preprocessing, exploratory data analysis, feature engineering, predictive modeling, model evaluation, fairness assessment, interactive visualization, and cloud deployment within a unified analytical environment.

Unlike traditional classification systems that provide only a binary prediction, NOVA combines predictive analytics with financial decision support by integrating mortgage approval probability estimation, affordability analysis, financial health assessment, risk evaluation, model performance monitoring, interactive data exploration, verified outcome feedback collection, and automated professional reporting. The platform was designed to provide both technical and non-technical users with an intuitive interface while preserving methodological rigor, model transparency, and reproducibility throughout the analytical workflow.

---

# Project Objectives

The primary objectives of NOVA Mortgage Intelligence are:

- Develop a robust Machine Learning model for mortgage approval prediction.
- Identify the financial variables that most influence lending decisions.
- Evaluate predictive performance using multiple statistical metrics.
- Compare alternative Machine Learning algorithms.
- Provide transparent financial risk analysis.
- Deploy the final model through an interactive web application.
- Demonstrate an end-to-end Data Science workflow aligned with industry best practices.

---

# Dataset

The predictive model was developed using the publicly available **Home Mortgage Disclosure Act (HMDA) 2023** dataset.

To facilitate efficient model training, deployment, and repository management, the original dataset underwent extensive preprocessing, including:

- Data cleaning
- Removal of incomplete and irrelevant records
- Missing value handling
- Feature selection
- Feature engineering
- Construction of a representative processed dataset

The processed dataset contains approximately **50,000 mortgage applications** and serves as the analytical foundation of the deployed model.

### Target Variable

| Value | Interpretation |
|--------|----------------|
| 1 | Mortgage Approved |
| 0 | Mortgage Denied |

---

# Machine Learning Pipeline

The complete analytical workflow consists of the following stages:

1. Data Cleaning
2. Missing Value Imputation
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Numerical Transformation
6. Categorical Encoding
7. Model Training
8. Model Comparison
9. Hyperparameter Optimization
10. Model Evaluation
11. Fairness Analysis
12. Model Performance Monitoring
13. Verified Outcome Feedback Collection
14. Streamlit Deployment

---

# Predictive Model

Multiple supervised Machine Learning algorithms were evaluated throughout the development process.

| Model | Purpose |
|--------|---------|
| Logistic Regression | Baseline Classification Model |
| Random Forest | Final Production Model |

The Random Forest classifier achieved the strongest predictive performance and demonstrated superior generalization capability across the evaluation metrics. Consequently, it was selected as the production model and deployed within the NOVA platform.

---

# Model Evaluation

Model quality was assessed using a comprehensive collection of Machine Learning performance metrics, including:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Precision–Recall Curve
- Confusion Matrix

The evaluation process confirmed that the selected model provides a strong balance between predictive accuracy, robustness, and generalization performance.

---

# Dashboard Features

The deployed NOVA platform provides the following capabilities:

- Mortgage Approval Prediction
- Approval Probability Estimation
- Financial Health Assessment
- Mortgage Affordability Analysis
- Monthly Payment Estimation
- Debt-to-Income Evaluation
- Loan-to-Value Assessment
- Model Performance Dashboard
- Interactive Data Insights Dashboard
- Mortgage Scenario Simulator
- AI Mortgage Advisor
- Verified Outcome Feedback System
- Professional PDF Report Generation
- About NOVA Project Documentation

---

# Technologies

Programming Language

- Python

Core Libraries

- Pandas
- NumPy
- Scikit-Learn
- Matplotlib
- Plotly
- Joblib
- Streamlit
- ReportLab

Development Environment

- Visual Studio Code
- Google Colab
- Git
- GitHub
- Streamlit Community Cloud

---

# Project Structure

```
mortgage_dashboard/

│── app.py
│── mortgage_pipeline.pkl
│── model_columns.pkl
│── hmda_2023_processed.csv
│── requirements.txt
│── README.md
│── USER_GUIDE.md

├── components/
├── pages/
│   ├── home.py
│   ├── approval.py
│   ├── results.py
│   ├── detailed_analysis.py
│   ├── simulator.py
│   ├── advisor.py
│   ├── model_performance.py
│   ├── data_insights.py
│   ├── model_feedback.py
│   └── about.py

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

# Academic Contribution

NOVA Mortgage Intelligence demonstrates the complete lifecycle of a contemporary Machine Learning application within the financial services domain. The project integrates data preprocessing, statistical analysis, supervised learning, predictive modeling, feature engineering, fairness evaluation, interactive visualization, cloud deployment, performance monitoring, verified feedback collection, and automated reporting into a unified decision-support platform. The implementation emphasizes methodological rigor, reproducibility, transparency, usability, and responsible deployment while reflecting software engineering and Data Science practices commonly adopted in real-world analytical systems.

---

# Future Improvements

Potential future enhancements include:

- Explainable Artificial Intelligence (SHAP)
- XGBoost and LightGBM model comparison
- Automated hyperparameter optimization
- Continuous retraining using verified user feedback
- Bias mitigation techniques
- Docker-based cloud deployment
- Continuous model monitoring

---

# Author

**Sama Andrea**

**B.Sc. Information Systems**

**Data Science Specialization**

**Final Capstone Project**

---

# License

This repository was developed for academic, educational, and research purposes.
