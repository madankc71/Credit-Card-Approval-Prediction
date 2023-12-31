# -*- coding: utf-8 -*-
"""credit card approval.ipynb

Automatically generated by Collaboratory.

The original file is located at
    https://colab.research.google.com/drive/1VFcxYZpIbeUF3KSpfGZnCwZi3i0tNfg8

#**Credit Card Approval Prediction**

In today's fast-paced world, financial institutions receive a multitude of credit card applications daily. The process of scrutinizing these applications, considering factors like income levels, loans, and credit reports, can be laborious and prone to errors. It can be automated using Machine learning.

I've developed an **Automatic Credit Card Approval Predictor using advanced machine learning techniques**. The primary goal is to expedite the approval process while maintaining accuracy and precision. The project incorporates a comprehensive pipeline, from exploratory data analysis to model implementation with the **accuracy of 100%**.

This technical journey spans meticulous Exploratory Data Analysis (EDA), diverse machine learning classifiers (Logistic Regression, Random Forest, Decision Tree, XGBoost), and crucial data preprocessing steps (data imputation, normalization, and segregation) and visualization using seaborn and matplotlib.

#**Exploratory Data Analysis (EDA)**

##Libraries

We'll begin by importing the necessary libraries that we'll use for our Credit Card Approval Prediction project.

*   pandas and numpy for data manipulation and numerical operations.
*   matplotlib and seaborn for data visualization.
*   train_test_split for splitting the dataset into training and testing data.
*   MinMaxScaler for data normalization.
*   LogisticRegression, DecisionTreeClassifier, RandomForestClassifier, and XGBClassifier for machine learning models.
*   confusion_matrix, accuracy_score for evaluating classification accuracy metrics
*   ConfusionMatrixDisplay for visually represent accuracy metrics
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

"""##Data Loading

We load our dataset into a pandas DataFrame for analysis.
"""

credit_data = pd.read_csv("/content/crx.data", header = None)

"""##Data Inspection

To get an initial understanding of the dataset, we'll check the first few rows using **`head()`**:
"""

credit_data.head()

"""We'll also find the number of rows and columns in the dataset:"""

credit_data.shape

"""From the first few rows of the dataset, it seems like columns '1', '2', '7', '10', '13', and '14' are numerical and the remainings are categorical. However, we need to check the datatype of each columns. Data types of each column can be obtained using dtypes:"""

credit_data.dtypes

"""Surprisingly, we found that only columns '2', '7', '10', and '14' are numerical.

##Data Summary

###**Statistical Summary**

Lets check the summary statistics of the numerical columns in the dataset:
"""

credit_data.describe()

"""###**Data Information**

To get data information, including non-null entries, data types, and memory usage:
"""

credit_data.info()

"""##Data Visualization: Bar Chart

We'll create a bar graph using Seaborn to visualize the distribution of categorical data.
"""

# Create a bar graph using Seaborn
target_column = credit_data.iloc[:, -1]

category_names = ['Approval', 'Rejection']
colors = ["blue", "red"]

sns.countplot(x=target_column, data=credit_data, palette=colors)  # Use countplot for simplicity
plt.xlabel('Types')
plt.ylabel('Total Count')
plt.title('Bar Graph of Target Variable (Reject or Accept)')

# Add names for each bar on the x-axis
plt.xticks(ticks=range(len(category_names)), labels=category_names)

plt.show()

"""From the chart, we observed that there are more rejections than acceptances in the dataset, but the difference is not significantly high.

##Uniqueness

To explore unique values in each column:
"""

# List unique values for each column
unique_values_per_column = {column: credit_data[column].unique() for column in credit_data.columns}

# Print the unique values for each column
for column, values in unique_values_per_column.items():
    print(f"Column '{column}' has unique values:")
    print(values)

"""We found that there are '?' values in some columns. To handle the **missing values**, we replace '?' with 'NaN':"""

credit_data_nan_replace = credit_data.replace("?", np.NaN)

"""Counting the total numbers of missing values in each columns"""

import matplotlib.pyplot as plt
import seaborn as sns

# Count missing values in each column
missing_values = credit_data_nan_replace.isnull().sum()

# Plotting the missing values
plt.figure(figsize=(10, 6))
sns.barplot(x=missing_values.index, y=missing_values.values)
plt.xlabel('Columns of the dataset')
plt.ylabel('Number of Missing Values')
plt.title('Missing Values in Each Column')
plt.xticks(rotation=45)
plt.show()

