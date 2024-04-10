import pandas as pd
from meteostat import Hourly
from datetime import datetime
import math



flights = pd.read_csv('flights.csv')
desired_airport = 'ORD'  # Filter data to be only departing at SFO

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

# print(flight_df[flight_df['DEPARTURE_DELAY'] < 1])





""" Weather Data """
start = datetime(2015, 12, 1, 00, 00) 
end = datetime(2015, 12, 29, 23, 59) # Year, Month, Day, Hour, Minute
tz = "America/Chicago"
data1 = Hourly('72530', start, end, tz) # '72537' is the code for DTW

data1 = data1.fetch()

""" Fixing the DateTime index to remove the timezone addition '--06:00' """
# If you want to name the new column that contains the old index values:
data1 = data1.reset_index()

# Ensure the 'time' column is treated as string
data1['time'] = data1['time'].astype(str)

# Now you can safely use .str accessor and perform the slice operation
remove_timezone = data1['time'].str.slice(0, 19)
data1['time'] = remove_timezone

# Convert the 'time' column to datetime
data1['time'] = pd.to_datetime(data1['time'])

# Set the 'time' column as the index of the DataFrame
data1 = data1.set_index('time')

# Filter out rows where all values are NaN
data1 = data1.dropna(how='all')
  
# Drop columns with all NaN values for data1
data1 = data1.dropna(axis=1, how='all')    
print("Weather Data")
print(data1)
print("-----------------------------------------------------------")


""" Merge the flight and weather data together. The merge is done through the column 'time' on each.
    Time includes the date and time. As the flight data includes multiple of the same hour the merge
    is supposed to keep the integrity of the data. I am not sure how correct this merge is I need to 
    look into it more and get second opinions."""
flight_df.set_index('time', inplace=True)
merged_df = pd.merge(flight_df, data1, on='time', how='inner')


merged_df = merged_df.drop(columns=['DAY_OF_WEEK', 'AIRLINE', 'FLIGHT_NUMBER',
       'TAIL_NUMBER', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
       'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME', 'DEPARTURE_DELAY', 'TAXI_OUT',
       'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'AIR_TIME', 'DISTANCE',
       'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME',
       'ARRIVAL_DELAY', 'DIVERTED', 'CANCELLED', 'CANCELLATION_REASON',
       'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
       'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY', 'coco'])

# print(merged_df)



''' Bayiesian Inference Portion. '''

""" Probability of delays calculation """
delayed = merged_df[merged_df['result'] == 1]
delayed_count = delayed.shape[0]

count_total = merged_df.shape[0]
probability_delays = delayed_count/count_total
print("Probability of delays", delayed_count/count_total)




# Probability of high wind speed 41km/h
wind_weather_delays = merged_df[(merged_df['wspd'] > 30) & (merged_df['result'] == 1)]
wind_delays_count = wind_weather_delays.shape[0]

wind_weather = merged_df[(merged_df['wspd'] > 30)]
wind_count = wind_weather.shape[0]

proabability_wind_delays = wind_delays_count/count_total
log_probability_wind_delays = math.log(proabability_wind_delays) 

# Calculate probability of wind
probability_wind = wind_count / count_total

# Log of probability of wind
log_probability_wind = math.log(probability_wind)

# Correct calculation of log of probability of delays given wind
log_probability_delay_given_wind = log_probability_wind_delays - log_probability_wind

probability_delay_given_wind = math.exp(log_probability_delay_given_wind)
print("Probability of delays given high winds:", probability_delay_given_wind)






# Probability of low temp delays
temp_delays = merged_df[(merged_df['temp'] < 0) & (merged_df['result'] == 1)]
temp_delays_count = temp_delays.shape[0]

temp = merged_df[(merged_df['temp'] < 0)]
temp_count = temp.shape[0]

proabability_temp_delays = temp_delays_count/count_total
log_probability_temp_delays = math.log(proabability_temp_delays)

# Calculate probability of low temperature
probability_low_temp = temp_count / count_total

# Log of probability of low temperature
log_probability_low_temp = math.log(probability_low_temp)

# Correct calculation of log of probability of delays given low temperature
log_probability_delay_given_lowtemp = log_probability_temp_delays - log_probability_low_temp

probability_delay_given_lowtemp = math.exp(log_probability_delay_given_lowtemp)


print("Probability of delays given low temperature:", probability_delay_given_lowtemp)





# Probability of rain delays
rain_delays = merged_df[(merged_df['prcp'] > 2) & (merged_df['temp'] > 2) & (merged_df['result'] == 1)]
rain_delays_count = rain_delays.shape[0]

# Instances of rain
rain = merged_df[(merged_df['prcp'] > 2) & (merged_df['temp'] > 2)]
rain_count = rain.shape[0]

# Calculating the probabilities
probability_rain_delays = rain_delays_count / count_total
probability_rain = rain_count / count_total

# Converting probabilities to logarithms
log_probability_rain_delays = math.log(probability_rain_delays)
log_probability_rain = math.log(probability_rain)

# Calculating the log of the probability of delays given rain
log_probability_delay_given_rain = log_probability_rain_delays - log_probability_rain

