#!/usr/bin/env python
# coding: utf-8

# In[1]:


#opening data

import pandas as pd
import numpy as np

df = pd.read_csv('beep.csv')

df.drop(df.tail(2).index,inplace=True)

df['Age'] = df['Age'].astype(float)
df["Annual Income (x1000 $)"] = df["Annual Income (x1000 $)"].astype(float) 

df["Annual Spending on Electronics"] = df['Monthly Electronics Spend'] * 12

df["Electronic spending as % of income"] = df['Annual Spending on Electronics'] /(df['Annual Income (x1000 $)'] *1000)


pd.to_numeric(df['Annual Income (x1000 $)']) # convert col from string to float


# In[5]:


df["Electronic spending as % of income"].describe()


# In[4]:


#need to include new location dummy into code below where the dummy variables are ctrl c ctrl v


# In[5]:


state_mapping = {
    'Connecticut': 'Northeast',
    'Maine': 'Northeast',
    'Massachusetts': 'Northeast',
    'New Hampshire': 'Northeast',
    'Rhode Island': 'Northeast',
    'Vermont': 'Northeast',
    'New Jersey': 'Northeast',
    'New York': 'Northeast',
    'Pennsylvania': 'Northeast',
    'Illinois': 'Midwest',
    'Indiana': 'Midwest',
    'Michigan': 'Midwest',
    'Ohio': 'Midwest',
    'Wisconsin': 'Midwest',
    'Iowa': 'Midwest',
    'Kansas': 'Midwest',
    'Minnesota': 'Midwest',
    'Missouri': 'Midwest',
    'Nebraska': 'Midwest',
    'North Dakota': 'Midwest',
    'South Dakota': 'Midwest',
    'Delaware': 'South',
    'Florida': 'South',
    'Georgia': 'South',
    'Maryland': 'South',
    'North Carolina': 'South',
    'South Carolina': 'South',
    'Virginia': 'South',
    'West Virginia': 'South',
    'Alabama': 'South',
    'Kentucky': 'South',
    'Mississippi': 'South',
    'Tennessee': 'South',
    'Arkansas': 'South',
    'Louisiana': 'South',
    'Oklahoma': 'South',
    'Texas': 'South',
    'Arizona': 'West',
    'Colorado': 'West',
    'Idaho': 'West',
    'Montana': 'West',
    'Nevada': 'West',
    'New Mexico': 'West',
    'Utah': 'West',
    'Wyoming': 'West',
    'Alaska': 'West',
    'California': 'West',
    'Hawaii': 'West',
    'Oregon': 'West',
    'Washington': 'West'
}
df['Location'] = df['Location'].map(state_mapping)


# In[6]:


from sklearn.preprocessing import StandardScaler
dummy_variables = df.copy()

def create_dummy_variables(df, column):
    unique_values = df[column].unique()
    baseline = unique_values[0]  # Assuming the first unique value is the baseline

    # Create dummy variables for non-baseline values
    for value in unique_values[1:]:
        dummy_column_name = f"{column}{value}Dummy"  # Name of the dummy variable column
        df[dummy_column_name] = (df[column] == value).astype(int)

    return df

dummy = ['Gender',
         'Marital Status',
         'Work Status',
         'Education',
         "Location",
         'Purchasing Decision-maker',
         'Purchasing Location',
         'Technology Adoption',
         'Favorite feature']  # List of columns for dummy variables

for column in dummy:
    df = create_dummy_variables(df, column)

df[dummy] = dummy_variables[dummy]  # Restore the original columns

# Drop the original dummy variable columns
df = df.drop(dummy, axis=1)


# In[7]:


to_standarise = ['Annual Income (x1000 $)', 'Age', 'Monthly Electronics Spend',
                 'Monthly Household Spend', 'Purchasing Frequency (every x months)',
                 'TV Viewing (hours/day)', 'Annual Spending on Electronics',
                 'Electronic spending as % of income']

# Create a new DataFrame with the columns to be standardized
df_standarised = df[to_standarise + ['ID']].copy()

# Separate the 'ID' column from the columns to be standardized
id_column = df_standarised['ID']
df_standarised.drop('ID', axis=1, inplace=True)

# Standardize the data
scaler = StandardScaler()
df_standarised[to_standarise] = scaler.fit_transform(df_standarised[to_standarise])

