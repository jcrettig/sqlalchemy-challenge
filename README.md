# sqlalchemy-challenge

Project Setup 

Created SQLAlchemy-Challenge repository in GitHub and cloned repository to my computer.
Added files provided for this assignment to the repository on my computer and git pushed the updated directory to GitHub.

Step 1 - Climate Analysis and Exploration
For this portion of the project I used SQLAlchemy ORM queries, Pandas and Matplotlib in Jupyter Notebooks.
My work for this section is located in the repository as follows:
climate_starter.ipynb – located in the main repository
hawaii.sqlite – located in the Resources folder
pngs of the charts I created are located in the Output folder
Other preparatory steps I performed are described in the “Reflect Tables into SQLAlchemy ORM” section of climate_starter.ipynb
Exploratory Precipitation Analysis
First I inspected both of the tables that make up the Hawaii database – measurement table and station table
Performed a query to determine the most recent date in the measurement table – 8/23/2017
Using the Datetime tool, I computed the date one year prior to 8/23/2017.  
Performed a query on the measurement table to pull all dates and precipitation scores 
Saved the query to a Dataframe with the date column as the index and sorted in ascending order by date.
Grouped the DataFrame data by date and determined the maximum precipitation by date
Using Matplotlib, I charted the data in the grouped DataFrame to a bar chart.  
In order to present the dates in the chart in the desired format along the x-axis, I had to convert the dates using datetime to a date format
Completed the bar chart by setting up all of the bar chart attributes
Wrapped up this section by calculating the summary statistics both for the entire data set and for the most recent 12 months data set.  

Observations about the precipitation data – It appears that the recent 12 months subset was overall representative of the entire data set.  The mean, standard deviation and min of the full data set and the 12 months subset were all very close to each other.  The max of the full data set was nearly double of the max in the 12 months subset, but seems to be more of an outlier than representative of the entire data set.  

Exploratory Station Analysis
Designed a query to calculate the total number of stations in the stations and measurements datasets – 9 unique stations in both
Determined that station USC00519281 is the most active station
Performed queries to determine the maximum, minimum and average temperatures for station USC00519281.  
Queried the temperature data to get the last 12 months of temperature measurements.
Created a DataFrame from the temperature query.  
Created a histogram from the DataFrame 

Observations of the Temperature data – The ranges of temperatures where most of the data fall is relatively tight with only a 10 degree change in the range of 70 degrees to 80 degrees.  The highest frequency is in the upper mid-70’s but the data immediately above and below the max is pretty significant.  Once you get below 70 degrees it almost appears that these data points are outliers.  

I am a little surprised that the average temperature as computed in the queries is only 71.7 degrees, given the higher measurement frequencies falling more in the mid-70’s range.  

Step 2 – Climate App
For this portion of the project I used a Flask API and utilized VS Code to perform the work.
My file for this section is called app.py and is located in the main section of the sqlalchemy-challenge repository.  
My initial set up included the imports and the database and Flask set ups
Created a home route that included instructions to launch the other routes.  The following is a picture of a portion of the results

 

Created a precipitation route
In this route I create a query to retrieve the last 12 months of precipitation data which I then converted to a dictionary using the date as the key.  I then JSONified the results. The following is a picture of a portion of the results

 

Created a stations route
Performed a query to present all of the Station information and then JSONified the query. The following is a picture of a portion of the results

 

Created a tobs route
For this route I queried the dates and temperature observations of the most active station for the previous year and then JSONified the query. The following is a picture of a portion of the results

 

Created a max_min_avg temperature route
Created an interactive query that requested date ranges and provided a default end date if the user does not want to input an end date
Upon complete of the user entering their responses, query determined a minimum, average and maximum temperature for the previous year at the most active station.
The min, max and average results were then JSONified. The following is a picture of a portion of the results

 