# Converting the log probability back to a regular probability for interpretation
probability_delay_given_rain = math.exp(log_probability_delay_given_rain)

print("Probability of rain", probability_rain)
print("Probability of delays given rain", probability_delay_given_rain)


# Probability of snow
# Count of delays when there is snow
snow_delays = merged_df[(merged_df['prcp'] > 0.5) & (merged_df['temp'] <= 2) & (merged_df['result'] == 1)]
snow_delays_count = snow_delays.shape[0]

# Count of snow occurrences
snow = merged_df[(merged_df['prcp'] > 0.5) & (merged_df['temp'] <= 2)]
snow_count = snow.shape[0]

# Calculating the probabilities
probability_snow_delays = snow_delays_count / count_total
probability_snow = snow_count / count_total

# Converting probabilities to logarithms
log_probability_snow_delays = math.log(probability_snow_delays)
log_probability_snow = math.log(probability_snow)

# Calculating the log of the probability of delays given snow
log_probability_delay_given_snow = log_probability_snow_delays - log_probability_snow

# Converting the log probability back to a regular probability for interpretation
probability_delay_given_snow = math.exp(log_probability_delay_given_snow)

print("Probability of snow", probability_snow)
print("Probability of delays given snow", probability_delay_given_snow)



# Probability of fog

# Count of delays when there is fog
fog_delays = merged_df[(merged_df['rhum'] >= 95) & (abs(merged_df['temp'] - merged_df['dwpt']) < 2.5) 
                        & (merged_df['wspd'] < 6) & (merged_df['result'] == 1)]
fog_delays_count = fog_delays.shape[0]

# Count of fog occurrences
fog = merged_df[(merged_df['rhum'] >= 95) & (abs(merged_df['temp'] - merged_df['dwpt']) < 2.5) 
                        & (merged_df['wspd'] < 6)]
fog_count = fog.shape[0]

# Calculating the probabilities
probability_fog_delays = fog_delays_count / count_total
probability_fog = fog_count / count_total

# Converting probabilities to logarithms
log_probability_fog_delays = math.log(probability_fog_delays)
log_probability_fog = math.log(probability_fog)

# Calculating the log of the probability of delays given fog
log_probability_delay_given_fog = log_probability_fog_delays - log_probability_fog

# Converting the log probability back to a regular probability for interpretation
probability_delay_given_fog = math.exp(log_probability_delay_given_fog)

print("Probability of fog", probability_fog)
print("Probability of delays given fog", probability_delay_given_fog)


'''Bayes nets - show dependencies'''

# P(Delay | Wind, Rain) = P(Wind, Rain, Delay) / P(Wind) P(Rain | Wind)
# P(Rain∣Wind) = P(rain, wind)/ P(wind)

"""Have conditions for if there is no rain so you are not dividing by 0"""
# Probability of delay given rain and wind
probability_wind_rain_delay = (merged_df[(merged_df['wspd'] > 30) & (merged_df['prcp'] > 2) & (merged_df['temp'] > 2) & (merged_df['result'] == 1)]).shape[0]/count_total
probability_rain_wind = (merged_df[(merged_df['wspd'] > 30) & (merged_df['prcp'] > 2) & (merged_df['temp'] > 2)]).shape[0]/count_total
probability_rain_given_wind = probability_rain_wind/probability_wind
probability_delay_given_rain_wind = probability_wind_rain_delay/ (probability_wind * probability_rain_given_wind)
print("Probability of delay given rain and wind: ", probability_delay_given_rain_wind)


# Probability of delay given snow and wind
probability_wind_snow_delay = (merged_df[(merged_df['wspd'] > 30) & (merged_df['prcp'] > 2) & (merged_df['temp'] <= 2) & (merged_df['result'] == 1)]).shape[0]/count_total
probability_snow_wind = (merged_df[(merged_df['wspd'] > 30) & (merged_df['prcp'] > 2) & (merged_df['temp'] <= 2)]).shape[0]/count_total
probability_snow_given_wind = probability_snow_wind/probability_wind
probability_delay_given_snow_wind = probability_wind_snow_delay/ (probability_wind * probability_snow_given_wind)
print("Probability of delay given snow and wind: ", probability_delay_given_snow_wind)

# Probability of delay given rain and fog
probability_fog_rain_delay = (merged_df[(merged_df['rhum'] >= 95) & (abs(merged_df['temp'] - merged_df['dwpt']) < 2.5) 
                        & (merged_df['wspd'] < 6) & (merged_df['result'] == 1) & (merged_df['prcp'] > 2) & (merged_df['temp'] > 2)]).shape[0]/count_total
probability_rain_fog = (merged_df[(merged_df['rhum'] >= 95) & (abs(merged_df['temp'] - merged_df['dwpt']) < 2.5) 
                        & (merged_df['wspd'] < 6) & (merged_df['prcp'] > 2) & (merged_df['temp'] > 2)]).shape[0]/count_total
probability_rain_given_fog = probability_rain_fog/probability_fog
probability_delay_given_rain_fog = probability_fog_rain_delay/ (probability_fog * probability_rain_given_fog)
print("Probability of delay given fog and rain: ", probability_delay_given_rain_fog)



""" User Input Predictions """

