import pandas as pd
import pvlib
from pvlib.location import Location
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt

"""timezone = "Europe/Copenhagen"
start_date = "2024-04-1"
end_date = "2024-04-30"
delta_time = "Min"  # "Min", "H", 

# Definition of Location object. Coordinates and elevation of Amager, Copenhagen (Denmark)
site = Location(
    55.660439, 12.604980, timezone, 10, "Amager (DK)"
)  # latitude, longitude, time_zone, altitude, name

# Definition of a time range of simulation
times = pd.date_range(
    start_date + " 00:00:00", end_date + " 23:59:00", freq=delta_time, tz=timezone
)




# Estimate Solar Position with the 'Location' object
sunpos = site.get_solarposition(times)

# Visualize the resulting DataFrame
#print(sunpos.head())



import matplotlib.dates as mdates

chosen_date = "2024-04-20"

# Plots for solar zenith and solar azimuth angles
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))
fig.suptitle("Solar Position Estimation in " + site.name + chosen_date)

# plot for solar zenith angle
ax1.plot(sunpos.loc[chosen_date].zenith)
ax1.set_ylabel("Solar zenith angle (degree)")
ax1.set_xlabel("Time (hour)")
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%H"))

# plot for solar azimuth angle
ax2.plot(sunpos.loc[chosen_date].azimuth)
ax2.set_ylabel("Solar azimuth angle (degree)")
ax2.set_xlabel("Time (hour)")
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%H"))
#plt.show()

# print("start here", (max(sunpos.loc[chosen_date].apparent_elevation)))"""

def elevation_max(date, latitude, longitude, frequency, timezone, altitude, location_name):
    
    times = pd.date_range(date + " 00:00:00", date + " 23:59:00", freq=frequency, tz=timezone)

    site = Location(latitude, longitude, timezone, altitude, str(location_name))

    sunpos = site.get_solarposition(times)

    return (max(np.array(sunpos.loc[date].apparent_elevation)))

print(elevation_max("2024-06-20", 55.785469, 12.519103, "H", "Europe/Copenhagen", 21, "Amager DK"))
print('done') 

