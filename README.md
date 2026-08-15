# NOVA Mortgage Intelligence

### End-to-End Machine Learning Decision-Support Platform for Mortgage Approval Prediction

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

A comprehensive user guide describing the complete workflow of the NOVA platform—including application navigation, mortgage prediction, model-performance interpretation, data insights, verified outcome feedback, PDF report generation, and troubleshooting—is available below.

## **[Open the NOVA User Guide](USER_GUIDE.md)**

---

# Executive Summary

**NOVA Mortgage Intelligence** is an end-to-end Machine Learning decision-support platform developed for mortgage approval prediction using the **Home Mortgage Disclosure Act (HMDA)** dataset.

The project demonstrates the complete lifecycle of a Data Science solution, including data preparation, exploratory data analysis, preprocessing, feature engineering, predictive modeling, model comparison, model evaluation, Cross Validation, Hyperparameter Tuning, Feature Importance analysis, preliminary fairness analysis, External Validation, interactive visualization, and cloud deployment.

NOVA goes beyond providing only an Approved or Denied prediction. The platform combines predictive analytics with supporting financial indicators and interactive tools, including approval-probability estimation, affordability analysis, financial-health indicators, mortgage scenario simulation, model-performance visualization, interactive data exploration, verified outcome feedback, and automated PDF reporting.

The platform was developed to make the final Machine Learning model accessible to both technical and non-technical users through an intuitive Streamlit interface while maintaining consistency between the preprocessing used during model development and the preprocessing applied to new observations.

> **NOVA does not approve or reject mortgage applications and does not replace the decision-making process of a financial institution.**
>
> NOVA provides a model-based prediction derived from patterns learned from historical HMDA data and is intended to serve as a decision-support and academic analytical system.

---

# Project Objectives

The primary objectives of NOVA Mortgage Intelligence are:

- Develop a robust Machine Learning model for mortgage approval prediction.
- Compare alternative supervised Machine Learning algorithms.
- Evaluate model performance using multiple statistical and classification metrics.
- Assess model stability using 5-Fold Cross Validation.
- Improve model performance through Hyperparameter Tuning.
- Identify the variables that contribute most strongly to the model's predictions.
- Examine potential differences in outcomes across demographic groups through preliminary fairness analysis.
- Evaluate model generalization using External Validation.
- Deploy the final model through an interactive web application.
- Transform a Data Science model from a research-oriented Notebook into an accessible decision-support system.
- Demonstrate a complete end-to-end Data Science workflow.

---

# Dataset

The predictive model was developed using the publicly available **Home Mortgage Disclosure Act (HMDA) 2023** dataset.

The original HMDA dataset contains a large number of mortgage applications and variables. To support efficient model development, deployment, and repository management, the data underwent preprocessing that included:

- Data understanding
- Data cleaning
- Removal of incomplete and irrelevant records
- Missing-value analysis
- Missing-value handling
- Target definition
- Feature selection
- Feature preparation
- Construction of a representative processed dataset

The processed dataset contains approximately **50,000 mortgage applications** and serves as the analytical foundation of the deployed model.

Missing numerical values were handled using **Median Imputation**, while missing categorical values were represented using an **"Unknown"** category as part of the preprocessing workflow.

---

## Target Variable

The project was formulated as a **Binary Classification** problem.

The original mortgage outcome information was used to construct the target variable:

| Value | Interpretation |
|------:|----------------|
| 1 | Mortgage Approved |
| 0 | Mortgage Denied |

The objective of the predictive model is therefore to learn patterns from historical mortgage-application characteristics and predict whether a new application is expected to belong to the Approved or Denied class.

---

# Selected Model Features

A focused set of financial, loan-related, and applicant characteristics was selected for model development.

## Numerical Features

- `loan_amount`
- `income`
- `interest_rate`
- `loan_to_value_ratio`
- `debt_to_income_ratio`
- `property_value`
- `loan_term`

## Categorical Features

