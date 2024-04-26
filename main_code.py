from panelpy import *
import pyfiglet

RED = "\33[91m"
BLUE = "\33[94m"
GREEN = "\033[32m"
YELLOW = "\033[93m"
PURPLE = '\033[0;35m' 
CYAN = "\033[36m"
END = "\033[0m"

BOLD = "\033[1m"
RESET_BOLD = "\033[22m"

print(f"{END}")
print(f"""
      {PURPLE}
 ██████╗ ██████╗ ████████╗██╗      ██████╗  █████╗ ███╗   ██╗███████╗██╗     
██╔═══██╗██╔══██╗╚══██╔══╝██║      ██╔══██╗██╔══██╗████╗  ██║██╔════╝██║     
██║   ██║██████╔╝   ██║   ██║█████╗██████╔╝███████║██╔██╗ ██║█████╗  ██║     
██║   ██║██╔═══╝    ██║   ██║╚════╝██╔═══╝ ██╔══██║██║╚██╗██║██╔══╝  ██║     
╚██████╔╝██║        ██║   ██║      ██║     ██║  ██║██║ ╚████║███████╗███████╗
 ╚═════╝ ╚═╝        ╚═╝   ╚═╝      ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝                                                                         
{CYAN}-------------------------------------------------------------------------------------------------                                    
""")
print(f"{BOLD}Opti-panel computes the solar panel angle that generate the most energy, given a location.")
print("Provide your decimal latitude and your altitude and get the optimal angle to install your panel !{RESET_BOLD}", "\n")
print(f"-------------------------------------------------------------------------------------------------\n{END}")

first_time = True

# Invalid and out of range inputs handling:
while True:
    try:
        if first_time:
            user_input = input(f"{END}Enter your {BLUE}Latitude{END} as a float: {BLUE}")
            latitude = float(user_input)

        if latitude >= -90 and latitude <= 90:
            break
        
        first_time = False
        user_input = input(f"{END}latitude out of range, please reenter your {BLUE}Latitude{END} again: {BLUE}")
        latitude = float(user_input)

    except ( TypeError, ValueError ):
        first_time = False
        while True:
            if user_input[:6] == "python":
                exit()
            try:
                user_input = input(f"{END}Bad input, please reenter your {BLUE}Latitude{END} again: {BLUE}")
                latitude = float(user_input)
                break
            except ( TypeError, ValueError ):
                continue

print("\n")
while True:
    try:
        user_input = input(f"{END}Enter your {CYAN}Altitude{END} as a float: {CYAN}")
        altitude = float(user_input)
        break

    except ( TypeError, ValueError ):
        while True:
            if user_input[:6] == "python":
                exit()
            try:
                user_input = input(f"{END}Bad input, please reenter your {CYAN}Altitude{END} again: {CYAN}")
                altitude = float(user_input)
                break
            except ( TypeError, ValueError ):
                continue

print(f"{END}")

print(f"\r\nYou entered this latitude: {BLUE}{latitude}{END} and this altitude: {CYAN}{altitude}{END}\n")

# Here we setup the time range over which we will compute the energy production
# We are calculating energy production over 365.25 days.
# The .25 day is to account for bissextile years
#
# To accheive this, we are first computing the energy production of a non bissextile year
# We then add 1/4 of the 02/29/2024 energy production to the total, because 2024 is a bissextile year.
# The total represents the average yearly production of the solar panel

start_date = "2023-01-01"
end_date = "2023-12-31"
extra_day = "2024-02-29"
delta_time = "H"  # "Min", "H",

if latitude < 0:
    azimuth_panel = 0
else:
    azimuth_panel = 180

# Definition of Location object. Using the latitude and altitude entered by the user
site = Location(
    latitude, 0.0, altitude=altitude
)  # latitude, longitude, altitude

# We now compute the average yearly energy production for each panel angle between 0 and 90.
# We can then get the angle that procuces the most energy.

angle = []
energy = []
progress = 0

# We are first computing the energy production of a non bissextile year:

# Definition of the time range of simulation for 365 days
times = pd.date_range(
    start_date + " 00:00:00", end_date + " 23:59:00", freq=delta_time
)
# Retreiving all the sun's position over the time range
sunpos = site.get_solarposition(times)

# Calculation of the 365 days energy production:
for alpha in range(0,90):
    angle.append(alpha)
    energy.append(flux_function(azimuth_panel, alpha, 0.5, 1, 1, sunpos))

    progress += 1.095
    print(f"Computing the optimal angle, progress: {round(progress)}%", end='\r')


# We Then compute the energy production of the 02/29/2024
# And we then add 1/4 of this energy to the total:

# Definition of the time range of simulation for the 02/29/2024:
times = pd.date_range(
    extra_day + " 00:00:00", extra_day + " 23:59:59", freq=delta_time
)
# Retreiving all the sun's position over the time range
sunpos = site.get_solarposition(times)

# Calculation the energy production of the extra day:
for alpha in range(0,90):
    energy[alpha] += 0.25 * flux_function(180, alpha, 0.5, 1, 1, sunpos)
print(f"Computing the optimal angle, progress: 100%\n")

max_pos = np.argmax(energy)
print(f"{BOLD}The optimal angle is {CYAN}{angle[max_pos]}°{END}{BOLD} !!{RESET_BOLD}\n")