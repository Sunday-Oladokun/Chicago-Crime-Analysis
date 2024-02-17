#!/usr/bin/env python
# coding: utf-8

# #### OBJECTIVES: Using the Chicago Crime Dataset, perfoRm the following data preparation steps:
# 
# 1. Use a funtion to Drop redundant columns (a redundant colum is one that gives infromation that another column already explains: eg ID and Case number) 
# 2. Use functions to create new columns for Months, Day, Season.
# 3. Use subsetting and grouping to show how the frequency of crime is distributed within Months, Days, Seasons with the most crime record and what crimes are highest and lowest?
# 4.  According to location description, where does crime hapen the most?
# 5.  Did the Types of crime change as years go by? if yes/no. let the data show the insight.

# In[2]:


# Import pandas package 
import pandas as pd
 
# Read the data into the environment
dataset = pd.read_csv("chicago2.csv")

# Inspect the first 10 rows
dataset.head(10)


# In[3]:


# Check the columns of the data
dataset.columns


# In[4]:


# Check for the brief overview of the dat
dataset.info()


# In[5]:


# Check the dimensions of the data
dataset.shape


# ### 1. Use a funtion to Drop redundant columns (a redundant colum is one that gives infromation that another column already explains: eg ID and Case number) 

# Dropping redundant columns
# 1. Unnamed is similar to the index of the dataframe- dropping Unnamed
# 2. ID and Case Number are similar- dropping ID
# 3. X coordinate and Y coordinate AND Latitude and Longitude redundantly describe geographical location- Dropping location AND X and Y coordinates
# 4. Community area and ward are similar to geographical subdivisions or clusters within the city, they might overlap at some point- Dropping community area

# In[6]:


dataset.drop(["Unnamed: 0", "ID", "Location", "Community Area", "X Coordinate", "Y Coordinate"], axis=1, inplace=True)


# In[7]:


dataset.head()


# Before we proceed to answer other questions or do feature engineering to create columns we need, let us handle missing values first.
# 
# From our data, Location description, Ward, Latitude, and Longitude are all missing one or more data which we would handle

# In[8]:


dataset.isna().sum()


# Handling Location Description missing data
# 
# Location Description refers to the type of location where the crime occurred such as on the street, pool room, residence etc, I will be using the most common place to fill up the missing data

# In[9]:


# Examine the missing data
dataset[dataset["Location Description"].isna()]


# In[10]:


# Get mode and subset first value in the series
most_frequent_LD = dataset["Location Description"].mode()[0]

# Assign the mode to the missing value
dataset["Location Description"] = dataset["Location Description"].fillna(most_frequent_LD)


# In[11]:


dataset.isna().sum()


# Handling Ward missing data
# 
# From viewing the rows with missing data in the ward column, it would make sense to also use the modal value to fill up missing values. I had doubts about using mode initially because I thought they might be clustered to a particular location and this might really affect the data in that location. They are dispersed as evidenced by the districts where the missing data are located so its okay to use mode.

# In[12]:


# View the rows with missing ward data
dataset[dataset["Ward"].isna()]


# In[13]:


# Get mode and subset first value in the series
mode_ward = dataset["Ward"].mode()[0]

# Assign modal value to ward
dataset["Ward"] = dataset["Ward"].fillna(mode_ward)


# In[14]:


dataset.isna().sum()


# Handling Latitude and Longitude missing data
# 
# Taking a good look at our data info above, the district data does not have any missing data and that is a very good thing because we can group our district data, generate measures of central tendency such as median, mean, or mode per district and use that to fill up our missing latitude and longitude data.
# 
# The short summary is that latitude and longitude points to specific locations and districts would have latitude and longitude data that are very close because they are located in the same place.

# In[15]:


# Let's see the unique values in our district data
dataset["District"].unique()


# In[16]:


# Define a function that fills the longitude and latitude data with median values
def fill_long_lat(x):
    x = x.fillna(x.median())
    return x


# In[17]:


dataset["Longitude"] = dataset.groupby("District", group_keys=False)["Longitude"].apply(fill_long_lat)
dataset["Latitude"] = dataset.groupby("District", group_keys=False)["Latitude"].apply(fill_long_lat)


# In[18]:


dataset.isna().sum()

# Finally, we have handled all missing data


# ### 2. Use functions to create new columns for Months, Day, Season.