# Add the 'ID' column back to the standarised DataFrame
df_standarised['ID'] = id_column

# Create a list of column names to append
columns_to_append = df.columns[9:]
# Append the columns from df to df_standarised
df_standarised = pd.concat([df_standarised, df[columns_to_append]], axis=1)


# In[8]:


#Elbow Plot

from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
# Prepare a list to store the inertia values
inertia = []

# Define the range of clusters to evaluate
k_values = range(1, 11)

# Perform k-means clustering for each value of k
for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(df_standarised)
    inertia.append(kmeans.inertia_)

# Plot the elbow curve
plt.plot(k_values, inertia, 'bx-')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('Elbow Method')
plt.show()


# In[8]:


from sklearn.cluster import KMeans

# Create a copy of the DataFrame without the 'ID' column
df_cluster = df_standarised.drop('ID', axis=1)

# Perform k-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
kmeans.fit(df_cluster)

# Assign cluster labels to a new column in the original dataframe
df_standarised['Cluster'] = kmeans.labels_

# Add the 'ID' column back to the DataFrame
df_standarised['ID'] = range(1, len(df_standarised) + 1)


# In[7]:


# Group the dataframe by the 'Cluster' column and calculate the mean for each group
cluster_means = df_standarised.groupby('Cluster').mean()

# Print the resulting table
print(cluster_means)


# In[9]:


column_names = [
    'Annual Income (x1000 $)',
    'Age',
    'Monthly Electronics Spend',
    'Monthly Household Spend',
    'Purchasing Frequency (every x months)',
    'TV Viewing (hours/day)',
    'Annual Spending on Electronics',
    'Electronic spending as % of income',

]

# Calculate the mean and standard deviation of the specified columns from df
mean_values = df[column_names].mean()
std_values = df[column_names].std()

# List of columns to unstandardize
columns_to_unstandarize = [
    'Annual Income (x1000 $)',
    'Age',
    'Monthly Electronics Spend',
    'Monthly Household Spend',
    'Purchasing Frequency (every x months)',
    'TV Viewing (hours/day)',
    'Annual Spending on Electronics',
    'Electronic spending as % of income',

]

# Create a new dataframe as a copy of df_standarised
df_unstandarized = df_standarised.copy()

# Unstandarize the selected columns
df_unstandarized[columns_to_unstandarize] = df_standarised[columns_to_unstandarize] * std_values[columns_to_unstandarize] + mean_values[columns_to_unstandarize]


# In[12]:


# Group the dataframe by the 'Cluster' column and calculate the mean for each group
cluster_averages = df_unstandarized.groupby('Cluster').mean()

# Print the average values for each column
for column in cluster_averages.columns:
    print(f"Cluster {column}:\n{cluster_averages[column]}\n")


# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

for column in ['Annual Income (x1000 $)', 'Age', 'Monthly Electronics Spend', 'Monthly Household Spend',
               'Purchasing Frequency (every x months)', 'TV Viewing (hours/day)', 'Annual Spending on Electronics',
               'Electronic spending as % of income']:
    plt.figure(figsize=(8, 6))
    sns.violinplot(x='Cluster', y=column, data=df_unstandarized)
    plt.xlabel('Cluster')
    plt.ylabel(column)
    plt.title(f'Violin Plot of {column} by Cluster')
    plt.show()


# In[10]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Get the values of the 'Annual Income (x1000 $)' column
x = df_unstandarized["Annual Income (x1000 $)"]

# Calculate the mean and standard deviation
mean = x.mean()
std = x.std()

# Define the threshold for outliers
threshold = 3 * std

# Filter out the outliers
filtered_data = df_unstandarized[(x - mean).abs() <= threshold]

# Set the figure size
plt.figure(figsize=(8, 6))

# Create the violin plot
sns.violinplot(x='Cluster', y='Annual Income (x1000 $)', data=filtered_data)

# Customize the plot
plt.xlabel('Cluster')
plt.ylabel('Annual Income (x1000 $)')
plt.title('Violin Plot of Annual Income adjusted for outliers by Cluster')

# Display the plot
plt.show()


# In[12]:


scrap = pd.read_csv('beep.csv')

scrap.drop(scrap.tail(2).index, inplace=True)