- `applicant_age`
- `derived_race`
- `derived_sex`
- `derived_ethnicity`

These features were selected to represent relevant characteristics of the mortgage application, the financial profile, and the applicant.

The project avoids using variables that directly reveal the target outcome in order to reduce the risk of **Data Leakage**.

---

# Data Understanding

Before model development, the dataset was explored to understand its structure, quality, variable types, missing values, and target distribution.

Typical exploratory checks included:

```python
df.head()
df.shape
df.info()
df.describe()
df.isnull().sum()
df["action_taken"].value_counts()
```

These checks helped answer several important questions:

- How many observations and variables are available?
- What type of data is stored in each column?
- Which variables contain missing values?
- How are numerical variables distributed?
- Are there unusually large or small values?
- How are mortgage outcomes distributed?
- Is there an imbalance between Approved and Denied applications?

This stage provided the foundation for the preprocessing decisions used later in the project.

---

# Data Preparation and Preprocessing

The preprocessing workflow prepares raw observations for Machine Learning in a consistent and reproducible way.

The main preprocessing operations included:

- Missing-value handling
- Numerical imputation
- Categorical missing-value handling
- Numerical transformation
- Categorical encoding
- Consistent feature preparation

## Numerical Variables

Missing numerical values were handled using:

```python
SimpleImputer(strategy="median")
```

Median Imputation was selected because financial variables may contain skewed distributions or extreme values, and the median is generally less sensitive to outliers than the arithmetic mean.

Numerical variables were also transformed using:

```python
StandardScaler()
```

Scaling is especially useful for models such as Logistic Regression, where differences in feature scales can affect model training.

---

## Categorical Variables

Missing categorical values were represented as:

```text
Unknown
```

Categorical variables were transformed using **One-Hot Encoding** so that the Machine Learning algorithms could process them numerically without introducing an artificial numerical order between categories.

Example:

```python
OneHotEncoder(handle_unknown="ignore")
```

Using:

```python
handle_unknown="ignore"
```

allows the preprocessing pipeline to handle previously unseen categories without causing the application to fail.

---

# Preprocessing Pipeline

Numerical and categorical features require different preprocessing operations.

The project therefore uses a structured preprocessing workflow based on:

- `Pipeline`
- `ColumnTransformer`
- `SimpleImputer`
- `StandardScaler`
- `OneHotEncoder`

Conceptually, the preprocessing process can be represented as:

```text
Raw Mortgage Application
          |
          v
   Feature Selection
          |
          v
+-----------------------+
|                       |
v                       v
Numerical Features   Categorical Features
|                       |
Median Imputation    Missing → Unknown
|                       |
Scaling              One-Hot Encoding
|                       |
+-----------+-----------+
            |
            v
      Model-Ready Data
            |
            v
     Machine Learning Model
```

Using a Pipeline ensures that the same preprocessing operations used during model training are also applied consistently to new observations submitted through NOVA.

---

# Machine Learning Workflow

The complete analytical workflow consists of the following stages:

1. Data Understanding
2. Data Cleaning
3. Target Definition
4. Feature Selection
5. Missing-Value Analysis
6. Missing-Value Imputation
7. Exploratory Data Analysis (EDA)
8. Feature Preparation
9. Numerical Transformation
10. Categorical Encoding
11. Train/Test Split
12. Model Training
13. Model Comparison
14. 5-Fold Cross Validation
15. Hyperparameter Tuning using `RandomizedSearchCV`
16. Final Model Evaluation
17. Feature Importance Analysis
18. Preliminary Fairness Analysis
19. External Validation
20. Model Performance Monitoring
21. Verified Outcome Feedback Collection
22. Streamlit Deployment

---

# Train/Test Split

The processed data was divided into:

- **80% Training Set**
- **20% Test Set**

The Training Set is used to train the Machine Learning models.

The Test Set is kept separate from model training and is used to evaluate how well the trained model performs on observations it has not seen during training.

Stratification was used to preserve the relative distribution of Approved and Denied applications in both datasets.

