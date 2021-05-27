# CapstoneProject

This projects aims to enrich the US I94 immigration data with further data such as US airport data, US demographics and temperature data to have a wider basis for analysis on the immigration data.

## Data sources

### I94 Immigration Data
This data comes from the US National Tourism and Trade Office. A data dictionary is included in the workspace. [This](https://travel.trade.gov/research/reports/i94/historical/2016.html) is where the data comes from. There's a sample file so you can take a look at the data in csv format before reading it all in.

### World Temperature Data
This dataset came from Kaggle. You can read more about it [here](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).

### U.S. City Demographic Data
This data comes from OpenSoft. You can read more about it [here](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).

### Airport Code Table
This is a simple table of airport codes and corresponding cities. It comes from [here](https://datahub.io/core/airport-codes#data).

## Data cleaning

* Filter temperature data to only use US data.
* Remove columns with missing values and columns not important for analysis from I94 file.
* Get the Port Code, Name and State info from I94 Label Metadata file.
* Drop rows with missing IATA codes from airport codes file. We need the IATA codes to join the data with other sources.
* Drop missing row values from Temperature data file
* Only keep total population for cities in us-cities-demographics.csv file

## Conceptual Data Model

We will leverage a Star Schema creating a Fact Table with Multiple Dimensions with Fact Table created using I94 Immigration data & airport, weather and demographics as dimensions. This would allow us to run OLAP queries with the key fact table provided COUNT of immigrants and joining with dimension tables using Port Code for the Port of Entry of Immigrants. The reasoning behind using immigrations data as a Fact table is we want to keep the COUNT of Immigrants entering the country as a key measure or Fact to report on. The demographics of cities, weather of cities & airport information describe attributes of the airports, cities & weather of cities visited.

Using the data model above, we can answer for use case such as finding the Proportion of immigrants to Population entering different cities on Visas. This would allow the analyst to understand which cities are popular destination points of arrival. We can join i94 data with demographics data using Port Code to get number of immigrants arrive in a city compared to population of city, thereby, understanding which communities have higher proportion of visitors than locals. 

### Tables:
| table name | columns | description | type |
| ------- | ---------- | ----------- | ---- |
| airports | iata_code - name - type - local_code - coordinates - city | stores information related to airports | dimension table |
| demographics | city - state - media_age - male_population - female_population - total_population - num_veterans - foreign_born - average_household_size - state_code - race - count | stores demographics data for cities | dimension table |
| immigrations | cicid - year - month - cit - res - iata - arrdate - mode - addr - depdate - bir - visa - coun- dtadfil - visapost - occup - entdepa - entdepd - entdepu - matflag - biryear - dtaddto - gender - insnum - airline - admnum - fltno - visatype | stores all i94 immigrations data | fact table |
| temperature | timestamp - average_temperature - average_temperatur_uncertainty - city - country - latitude - longitude | stores temperature information | dimension table |

#### Fact Table -
This will contain information from the I94 immigration data for different ports

Columns:

i94yr = 4 digit year; 
i94mon = numeric month; 
i94cit = 3 digit code of origin city; 
i94res = 3 character code of destination city; 
i94port = 3 character code of destination city; 
arrdate = arrival date; 
i94mode = 1 digit travel code; 
i94addr = State; 
depdate = departure date; 
i94bir = Age of Respondent in Years; 
i94visa = reason for immigration; 
count = Count Summary; 
matflag = Match of arrival and departure records; 
biryear = 4 digit year of birth; 
airline = Airline used to arrive in U.S.; 
admnum = Admission Number; 
fltno = Flight number of Airline used to arrive in U.S.; 
visatype = Class of admission legally admitting the non-immigrant to temporarily stay in U.S.; 
port_code = Port Code; = connect to port_code for Fact table join;REFERENCE KEY
port_city = Port City; 
port_state = Post State

#### Dimensions -

##### Demographic data = Population of destination city. This will contain data from demographic data.

##### Columns:

City; 
State; 
Median Age; 
Male Population; 
Female Population; 
Total Population; 
Number of Veterans; 
Foreign-born; 
Average Household Size; 
State Code; 
port_code = connect to port_code for Fact table join;REFERENCE KEY
port_city; 
port_state

##### Airport data = Airport information of destination city. This will contain data from airport data.

##### Columns:

iata_code = connect to port_code for Fact table join; 
name; 
type; 
local_code; 
coordinates;
port_code = connect to port_code for Fact table join;REFERENCE KEY
port_city; 
elevation_ft; 
continent; 
iso_country; 
iso_region; 
municipality; 
gps_code

##### Temperature data = Temperatue information of destination city. This will contain data from temperature data.

##### Columns:

dt = Date; 
AverageTemperature; 
AverageTemperatureUncertainty; 
City; 
Country; 
Latitude; 
Longitude; 
port_code = connect to port_code for Fact table join; REFERENCE KEY
port_state; 
Year; 
Month; 

### Table decision

We want to have the immigrations data to store the key information & then enrich the data with airports, demographics and temperature data. We use the Port Code / City information to join the Fact table with dimension tables efficiently.

The reasoning behind using immigrations data as a Fact table is we want to keep the COUNT of Immigrants entering the country as a key measure or Fact to report on. The demographics of cities, weather of cities & airport information describe attributes of the airports, cities & weather of cities visited. One use case is finding the Proportion of immigrants to Population entering different cities on Visas. This would allow the analyst to understand which cities are popular destination points of arrival. 

The fact tables can be joined with dimension tables using port_code column. 


## Data Use

The data model will be used by Analysts to query the immigration statistics (Fact) for US that can be appended with airports the immigrants travel via, type of cities they frequent to and weather conditions of such US cities(Dimensions). 

## Example use case 

A use case could be find the cities with the highest proportion of travellers to the population of city that can easily be derived using the i94 fact table and demographic dimension data model using the above data model created. 

## Mapping Out Data Pipelines

1. Create fact and dimension tables.
2. Insert data.
3. Join fact to dimension tables using Port Code / City data.

## Choice of tools and technologies for the project

For this project, we used Python DataFrames for ingesting the limited data from files provided since it can easily handle multiple file formats such as SAS, csv, so on. Inputs were converted into python dataframe and then manipulated to come up with Facts & Dimension tables for OLAP reporting.

We can leverage Spark Dataframes in case the files are large but is not used in the current scenario. 

## How often the data should be updated and why

The data can be updated daily as we are processing the data in i94 immigrations data at daily level.

## FAQ: What would I do if...
* The data was increased by 100x.
  * Utilize tools such as AWS EMR & Spark to process the data
* The data populates a dashboard that must be updated on a daily basis by 7am every day.
  * Use airflow to set up data refresh schedules so jobs are complete before 7 AM every day. Have data quality and data load failure checks so the team is informed by email if any such issue arises and can be fixed
* The database needed to be accessed by 100+ people.
  * Use Amazon Redshift or No SQL Database such as Cassandra since these have auto-scaling capabilities and good read performance
