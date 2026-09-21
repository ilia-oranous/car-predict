# 🏎️ Car Price Prediction

A machine learning project for predicting the price of supercars based on their specifications.

## 📌 Overview

In this project, I tried to build a machine learning system that can predict the price of a supercar based on its features.

The dataset used in this project was obtained from Kaggle. It contains information about different supercars and their specifications, such as:

* Car Make
* Car Model
* Year
* Engine Size
* Horsepower
* Torque
* 0–60 MPH Time
* Powertrain Type
* Price

The main goal of this project was not only to train a model, but also to go through a complete machine learning workflow, starting from data exploration and cleaning and ending with model evaluation and a small application.

---

## 🔄 Project Workflow

The project was developed in several steps:

```text
Dataset
   ↓
Exploratory Data Analysis
   ↓
Data Cleaning
   ↓
Feature Engineering
   ↓
Preprocessing
   ↓
Baseline Models
   ↓
Hyperparameter Tuning
   ↓
Cross-Validation
   ↓
Final Model
   ↓
Streamlit Application
```

---

## 1. 🔍 Exploratory Data Analysis

First, I loaded the dataset and explored its structure.

The main goals of this step were:

* Understanding the features
* Checking data types
* Finding missing values
* Looking for unusual values
* Understanding the distribution of the target variable
* Studying relationships between features and car prices

Different visualizations were also created to better understand the dataset.

---

## 2. 🧹 Data Cleaning

After exploring the dataset, I handled the data quality issues that were found during EDA.

One of the main problems was missing values in `Engine Size (L)`.

This happened mainly because engine size is not applicable to fully electric vehicles.

Instead of simply filling all missing values with the mean of the whole column, I considered the `Powertrain Type` when handling these values.

This was important because the meaning of a missing engine size is different for an electric vehicle compared with an internal combustion engine vehicle.

After cleaning, the processed dataset was saved and used in the next steps.

---

## 3. 🛠️ Feature Engineering

For feature engineering, I tried to create useful features instead of adding many artificial features.

The main feature created in this project was:

### `Car Age`

```text
Car Age = 2026 - Year
```

The reason for creating this feature was that the age of a car can be more directly useful for price prediction than the production year itself.

I also experimented with other possible features during the development process, but I decided to keep the feature engineering relatively simple.

---

## 4. ⚙️ Data Preprocessing

Before training the models, the numerical and categorical features were processed separately.

### Numerical Features

The numerical features were scaled using `MinMaxScaler`.

### Categorical Features

Categorical features such as:

* `Car Make`
* `Car Model`
* `Powertrain Type`

were transformed using `OneHotEncoder`.

`handle_unknown="ignore"` was also used so that unseen categories in the test data would not cause an error during prediction.

The preprocessing was implemented using a `ColumnTransformer` and later combined with the models using a `Pipeline`.

---

## 5. 🤖 Baseline Models

Before tuning the models, I trained several regression models with their initial/default configurations.

The models were:

* Linear Regression
* Ridge Regression
* Random Forest
* Gradient Boosting
* XGBoost

The purpose of this step was to get a baseline and compare how different models perform on this dataset.

One interesting result was that the more complex tree-based models did not automatically perform better.

Linear Regression and Ridge performed very well compared with the other models.

This was an interesting result because it showed that model complexity does not always mean better performance.

---

## 6. 🎛️ Hyperparameter Tuning

After the baseline comparison, I tuned the models that showed potential for better performance.

For example, parameters such as the following were tested for the tree-based models:

* Number of estimators
* Learning rate
* Maximum depth
* Minimum samples per split
* Minimum samples per leaf
* Subsampling parameters

`RandomizedSearchCV` was used to search through different combinations of hyperparameters.

The goal was to check whether changing the hyperparameters could improve the baseline results.

Interestingly, the tuned Gradient Boosting and XGBoost models did not outperform the simpler models in my experiments.

---