This separation helps provide a more realistic estimate of the model's ability to generalize to new observations.

---

# Predictive Models

Multiple supervised Machine Learning algorithms were evaluated.

| Model | Purpose |
|-------|---------|
| Logistic Regression | Baseline Classification Model |
| Random Forest | Advanced Classification Model |

---

## Logistic Regression

Logistic Regression was used as a **Baseline Model**.

Although the name contains the word "Regression", Logistic Regression is commonly used for binary classification.

The model estimates the probability that an observation belongs to a particular class.

Using a baseline model provides a reference point against which a more advanced model can be compared.

---

## Random Forest

Random Forest is an **Ensemble Learning** algorithm based on multiple Decision Trees.

Instead of relying on a single decision tree, Random Forest trains many trees using different subsets of observations and features.

The predictions of the individual trees are combined to produce the final prediction.

Random Forest was selected for further development because it can:

- Capture nonlinear relationships
- Model interactions between variables
- Handle complex feature patterns
- Reduce reliance on a single Decision Tree
- Provide Feature Importance estimates

Following model comparison, Random Forest demonstrated stronger overall performance and was selected for further optimization.

---

# Model Evaluation

Model performance was evaluated using several complementary metrics rather than Accuracy alone.

The evaluation included:

- Accuracy
- Precision
- Recall
- F1-Score
- ROC-AUC
- Precision–Recall Curve
- Average Precision
- Confusion Matrix

This is especially important because the Approved and Denied classes are not equally represented.

A high Accuracy score alone does not necessarily mean that a model performs equally well for both classes.

---

## Original Random Forest Performance

The original Random Forest model achieved:

| Metric | Score |
|-------|------:|
| Accuracy | **0.9678** |
| Precision | **0.9830** |
| Recall | **0.9713** |
| F1-Score | **0.9771** |
| ROC-AUC | **0.9930** |
| Average Precision | **0.9967** |

These results demonstrated strong predictive performance and strong discrimination between Approved and Denied mortgage applications.

---

# 5-Fold Cross Validation

To evaluate model stability and reduce dependence on a single Train/Test split, **5-Fold Cross Validation** was performed using the training data.

In 5-Fold Cross Validation, the training data is divided into five subsets.

During each iteration:

- Four subsets are used for training.
- One subset is used for validation.
- The validation subset changes between iterations.

The results were:

| Fold | Accuracy |
|------|---------:|
| Fold 1 | 0.9705 |
| Fold 2 | 0.9679 |
| Fold 3 | 0.9710 |
| Fold 4 | 0.9706 |
| Fold 5 | 0.9684 |

### Cross Validation Summary

- **Mean Accuracy:** **0.9697 (96.97%)**
- **Standard Deviation:** **0.0013**

The similar scores across the five folds and the low standard deviation indicate that the Random Forest performance was relatively stable across the evaluated training-data partitions.

---

# Hyperparameter Tuning

After the initial model comparison and validation, Random Forest was selected for further optimization.

Hyperparameter Tuning was performed using:

```python
RandomizedSearchCV
```

RandomizedSearchCV evaluates sampled combinations of model settings instead of exhaustively testing every possible combination.

This provides a more computationally efficient way to search a larger hyperparameter space.

The optimization process examined:

- `n_estimators`
- `max_depth`
- `min_samples_split`
- `min_samples_leaf`
- `max_features`
- `class_weight`

The best configuration identified during the optimization process was:

```text
n_estimators = 300
max_depth = 20
min_samples_split = 10
min_samples_leaf = 1
max_features = None
class_weight = None
```

The best Cross Validation score obtained during the RandomizedSearchCV optimization process was approximately:

```text
0.9666
```

---

# Final Model – Tuned Random Forest

Following:

- Model comparison
- Cross Validation
- Hyperparameter Tuning
- Final evaluation

the **Tuned Random Forest** was selected as the final predictive model integrated into NOVA.

---