# Our dataset has a data column that contains day, month, year, hours, minutes, seconds, and PM or AM. We will be using this column to get our Months, Day, and Season data

# In[19]:


from datetime import datetime

def extract_months(date):
    date_column = pd.to_datetime(date, format='%m/%d/%Y %I:%M:%S %p')
    months = date_column.dt.month_name()
    return months

def extract_day_of_week(date):
    date_column = pd.to_datetime(date, format='%m/%d/%Y %I:%M:%S %p')
    day_of_week = date_column.dt.day_name()
    return day_of_week


# In[20]:


dataset["Month"] = extract_months(dataset["Date"])
dataset["Day"] = extract_day_of_week(dataset["Date"])


# In[21]:


def assign_season(month):
    if month in ["January", "February", "December"]:
        return "Winter"
    elif month in ["March", "April", "May"]:
        return "Spring"
    elif month in ["June", "July", "August"]:
        return "Summer"
    else:
        return "Fall"

# Assuming dataset is a DataFrame with a column "Month"
dataset["Season"] = dataset["Month"].apply(assign_season)


# In[22]:


dataset.head(2)


# ### 3. Use subsetting and grouping to show how the frequency of crime is distributed within Months, Days, Seasons with the most crime record and what crimes are highest and lowest?

# We could approach this in two ways:
# 
# 1. Group by the primary type which talks about type of crime and subset the months, days, and seasons which would give us three separate series
# 
# 2. Group by the primary type and subset months, days, and seasons which would return a single series

# In[23]:


# Approach 1
crime_freq_month = dataset.groupby("Primary Type")[["Month"]].value_counts()
crime_freq_day = dataset.groupby("Primary Type")[["Day"]].value_counts()
crime_freq_season = dataset.groupby("Primary Type")[["Season"]].value_counts()


# In[24]:


# frequency of crime distribution by month
crime_freq_month.sort_values(ascending=False)


# In[25]:


# frequency of crime distribution by day
crime_freq_day.sort_values(ascending=False)


# In[26]:


# frequency of crime distribution by season
crime_freq_season.sort_values(ascending=False)


# In[27]:


# Approach 2
# frequency of crime distribution by Month, Day, and Season
crime_freq_month_day_season = dataset.groupby("Primary Type")[["Month", "Day", "Season"]].value_counts()


# In[28]:


crime_freq_month_day_season.sort_values(ascending=False)


# ### 4.  According to location description, where does crime happen the most?

# In[29]:


crime_rate_by_location = dataset["Location Description"].value_counts()


# In[30]:


crime_rate_by_location.sort_values(ascending=False)


# ### 5.Did the Types of crime change as years go by? if yes/no. let the data show the insight.

# In[31]:


crime_yearly_trend = dataset.groupby("Year")["Primary Type"].value_counts()


# In[32]:


crime_yearly_trend


# In[33]:


import matplotlib.pyplot as plt

# Unstack the data generated by the groupby to transform the hierarchical index gotten into a convenient tabular day for plotting
crime_yearly_trend = dataset.groupby("Year")["Primary Type"].value_counts().unstack()

# Using the stacked area plot to visualize the data
crime_yearly_trend.plot(kind='area', stacked=True, figsize=(10, 6))

# Set plot title
plt.title('Yearly Trend of Crimes')

# Set axis titles
plt.xlabel('Year')
plt.ylabel('Number of Crimes')

# Set the legend since to differentiate the categories visaully
plt.legend(title='Crime Type', bbox_to_anchor=(1.05, 1), loc='upper left')

# Show the plot
plt.show()


# In assessing whether there have been shifts in the landscape of criminal activity over time, the analysis reveals that while the specific types of crimes have persisted, their occurrence has shown a notable decrease over the years. Focusing on theft, which emerges as the predominant offense, a discernible pattern emerges. Initially, theft rates exhibited a sharp incline, peaking in approximately 2005 at a frequency of approximately 70 instances, with slight fluctuations around this apex. However, subsequent years witnessed a gradual but consistent decline, with occurrences diminishing to approximately 10 past the year 2020.
# 
# Similar trends are observed across other categories of crime, with notable spikes occurring around the year 2005, followed by a parallel trajectory of decline. Ultimately, while the frequency of criminal incidents has evolved over time, the fundamental composition of criminal activities has remained largely consistent.

# In[ ]:




