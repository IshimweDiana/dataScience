import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load the dataset
file_path = 'Employee data.csv'
employee_data = pd.read_csv(file_path)

# Data Cleaning
q1 = employee_data['MonthlyIncome'].quantile(0.25)
q3 = employee_data['MonthlyIncome'].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

# Handle outliers in MonthlyIncome
def cap_outliers(value):
    if value < lower_bound:
        return lower_bound
    elif value > upper_bound:
        return upper_bound
    else:
        return value

employee_data['MonthlyIncome'] = employee_data['MonthlyIncome'].apply(cap_outliers)

bins = [20, 30, 40, 50, 60, 70]
labels = ['20-30', '31-40', '41-50', '51-60', '61-70']
employee_data['AgeGroup'] = pd.cut(employee_data['Age'], bins=bins, labels=labels, right=False)
employee_data['Gender'] = employee_data['Gender'].astype('category')
employee_data['MaritalStatus'] = employee_data['MaritalStatus'].astype('category')

# Streamlit Dashboard
st.title("Employee Data Analysis Dashboard")

# Sidebar filters
st.sidebar.header("Filters")
age_group_filter = st.sidebar.multiselect(
    "Select Age Group:",
    options=employee_data['AgeGroup'].unique(),
    default=employee_data['AgeGroup'].unique()
)
gender_filter = st.sidebar.multiselect(
    "Select Gender:",
    options=employee_data['Gender'].unique(),
    default=employee_data['Gender'].unique()
)
marital_status_filter = st.sidebar.multiselect(
    "Select Marital Status:",
    options=employee_data['MaritalStatus'].unique(),
    default=employee_data['MaritalStatus'].unique()
)

# Apply filters
filtered_data = employee_data[
    (employee_data['AgeGroup'].isin(age_group_filter)) &
    (employee_data['Gender'].isin(gender_filter)) &
    (employee_data['MaritalStatus'].isin(marital_status_filter))
]

# Display filtered data
st.header("Filtered Employee Data")
st.write(filtered_data)

# Visualizations
st.header("Visualizations")

# Histogram: Age Distribution
st.subheader("Age Distribution")
age_hist_fig, ax = plt.subplots()
ax.hist(filtered_data['Age'], bins=10, color='skyblue', edgecolor='black')
ax.set_title("Age Distribution")
ax.set_xlabel("Age")
ax.set_ylabel("Frequency")
st.pyplot(age_hist_fig)

# Boxplot: MonthlyIncome by Gender
st.subheader("Monthly Income by Gender")
income_boxplot_fig, ax = plt.subplots()
sns.boxplot(x='Gender', y='MonthlyIncome', data=filtered_data, ax=ax, palette='Set2')
ax.set_title("Monthly Income by Gender")
ax.set_xlabel("Gender")
ax.set_ylabel("Monthly Income")
st.pyplot(income_boxplot_fig)

# Bar Chart: Environment Satisfaction Levels
st.subheader("Environment Satisfaction Levels")
env_satisfaction_counts = filtered_data['EnvironmentSatisfaction'].value_counts().sort_index()
env_satisfaction_fig, ax = plt.subplots()
ax.bar(env_satisfaction_counts.index, env_satisfaction_counts.values, color='coral', edgecolor='black')
ax.set_title("Environment Satisfaction Levels")
ax.set_xlabel("Satisfaction Level")
ax.set_ylabel("Number of Employees")
st.pyplot(env_satisfaction_fig)

# Boxplot: MonthlyIncome by Marital Status
st.subheader("Monthly Income by Marital Status")
marital_income_fig, ax = plt.subplots()
sns.boxplot(x='MaritalStatus', y='MonthlyIncome', data=filtered_data, ax=ax, palette='Pastel1')
ax.set_title("Monthly Income Distribution by Marital Status")
ax.set_xlabel("Marital Status")
ax.set_ylabel("Monthly Income")
st.pyplot(marital_income_fig)

st.write("\n**Dashboard created using Streamlit!**")