## Tuned Random Forest Performance

| Metric | Score |
|-------|------:|
| Accuracy | **0.9708** |
| Precision – Approved | **0.9854** |
| Recall – Approved | **0.9731** |
| F1-Score – Approved | **0.9792** |
| Precision – Denied | **0.9369** |
| Recall – Denied | **0.9651** |
| F1-Score – Denied | **0.9508** |
| ROC-AUC | **0.9950** |

The tuned model demonstrated strong overall predictive performance while maintaining strong ability to identify Denied applications.

---

# Understanding the Evaluation Metrics

## Accuracy

Accuracy measures the proportion of all predictions that were classified correctly.

```text
Correct Predictions
-------------------
Total Predictions
```

Accuracy is useful, but it should not be interpreted alone when the target classes are imbalanced.

---

## Precision

Precision answers:

> Of the applications predicted as a particular class, how many actually belonged to that class?

High Precision means that the model produces relatively few false positive predictions for the evaluated class.

---

## Recall

Recall answers:

> Of all applications that actually belonged to a particular class, how many did the model successfully identify?

Recall is especially useful when identifying minority or important cases is a priority.

---

## F1-Score

F1-Score combines Precision and Recall into a single measure.

It is useful when both Precision and Recall are important.

---

## ROC-AUC

ROC-AUC evaluates the model's ability to distinguish between the two classes across different classification thresholds.

A value close to:

```text
1.0
```

indicates strong separation between the classes.

ROC-AUC should **not** be interpreted as the percentage of predictions that were correct.

---

# Feature Importance

Feature Importance analysis was used to examine which input variables contributed most strongly to the Random Forest model's predictions.

This analysis helps improve understanding of model behavior.

However:

> **Feature Importance represents predictive contribution within the model and does not establish causality.**

A feature receiving high importance does not mean that the feature directly causes a mortgage application to be approved or denied.

---

# Preliminary Fairness Analysis

The project also includes a preliminary analysis of outcomes across demographic groups.

The purpose of this stage is to identify potential differences in observed approval outcomes and support responsible interpretation of the model.

This analysis should be interpreted carefully.

> **Observed differences between demographic groups do not automatically prove discrimination.**

Likewise, strong predictive performance does not automatically prove that a model is fair.

Additional statistical, contextual, and domain-specific analysis would be required before drawing stronger conclusions.

---

# External Validation

In addition to internal evaluation using HMDA 2023 data, **External Validation** was performed using HMDA data from **2022**.

The purpose of External Validation was to examine how the final pipeline performs on data originating from a different reporting year.

This provides additional evidence regarding model robustness and generalization beyond the HMDA 2023 development dataset.

External Validation should not be interpreted as proof that the model will achieve identical performance for every future year, population, or financial institution.

---

# NOVA Deployment

The final trained preprocessing and prediction pipeline was integrated into **NOVA Mortgage Intelligence**, an interactive Streamlit application.

Conceptually:

```text
New Mortgage Application
          |
          v
Preprocessing Pipeline
          |
          v
Tuned Random Forest
          |
          v
Prediction
          |
          +----> Approved / Denied
          |
          +----> Approval Probability
```

The user does not need to manually perform:

- Missing-value handling
- Scaling
- Encoding
- Feature transformation

The saved pipeline applies the required preprocessing automatically before generating the prediction.

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

# Verified Outcome Feedback

NOVA includes a **Verified Outcome Feedback** mechanism that allows verified real-world outcomes to be recorded and compared with previous model predictions.

The feedback mechanism supports:

- Prediction monitoring
- Comparison between predicted and observed outcomes
- Collection of future evaluation data
- A foundation for future controlled retraining

> **The production model is not automatically retrained after an individual user submission.**

Any future retraining process should include:

1. Verified observations
2. Data-quality review
3. Formal model evaluation
4. Comparison against the current production model
5. Controlled deployment

before replacing the existing production version.

---

# Model Persistence

The trained Machine Learning pipeline is saved using **Joblib**.