"""From the above bar chart, 7 columns have the missing values. Among them, three columns have around 12 missing values, 2 columns have 6 and the remaining two have 9 missing values.

#**Data Preprocessing**

##**Data Split**

We begin by splitting the dataset into training data (75%) and testing data (25%).
"""

credit_train, credit_test = train_test_split(credit_data_nan_replace, test_size= 0.25, random_state=2)

"""Let's examine the shape of the training and testing datasets:"""

credit_train.shape, credit_test.shape

"""##**Data Imputation**

###Imputing **Missing Value** in Numerical Columns

We address missing values in numerical columns by imputing them with mean values using the fillna() function:
"""

credit_train_imputed = credit_train.fillna(credit_train.mean())
credit_test_imputed = credit_test.fillna(credit_test.mean())

"""However, a warning is raised regarding the missing argument numeric_only=True. To resolve this, we explicitly include it in the fillna() function:"""

credit_train_imputed = credit_train.fillna(credit_train.mean(numeric_only=True))
credit_test_imputed = credit_test.fillna(credit_test.mean(numeric_only=True))

"""###Imputing **Missing Value** in Categorical Columns

Despite handling numerical columns, we still need to address missing values in categorical columns. These columns have the 'object' datatype. We iterate over each column and replace missing values with the most common values (mode) for each column:
"""

for col in credit_train_imputed.columns:
  if credit_train_imputed[col].dtypes == "object":
    credit_train_imputed = credit_train_imputed.fillna(credit_train_imputed[col].value_counts().index[0])
    credit_test_imputed = credit_test_imputed.fillna(credit_test_imputed[col].value_counts().index[0])

"""##**One-hot Encoding**

To make all values numerical, we employ one-hot encoding to convert categorical values into numerical representation:
"""

train_hot_encoding = pd.get_dummies(credit_train_imputed)
test_hot_encoding = pd.get_dummies(credit_test_imputed)

train_hot_encoding.shape, test_hot_encoding.shape

"""After one-hot encoding, it's possible that the test data features may not match those of the training data. In such cases, it's necessary to reindex the test data columns to align them with the training data:"""

test_hot_encoding = test_hot_encoding.reindex(columns=train_hot_encoding.columns, fill_value=0)
test_hot_encoding.shape

"""##**Segregating the feature variables and the target variable**

In the dataset, the last column represents the target variable, while the remaining 15 columns are feature variables. Thus, we segregate the features and the labels:
"""

X_train, y_train = (train_hot_encoding.iloc[:, :-1].values, train_hot_encoding.iloc[:, [-1]].values)
X_test, y_test = (test_hot_encoding.iloc[:, :-1].values, test_hot_encoding.iloc[:, [-1]].values)

"""Lets check the shape feature variables and target variables in training and test data."""

X_train.shape, X_test.shape, y_train.shape, y_test.shape

"""We noticed that the shape of the target (label) variables is 2-dimensional. To resolve this, we change them to 1D using the ravel() function:"""

y_train = np.array(y_train).ravel()
y_test = np.array(y_test).ravel()

"""##**Data Normalization**

We implemented four different models using LogisticRegression, RandomForestClassifier, DecisionTreeClassifier, and XGBClassifier. The accuracy for LogisticRegression and RandomForestClassifier improved with data normalization. Other classifiers achieved 100% accuracy even without normalizing the data.
"""

scaler = MinMaxScaler(feature_range=(0,1))
rescaledX_train = scaler.fit_transform(X_train)
rescaledX_test = scaler.transform(X_test)

"""#**Building Machine Learning Models**

## **Logistic Regression Model**

###Before normalizing data

In this section, we train a Logistic Regression model using the original (non-normalized) data:
"""

# Create an Logistic Regression model
logicalRegressionModel = LogisticRegression()

# Train the model
logicalRegressionModel.fit(X_train, y_train)

# Predictions on training and test sets
train_predict = logicalRegressionModel.predict(X_train)
test_predict = logicalRegressionModel.predict(X_test)

# Calculate accuracy scores
test_accuracy = accuracy_score(y_test, test_predict)
train_accuracy = accuracy_score(y_train, train_predict)

# Generate confusion matrix
confusion_matrix_result = confusion_matrix(y_test, test_predict)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, fmt="d", cmap="Blues", linewidths=.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Display accuracy scores
print("Accuracy: \n Train Score: ", train_accuracy*100, "% and Test Score: ", test_accuracy*100, "%")

"""###After the normalizing the data

Next, we retrain the Logistic Regression model after normalizing the data:
"""