## 7. 📊 Cross-Validation

After model tuning, I used cross-validation to get a more reliable comparison between the best linear models.

The main models compared at this stage were:

* Ridge Regression
* Linear Regression

The results from the cross-validation were:

| Model             |    Mean R² |    Mean RMSE |    Mean MAE |
| ----------------- | ---------: | -----------: | ----------: |
| **Ridge**         | **0.9267** | **$178,474** |     $48,496 |
| Linear Regression |     0.9232 |     $182,889 | **$40,203** |

Ridge achieved a slightly higher mean R² and lower mean RMSE, while Linear Regression achieved a lower mean MAE.

This shows that the choice of the evaluation metric can affect how we interpret model performance.

---

## 8. 🏆 Final Model

Based on the experiments and cross-validation results, I selected **Ridge Regression** as the final model used in the application.

The complete preprocessing and model were saved together as a single pipeline using `joblib`.

This makes it possible to load the trained pipeline later and directly pass new car specifications to it without manually repeating the preprocessing steps.

The saved model is:

```text
best_ridge_pipeline.pkl
```

---

## 9. 🌐 Streamlit Application

After completing the machine learning part, I created a simple Streamlit application for using the trained model.

The application allows the user to enter different car specifications, including:

* Car Make
* Car Model
* Powertrain Type
* Engine Size
* Horsepower
* Torque
* 0–60 MPH Time
* Car Age

After entering the specifications, the application predicts the estimated price of the car.

It also includes a few visualizations, such as:

* Predicted price vs. brand average
* Predicted price vs. overall market average
* A radar chart showing the selected vehicle's specifications

The application was mainly built to make the machine learning model easier to interact with.

---

## 📁 Project Structure

```text
car-predict/
│
├── data/
│   ├── Sport car price.csv
│   ├── car_price_cleaned.csv
│   └── car_price_engineered.csv
│
├── notebooks/
│   ├── EDA.ipynb
│   ├── Feature_Engineering.ipynb
│   └── Modeling.ipynb
│
├── app.py
├── best_ridge_pipeline.pkl
├── requirements.txt
└── README.md
```

---

## 🧰 Technologies Used

### Programming Language

* Python

### Data Analysis

* Pandas
* NumPy

### Data Visualization

* Matplotlib
* Seaborn
* Plotly

### Machine Learning

* Scikit-learn
* XGBoost

### Application

* Streamlit

### Model Serialization

* Joblib

---

## 🚀 How to Run

Clone the repository:

```bash
git clone https://github.com/ilia-oranous/car-predict.git
```

Go to the project directory:

```bash
cd car-predict
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

The application should then open in your browser.

---

## 🔮 Future Improvements

There are several things that can be added to this project in the future.

Some possible improvements are:

* Adding more real-world car data
* Using a larger dataset
* Adding more features such as mileage, generation, trim, and market information
* Improving the handling of high-end and rare vehicles
* Adding model explainability
* Creating a FastAPI backend
* Connecting the application to a database
* Adding an LLM-based car assistant
* Deploying the application

The current version mainly focuses on the machine learning pipeline and price prediction.

---

## 🤖 Use of LLMs

During the development of this project, I occasionally used Large Language Models such as DeepSeek as coding assistants.

They were mainly used for:

* Helping with some visualization code
* Assisting with parts of the Streamlit application
* Troubleshooting some implementation issues
* Speeding up parts of the development process

The main decisions related to data cleaning, feature engineering, model selection, evaluation, and the machine learning workflow were made and reviewed during the development of the project.

LLMs were used as development tools, not as a replacement for understanding the machine learning concepts used in the project.

---

## 📌 Notes

This project is mainly an educational and portfolio project.

The predicted prices should not be considered professional market valuations. The quality of the predictions depends heavily on the dataset and the features available in it.

The main purpose of the project was to practice and demonstrate an end-to-end machine learning workflow using a real-world-style regression problem.
