# CHICAGO CRIME ANALYSIS

This project explored the analysis of crime data sourced from Chicago, aiming to unveil intriguing insights into the city's criminal landscape. Through examination, three key inquiries guided this exploration:
1.	The frequency of crime distributed within Months, Days, Seasons.
2.	According to location description, where does crime happen the most?
3.	Did the Types of crime change as years go by?

### Data cleaning and feature engineering:
Dropping redundant columns: a redundant column is one that gives information that another column already explains: e.g. ID and Case number)
1. Unnamed is similar to the index of the DataFrame- dropping Unnamed
2. ID and Case Number are similar- dropping ID
3. X coordinate and Y coordinate AND Latitude and Longitude redundantly describe geographical location- Dropping location AND X and Y coordinates. Latitude and Longitude data are enough for our analysis
4. Community area and ward are similar to geographical subdivisions or clusters within the Chicago city, they will overlap at some point- Dropping community area

Handling missing data: From our data, Location description, Ward, Latitude, and Longitude are all missing one or more data which I handled as follows:
1.	Location Description: This refers to the type of location where the crime occurred such as on the street, pool room, residence etc., I will used the most common place to fill up the missing data.
2.	Ward: From viewing the rows with missing data in the ward column, it would make sense to also use the modal value to fill up missing values. I had doubts about using mode initially because I thought they might be clustered to a particular location and this might really affect the data in that location. They are dispersed as evidenced by the districts where the missing data are located so it’s okay to use mode.
3.	Latitude and Longitude: Taking a good look at our data info, the district data does not have any missing data and that is a very good thing because we can group our district data, generate measures of central tendency such as median, mean, or mode per district and use that to fill up our missing latitude and longitude data. The short summary is that latitude and longitude points to specific locations and districts would have latitude and longitude data that are very close because they are located in the same place.
Feature engineering: For the analysis I carried out on this data, I needed to get new features from existing ones. For instance, dataset has a data column that contains day, month, year, hours, minutes, seconds, and PM or AM. I used the column to get our Months, Days, and Season data and then, I added them to the dataframe.

### Conclusion of the project:
In assessing whether there have been shifts in the landscape of criminal activity over time, the analysis reveals that while the specific types of crimes have persisted, their occurrence has shown a notable decrease over the years. Focusing on theft, which emerges as the predominant offense, a discernible pattern emerges. Initially, theft rates exhibited a sharp incline, peaking in approximately 2005 at a frequency of approximately 70 instances, with slight fluctuations around this apex. However, subsequent years witnessed a gradual but consistent decline, with occurrences diminishing to approximately 10 past the year 2020.

Similar trends are observed across other categories of crime, with notable spikes occurring around the year 2005, followed by a parallel trajectory of decline. Ultimately, while the frequency of criminal incidents has evolved over time, the fundamental composition of criminal activities has remained largely consistent.