# Create an Logistic Regression model
logicalreg = LogisticRegression()

# Train the model
logicalreg.fit(rescaledX_train, y_train)

# Predictions on training and test sets
train_predict = logicalreg.predict(rescaledX_train)
test_predict = logicalreg.predict(rescaledX_test)

# Calculate accuracy scores
test_accuracy = accuracy_score(y_test, test_predict)
train_accuracy = accuracy_score(y_train, train_predict)

# Generate confusion matrix
confusion_matrix_result = confusion_matrix(y_test, test_predict)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, fmt="d", cmap="Blues", linewidths=.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Display accuracy scores
print("Accuracy: \n Train Score: ", train_accuracy*100, "% and Test Score: ", test_accuracy*100, "%")

"""##**Random Forest Clasifier Model**

###Before normalizing data

Now, let's explore the Random Forest Classifier model before normalizing the data:
"""

# Create an Random Forest Classifier model
RFModel = RandomForestClassifier()

# Train the model
RFModel.fit(X_train, y_train)

# Predictions on the training and test sets
train_predict = RFModel.predict(X_train)
test_predict = RFModel.predict(X_test)

# Calculate accuracy scores
test_accuracy = accuracy_score(y_test, test_predict)
train_accuracy = accuracy_score(y_train, train_predict)

# Generate confusion matrix
confusion_matrix_result = confusion_matrix(y_test, test_predict)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, fmt="d", cmap="Blues", linewidths=.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Display accuracy scores
print("Accuracy: \n Train Score: ", train_accuracy*100, "% and Test Score: ", test_accuracy*100, "%")

"""###After Normalizing data

Following that, we reevaluate the Random Forest Classifier model after normalizing the data:
"""

# Create and train a RandomForestClassifier using the rescaled training data
RFModel = RandomForestClassifier()
RFModel.fit(rescaledX_train, y_train)

# Predictions on training and test sets
train_predict = RFModel.predict(rescaledX_train)
test_predict = RFModel.predict(rescaledX_test)

# Calculate accuracy scores
test_accuracy = accuracy_score(y_test, test_predict)
train_accuracy = accuracy_score(y_train, train_predict)

# Generate confusion matrix
confusion_matrix_result = confusion_matrix(y_test, test_predict)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, fmt="d", cmap="Blues", linewidths=.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Display accuracy scores
print("Accuracy: \n Train Score: ", train_accuracy*100, "% and Test Score: ", test_accuracy*100, "%")



"""##**Decision Tree Classifier**

Now, let's move on to the Decision Tree Classifier:
"""

# Create an Decision Tree Classifier model
DTModel = DecisionTreeClassifier()

# Train the model
DTModel.fit(X_train, y_train)

# Predictions on the training and test sets
train_predict = DTModel.predict(X_train)
test_predict = DTModel.predict(X_test)

# Calculate accuracy scores
test_accuracy = accuracy_score(y_test, test_predict)
train_accuracy = accuracy_score(y_train, train_predict)

# Generate confusion matrix
confusion_matrix_result = confusion_matrix(y_test, test_predict)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, fmt="d", cmap="Blues", linewidths=.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Display accuracy scores
print("Accuracy: \n Train Score: ", train_accuracy*100, "% and Test Score: ", test_accuracy*100, "%")

"""##**Model using XGBClassifier**

Lastly, we examine the model using XGBClassifier:
"""

# Create an XGBoost Classifier model
XG_model = XGBClassifier()

# Train the model
XG_model.fit(X_train, y_train)

# Predictions on the training and test sets
train_predict = XG_model.predict(X_train)
test_predict = XG_model.predict(X_test)

# Calculate accuracy scores
test_accuracy = accuracy_score(y_test, test_predict)
train_accuracy = accuracy_score(y_train, train_predict)

# Generate confusion matrix
confusion_matrix_result = confusion_matrix(y_test, test_predict)

# Plot Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(confusion_matrix_result, annot=True, fmt="d", cmap="Blues", linewidths=.5)
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('True')
plt.show()

# Display accuracy scores
print("Accuracy: \n Train Score: ", train_accuracy*100, "% and Test Score: ", test_accuracy*100, "%")

"""#**Conclusion**

By combining meticulous exploratory data analysis, data preprocessing, and robust machine learning models, this project got the 100% accurate credit card approval model with the XGBClassifier, DecisionTreeClassifier and LogisticRegression (with normalized data). The automation not only saves time but also enhances accuracy, paving the way for more efficient decision-making in the financial domain.
"""
