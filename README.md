# NOVA Mortgage Intelligence

### End-to-End Machine Learning Dashboard for Mortgage Approval Prediction

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine%20Learning-orange?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-blue?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![GitHub](https://img.shields.io/badge/GitHub-Version%20Control-black?logo=github&logoColor=white)](https://github.com/)

---

# Live Application

**NOVA Mortgage Intelligence**

[https://mortgage-dashboard-sama.streamlit.app/](https://mortgage-dashboard-sama.streamlit.app/)

---

## User Guide

A comprehensive user guide describing the complete workflow of the NOVA platform—including application navigation, mortgage prediction, model performance interpretation, data insights, verified outcome feedback, PDF report generation, and troubleshooting—is available below.

## **[Open the NOVA User Guide](USER_GUIDE.md)**

# Executive Summary

NOVA Mortgage Intelligence is a comprehensive end-to-end Machine Learning decision-support platform developed for mortgage approval prediction using the Home Mortgage Disclosure Act (HMDA) dataset. The project demonstrates the complete lifecycle of a modern Data Science solution, integrating data acquisition, preprocessing, exploratory data analysis, feature engineering, predictive modeling, model evaluation, cross-validation, hyperparameter tuning, fairness assessment, external validation, interactive visualization, and cloud deployment within a unified analytical environment.

Unlike traditional classification systems that provide only a binary prediction, NOVA combines predictive analytics with financial decision support by integrating mortgage approval probability estimation, affordability analysis, financial health assessment, risk evaluation, model performance monitoring, interactive data exploration, verified outcome feedback collection, and automated professional reporting. The platform was designed to provide both technical and non-technical users with an intuitive interface while preserving methodological rigor, model transparency, and reproducibility throughout the analytical workflow.

---

# Project Objectives

The primary objectives of NOVA Mortgage Intelligence are:

- Develop a robust Machine Learning model for mortgage approval prediction.
- Identify the financial variables that most influence lending decisions.
- Evaluate predictive performance using multiple statistical metrics.
- Compare alternative Machine Learning algorithms.
- Assess model stability using Cross Validation.
- Improve model performance through Hyperparameter Tuning.
- Evaluate model generalization using External Validation.
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

Missing numerical values were handled using **Median Imputation**, while missing categorical values were represented using an **"Unknown"** category as part of the preprocessing pipeline.

### Target Variable

| Value | Interpretation    |
| ----- | ----------------- |
| 1     | Mortgage Approved |
| 0     | Mortgage Denied   |

---

# Machine Learning Pipeline

The complete analytical workflow consists of the following stages:

1. Data Cleaning
2. Missing Value Imputation
3. Exploratory Data Analysis (EDA)
4. Feature Engineering
5. Numerical Transformation
6. Categorical Encoding
7. Train/Test Split
8. Model Training
9. Model Comparison
10. 5-Fold Cross Validation
11. Hyperparameter Tuning using GridSearchCV
12. Final Model Evaluation
13. Feature Importance Analysis
14. Fairness Analysis
15. External Validation
16. Model Performance Monitoring
17. Verified Outcome Feedback Collection
18. Streamlit Deployment

---

# Predictive Model

Multiple supervised Machine Learning algorithms were evaluated throughout the development process.

| Model               | Purpose                       |
| ------------------- | ----------------------------- |
| Logistic Regression | Baseline Classification Model |
| Random Forest       | Final Production Model        |

Following model comparison, **Random Forest** was selected as the most promising model for further development.

The model was subsequently evaluated using **5-Fold Cross Validation** and optimized through **GridSearchCV**, where multiple combinations of key hyperparameters were examined.

The tuning process included:

- `n_estimators`: 50, 100, 200
- `max_depth`: 10, 20, None

Following model comparison, Cross Validation, Hyperparameter Tuning, and final evaluation, the tuned Random Forest classifier demonstrated the strongest overall predictive performance and generalization capability.

Consequently, it was selected as the final production model and deployed within the NOVA platform.

---

# Model Evaluation

Model quality was assessed using a comprehensive collection of Machine Learning performance metrics, including:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Precision–Recall Curve
- Average Precision
- Confusion Matrix

The final Random Forest model achieved the following performance on the Test Set:

| Metric | Score |
| ------ | ----: |
| Accuracy | **0.9678** |
| Precision | **0.9830** |
| Recall | **0.9713** |
| F1-Score | **0.9771** |
| ROC-AUC | **0.9930** |
| Average Precision | **0.9967** |

These results demonstrate strong predictive performance and an excellent ability to distinguish between approved and denied mortgage applications.

---

# 5-Fold Cross Validation

To evaluate model stability and reduce dependence on a single Train/Test split, **5-Fold Cross Validation** was performed on the Random Forest pipeline using the training data.

The Cross Validation results were:

| Fold | Accuracy |
| ---- | -------: |
| Fold 1 | 0.9695 |
| Fold 2 | 0.9722 |
| Fold 3 | 0.9699 |
| Fold 4 | 0.9715 |
| Fold 5 | 0.9699 |

### Cross Validation Summary

- **Mean Accuracy:** **0.9706 (97.06%)**
- **Standard Deviation:** **0.0011**

The consistently high accuracy across all five folds, together with the very low standard deviation, indicates strong model stability and limited sensitivity to individual data partitions.

---

# Hyperparameter Tuning

After the initial model comparison, Random Forest was selected for further optimization.

A **GridSearchCV** procedure was used to evaluate multiple combinations of Random Forest hyperparameters, including:

- `n_estimators`: 50, 100, 200
- `max_depth`: 10, 20, None

This process enabled systematic evaluation of different model configurations.

Following Hyperparameter Tuning and final model evaluation, the tuned Random Forest model was selected as the final model integrated into NOVA.

---

# External Validation

In addition to internal model evaluation, **External Validation** was performed using HMDA data from **2022**.

The purpose of this validation stage was to evaluate the model using data originating from a different reporting year and to examine its ability to generalize beyond the original HMDA 2023 development dataset.

This additional validation provides further evidence regarding the robustness and generalization capability of the final Machine Learning pipeline.

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
- Input Validation
- Model Performance Dashboard
- Interactive Data Insights Dashboard
- Mortgage Scenario Simulator
- AI Mortgage Advisor
- Verified Outcome Feedback System
- Professional PDF Report Generation
- About NOVA Project Documentation

---

# Model Transparency and Fairness

NOVA incorporates additional analytical components beyond traditional predictive performance.

Feature Importance analysis is used to examine the variables that contribute most strongly to Random Forest predictions, supporting greater transparency regarding model behavior.

The project also includes a fairness assessment examining prediction outcomes across demographic groups. This analysis is intended to support responsible Machine Learning practices and identify potential differences in model behavior.

Feature Importance and fairness results should be interpreted as analytical evidence and should not be considered proof of causal relationships.

---

# Model Feedback

NOVA includes a **Verified Outcome Feedback** mechanism that allows verified real-world outcomes to be recorded and compared with previous model predictions.

The feedback mechanism supports model monitoring and provides a foundation for a future controlled retraining process.

The production model is **not automatically retrained after individual user submissions**. Any future retraining process should use verified observations, quality review, formal model evaluation, and controlled deployment before replacing the existing production model.

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

```text
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

NOVA Mortgage Intelligence demonstrates the complete lifecycle of a contemporary Machine Learning application within the financial services domain.

The project integrates data preprocessing, statistical analysis, supervised learning, predictive modeling, feature engineering, model comparison, 5-Fold Cross Validation, Hyperparameter Tuning, model evaluation, Feature Importance, fairness assessment, External Validation, interactive visualization, cloud deployment, performance monitoring, verified feedback collection, and automated reporting into a unified decision-support platform.

The implementation emphasizes methodological rigor, reproducibility, transparency, usability, and responsible deployment while reflecting software engineering and Data Science practices commonly adopted in real-world analytical systems.

---

# Future Improvements

Potential future enhancements include:

- Advanced Explainable Artificial Intelligence using SHAP
- XGBoost and LightGBM model comparison
- Extended Hyperparameter Optimization
- Continuous model monitoring
- Data and concept drift detection
- Controlled retraining using verified user feedback
- Advanced bias detection and mitigation techniques
- Model versioning and automated validation before deployment
- Docker-based cloud deployment
- Integration with secure financial information systems

---

# Author

**Sama Andrea**

**B.Sc. Information Systems**

**Data Science Specialization**

**Final Capstone Project**

---

# License

This repository was developed for academic, educational, and research purposes.