Main model file:

```text
mortgage_pipeline.pkl
```

Model feature information is also stored in:

```text
model_columns.pkl
```

This allows the Streamlit application to load the trained model without retraining it every time the application starts.

---

# Technologies

## Programming Language

- Python

## Data Processing

- Pandas
- NumPy

## Machine Learning

- Scikit-Learn

## Visualization

- Matplotlib
- Plotly

## Model Persistence

- Joblib

## Application Development

- Streamlit

## PDF Reporting

- ReportLab

## Development Environment

- Visual Studio Code
- Google Colab

## Version Control and Deployment

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

## 1. Clone the Repository

```bash
git clone https://github.com/samaandrea10/mortgag-dashboard.git
```

---

## 2. Navigate into the Project

```bash
cd mortgag-dashboard
```

---

## 3. Create a Virtual Environment

```bash
python -m venv .venv
```

---

## 4. Activate the Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

---

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 6. Run NOVA

```bash
streamlit run app.py
```

---

# Academic Contribution

NOVA Mortgage Intelligence demonstrates a complete Data Science and Machine Learning workflow in the mortgage domain.

The project integrates:

- Data Understanding
- Data Cleaning
- Data Preprocessing
- Exploratory Data Analysis
- Feature Preparation
- Supervised Machine Learning
- Logistic Regression
- Random Forest
- Model Comparison
- 5-Fold Cross Validation
- Hyperparameter Tuning using RandomizedSearchCV
- Model Evaluation
- Feature Importance
- Preliminary Fairness Analysis
- External Validation
- Interactive Visualization
- Streamlit Deployment
- Cloud Deployment
- Performance Monitoring
- Verified Outcome Feedback
- Automated PDF Reporting

The project demonstrates the transition from raw mortgage data and analytical experimentation to a deployed and interactive Machine Learning decision-support application.

---

# Limitations

Although the final model achieved strong predictive performance, several limitations should be considered.

- The model was developed using historical HMDA data.
- Changes in economic conditions, lending policies, borrower characteristics, or market behavior may affect future performance.
- The analysis is limited to the variables available in HMDA and the features selected for the project.
- Predictive relationships do not establish causal relationships.
- Feature Importance does not prove that a feature causes approval or denial.
- Differences observed between demographic groups do not automatically prove discrimination.
- Preliminary fairness analysis does not prove that the model is completely fair.
- External Validation using another reporting year does not guarantee identical performance in every future population or financial institution.
- NOVA is an academic decision-support platform and should not replace professional lending assessment.

---

# Future Improvements

Potential future improvements include:

- Advanced Explainable AI using SHAP
- XGBoost model comparison
- LightGBM model comparison
- CatBoost evaluation
- Extended Hyperparameter Optimization
- Continuous model monitoring
- Data Drift detection
- Concept Drift detection
- Controlled retraining using verified feedback
- Advanced bias detection
- Bias-mitigation techniques
- Model versioning
- Automated validation before deployment
- Docker-based cloud deployment
- Integration with secure and updated financial data sources

---

# Conclusion

NOVA Mortgage Intelligence demonstrates an end-to-end approach to mortgage approval prediction using Machine Learning.

The project began with HMDA data understanding and preprocessing, progressed through model development, comparison, validation, and optimization, and concluded with the deployment of the selected Tuned Random Forest pipeline in an interactive Streamlit application.

The project demonstrates that strong predictive performance alone is not sufficient for evaluating a Machine Learning system. Model stability, minority-class performance, interpretation, preprocessing consistency, fairness considerations, validation, usability, and deployment are also important components of an end-to-end Data Science solution.

NOVA therefore represents not only a trained predictive model, but the integration of Data Science, Machine Learning, model evaluation, and application development into a unified decision-support platform.

---

# Author

**Sama Andrea**

**B.Sc. Information Systems**  
**Data Science**  
**Final Project**

---

# License

This repository was developed for academic, educational, and research purposes.