scrap['Age'] = scrap['Age'].astype(float)
scrap["Annual Income (x1000 $)"] = scrap["Annual Income (x1000 $)"].astype(float)

scrap["Annual Spending on Electronics"] = scrap['Monthly Electronics Spend'] * 12

scrap["Electronic spending as % of income"] = scrap['Annual Spending on Electronics'] / (scrap['Annual Income (x1000 $)'] * 1000)

pd.to_numeric(scrap['Annual Income (x1000 $)']) # convert col from string to float

scrap['Location'] = scrap['Location'].map(state_mapping)


columns_to_analyze = ['Gender', 'Marital Status', 'Work Status', 'Education',
                      'Location', 'Purchasing Decision-maker', 'Purchasing Location',
                      'Technology Adoption', 'Favorite feature']
scrap = pd.merge(scrap, df_unstandarized[['Cluster']], left_index=True, right_index=True)


# Iterate over the columns
for column in columns_to_analyze:
    column_clusters = scrap.groupby(['Cluster', column]).size().unstack()
    cluster_counts = column_clusters.sum(axis=1)
    column_percentages = column_clusters.div(cluster_counts, axis=0) * 100
    
    # Print the resulting table
    print(f"{column}:")
    print("\t\tCluster 0\tCluster 1\tCluster 2\t")
    for value in column_percentages.columns:
        percentages = '\t\t'.join(f"{percentage:.2f}%" for percentage in column_percentages[value])
        print(f"{value}\t\t{percentages}")
    print()


# In[13]:


# Initialize an empty dictionary: column_counts
column_counts = {}

# Iterate over columns in DataFrame
for column in scrap.columns:
    # Extract column from DataFrame
    col = scrap[column]

    # Initialize an empty dictionary for the current column
    col_count = {}

    # Iterate over entries in the current column
    for entry in col:
        # If the entry is in col_count, add 1
        if entry in col_count.keys():
            col_count[entry] += 1
        # Else add the entry to col_count, set the value to 1
        else:
            col_count[entry] = 1

    # Add the col_count dictionary to column_counts with the column name as key
    column_counts[column] = col_count

# Print the populated column_counts dictionary
print(column_counts)


# In[22]:


scrap


# In[19]:


columns_to_output = ['Electronic spending as % of income', 'Monthly Electronics Spend', 'TV Viewing (hours/day)']

for i in columns_to_output:
    # Calculate percentiles to determine the segment boundaries
    percentiles = scrap[i].quantile([0, 0.25, 0.5, 0.75, 1])

    # Create a new column with the segment number
    scrap[i + ' segment'] = pd.qcut(scrap[i],
                                    q=[0, 0.25, 0.5, 0.75, 1],
                                    labels=False,
                                    duplicates='drop')

    # Increment the segment number by 1 to start from 1 instead of 0
    scrap[i + ' segment'] += 1

    columns_to_analyze = ['Gender', 'Marital Status', 'Work Status', 'Education',
                          'Location', 'Purchasing Decision-maker', 'Purchasing Location',
                          'Technology Adoption', 'Favorite feature']

    # Sort the dataframe by the segment column
    scrap_sorted = scrap.sort_values(by=i + ' segment')

    # Print the resulting table
    print(f"{i}:")
    print("\t\tSegment 1\tSegment 2\tSegment 3\tSegment 4\t")
    for column in columns_to_analyze:
        column_segments = scrap_sorted.groupby([i + ' segment', column]).size().unstack()
        segment_counts = column_segments.sum(axis=1)
        column_percentages = column_segments.div(segment_counts, axis=0) * 100

        for value in column_percentages.columns:
            percentages = '\t\t'.join(f"{percentage:.2f}%" for percentage in column_percentages[value])
            print(f"{value}\t\t{percentages}")
    print()

    


# In[36]:


get_ipython().system('pip install matplotlib')
get_ipython().system('pip install scikit-learn')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

# Perform PCA with 2 components
pca_2d = PCA(n_components=2)
pca_2d_result = pca_2d.fit_transform(df_standarised)

# Create a 2D scatter plot with color-coded and labeled clusters
plt.figure(figsize=(8, 6))
for cluster in set(df_standarised["Cluster"]):
    indices = df_standarised["Cluster"] == cluster
    plt.scatter(pca_2d_result[indices, 0], pca_2d_result[indices, 1], label=f"Cluster {cluster}")
