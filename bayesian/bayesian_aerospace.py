from datetime import datetime
import pandas as pd
from meteostat import Hourly
import pymc3 as pm
from sklearn.model_selection import train_test_split


flights = pd.read_csv('flights.csv')
desired_airport = 'SFO'  # Filter data to be only departing at SFO

# Filter the DataFrame to include only rows where the airport column matches the desired airport code
flight_df = flights[flights['ORIGIN_AIRPORT'] == desired_airport]

# Only consider data that has values for departure delay.
flight_df = flight_df[flight_df['DEPARTURE_DELAY'].notna()]

""" Create column that determines whether flight has a departure delay. If the departure delay is greater
 than 15 it is significant enough to be classified as a delay (this number can be changed). """
result=[]
for row in flight_df['DEPARTURE_DELAY']:
  if row > 15:
    result.append(1)
  else:
    result.append(0)  

flight_df['result'] = result


"""Modify the date and time format to be the same as the weather date and time. 
 This will make merging the datasets possible"""

# The time input is 24h time but does not have a consitant length. This fills the time with 
# zeros so that it is able to be split into hour and minute.
flight_df['DEPARTURE_TIME'] = flight_df['DEPARTURE_TIME'].astype(int).astype(str).str.zfill(4)

# Extract hour and minute as integers
hour = flight_df['DEPARTURE_TIME'].str.slice(0, 2).astype(int)
minute = flight_df['DEPARTURE_TIME'].str.slice(2, 4).astype(int)

# Round hour to the nearest hour. Weather data is by hour, flight is more exact and involves minutes.
flight_df['rounded_hour'] = round(hour + minute / 60)

# Create 'time' column. This is standard date time format which corresponds to weather date and time.
flight_df['time'] = pd.to_datetime(flight_df[['YEAR', 'MONTH', 'DAY']]) + pd.to_timedelta(flight_df['rounded_hour'], unit='h')

"""These functions classify storm sevarity and visability with an integer ranking. These
    need to be ajusted, they are not accurate. There was a lot of issues with data consistancy and 
    missing values."""

def classify_storm_sevarity(row):
    storm_index = 0  # Initialize storm severity index

    # Check wind speed
    if row['wspd'] >= 40:
        storm_index += 2
    elif row['wspd'] >= 30:
        storm_index += 1

    # # Check peak wind gust
    # if row['wpgt'] >= 60:
    #     storm_index += 2
    # elif row['wpgt'] >= 40:
    #     storm_index += 1

    # Check precipitation
    if row['prcp'] > 0:
        storm_index += 2

    elif storm_index <= 1:
        return 0
    elif 2 <= storm_index <= 3:
        return 1
    elif 4 <= storm_index <= 5:
        return 2
    elif 6 <= storm_index <= 7:
        return 3
    elif 8 <= storm_index <= 9:
        return 4
    else:
        return 5


def visability_classification(row):
    # Define thresholds and play around with it. Percipitation is in mm, drewpoint temp close is in Celcius.
    heavy_precipitation_threshold = 30
    moderate_precipitation_threshold = 12.5
    dewpoint_temperature_close = 4

    if row['prcp'] > heavy_precipitation_threshold:  # Define this threshold as appropriate
        # Low
        return 0

    # elif abs(row['temp'] - row['dwpt']) <= dewpoint_temperature_close:  # Define this threshold
    #     return 0
    elif row['prcp'] > moderate_precipitation_threshold:  # Define this threshold
        # Moderate
        return 1
    else:
        # High
        return 2

# Random Dates of weather data that will be added. 
intervals = [[2, 5, 2015], [7, 5, 2015], [8, 5, 2015],[11, 5, 2015], [10, 6, 2015], [2, 7, 2015]]

# Create an empty DataFrame to store the weather data and classifications
combined_data = pd.DataFrame()

for i in intervals:
    start = datetime(2015, i[0], i[1]) 
    end = datetime(2015, i[0], (i[1] + 1), 23, 59) # Year, Month, Day, Hour, Minute
    data = Hourly('72494', start, end) # '72494' is the code for SFO
    data = data.fetch()
    data['s'] = data.apply(classify_storm_sevarity, axis=1)
    data['v'] = data.apply(visability_classification, axis=1)
    combined_data = pd.concat([combined_data, data])


weather_data_dropped = combined_data.drop(['temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres',
       'tsun', 'coco'], axis=1)

""" Merge the flight and weather data together. The merge is done through the column 'time' on each.
    Time includes the date and time. As the flight data includes multiple of the same hour the merge
    is supposed to keep the integrity of the data. I am not sure how correct this merge is I need to 
    look into it more and get second opinions."""
flight_df.set_index('time', inplace=True)
merged_df = pd.merge(flight_df, weather_data_dropped, on='time', how='outer')
non_nan_rows = merged_df[((~merged_df['v'].isna()) | (~merged_df['s'].isna()) )& (~merged_df['result'].isna())]


# Split the data into training and testing sets
X = non_nan_rows[['s', 'v']]
y = non_nan_rows['result']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Define Bayesian logistic regression model.
with pm.Model() as logistic_model:
    # Priors
    beta0 = pm.Normal('beta0', mu=0, sd=10, testval=0) # Intercept
    beta_storm_severity = pm.Normal('beta_storm_severity', mu=0, sd=10, testval=0)
    beta_visibility = pm.Normal('beta_visibility', mu=0, sd=10, testval=0)
    
    # Linear combination of predictors
    eta = beta0 + beta_storm_severity * X_test['s'] + beta_visibility * X_test['v']
    
    # Logistic transformation
    p = pm.Deterministic('p', 1 / (1 + pm.math.exp(-eta)))
    
    # Likelihood
    outcome = pm.Bernoulli('outcome', p=p, observed=y_test)
    
    # Sampling without parallelization
    trace = pm.sample(2000, cores=1)
    pm.traceplot(trace, ['beta0', 'beta_storm_severity', 'beta_visibility'])
    plt.show()

   