plt.title("2D PCA Visualization")
plt.legend()
plt.show()

# Perform PCA with 3 components
pca_3d = PCA(n_components=3)
pca_3d_result = pca_3d.fit_transform(df_standarised)

# Create a 3D scatter plot with color-coded and labeled clusters
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
for cluster in set(df_standarised["Cluster"]):
    indices = df_standarised["Cluster"] == cluster
    ax.scatter(pca_3d_result[indices, 0], pca_3d_result[indices, 1], pca_3d_result[indices, 2], label=f"Cluster {cluster}")
ax.set_title("3D PCA Visualization")
ax.legend()
plt.show()


# In[33]:


#gives some wack results ask prof
import statsmodels.api as sm

# Select the independent variables
independent_vars = ['Annual Income (x1000 $)', 'Age', 'Monthly Electronics Spend',
                   'Monthly Household Spend', 'Purchasing Frequency (every x months)',
                   'TV Viewing (hours/day)', 'Annual Spending on Electronics',
                    'ID', 'GenderfemaleDummy',
                   'Marital StatussingleDummy', 'Work StatusnoneDummy',
                   'EducationBADummy', 'EducationPhDDummy', 'EducationMADummy',
                   'LocationEast CoastDummy', 'LocationMidwestDummy',
                   'LocationWest CoastDummy',  'LocationAlaskaDummy',
                   'LocationHawaiiDummy', 'Purchasing Decision-makersingleDummy',
                   'Purchasing Locationspecialty storesDummy',
                   'Purchasing LocationretailDummy', 'Purchasing LocationdiscountDummy',
                   'Purchasing Locationweb (ebay)Dummy', 'Technology AdoptionearlyDummy',
                   'Favorite featuretime shiftingDummy',
                   'Favorite featurecool gadgetDummy',
                   'Favorite featureschedule controlDummy',
                   'Favorite featureprogramming/interactive featuresDummy']

# Set the dependent variable
dependent_var = 'Electronic spending as % of income'

# Create the X (independent variables) and y (dependent variable) matrices
X = df_unstandarized[independent_vars]
y = df_unstandarized[dependent_var]

# Add a constant column to the X matrix
X = sm.add_constant(X)

# Fit the multiple regression model
model = sm.OLS(y, X)
results = model.fit()

# Print the regression summary
print(results.summary())


# In[35]:


import scipy.stats as stats

# Select the dummy variables and the dependent variable
dummy_vars = ['GenderfemaleDummy', 'Marital StatussingleDummy', 'Work StatusnoneDummy',
              'EducationBADummy', 'EducationPhDDummy', 'EducationMADummy',
              'LocationEast CoastDummy', 'LocationMidwestDummy',
              'LocationWest CoastDummy', 'LocationAlaskaDummy',
              'LocationHawaiiDummy', 'Purchasing Decision-makersingleDummy',
              'Purchasing Locationspecialty storesDummy',
              'Purchasing LocationretailDummy', 'Purchasing LocationdiscountDummy',
              'Purchasing Locationweb (ebay)Dummy', 'Technology AdoptionearlyDummy',
              'Favorite featuretime shiftingDummy',
              'Favorite featurecool gadgetDummy',
              'Favorite featureschedule controlDummy',
              'Favorite featureprogramming/interactive featuresDummy']

dependent_var = 'Electronic spending as % of income'

# Perform ANOVA or t-test
for var in dummy_vars:
    group_labels = df_unstandarized[var].unique()
    groups = [df_unstandarized[dependent_var][df_unstandarized[var] == label] for label in group_labels]
    f_value, p_value = stats.f_oneway(*groups)
    # Alternatively, for t-test:
    # t_stat, p_value = stats.ttest_ind(*groups)
    print(f"{var}: F-value = {f_value:.4f}, p-value = {p_value:.4f}")


# In[38]:


import numpy as np

# Compute R-squared
r_squared = results.rsquared
print(f"R-squared: {r_squared:.4f}")

# Compute eta-squared for ANOVA
total_ss = np.sum((y - np.mean(y))**2)
explained_ss = total_ss * r_squared
eta_squared = explained_ss / total_ss
print(f"Eta-squared: {eta_squared:.4f}")

