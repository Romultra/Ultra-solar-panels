import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pvlib.location import Location
from sympy.abc import x,y,z,u,v,w,t
from dtumathtools import *

def panel_normal_np(azimuth,alpha):
    azimuth = np.deg2rad(azimuth)
    alpha = np.deg2rad(alpha)
    vector = np.array([np.cos(azimuth), np.sin(azimuth), np.tan(alpha)])
    return(vector / np.linalg.norm(vector))


def flux_function(azimuth_panel, alpha_panel, A0, L, B, sunpos):
    energy = 0
    
    # Creates the normal vector of the panel with the provided angles

    panel = panel_normal_np(azimuth_panel, alpha_panel)

    sunpos = sunpos[sunpos['apparent_elevation'] > 0]

    alpha = np.deg2rad(sunpos.apparent_elevation)
    azimuth = np.deg2rad(sunpos.azimuth)

    cos_azimuth = np.cos(azimuth)
    sin_azitmuth = np.sin(azimuth)
    tan_alpha = np.tan(alpha)

    solar_flux_array = np.array([cos_azimuth, sin_azitmuth, tan_alpha])
    
    for i in range(len(alpha)):
        solar_flux = solar_flux_array[:, i]*1100 / np.linalg.norm(solar_flux_array[:, i])
        energy += max(0, np.dot(panel, solar_flux))*A0*L*B/1000
            
    return energy


def flux_function_daily_prod(azimuth_panel, alpha_panel, A0, L, B, sunpos):
    energy = 0
    daily_energy = 0
    hours_counter = 0
    daily_energy_prod = []

    # Creates the normal vector of the panel with the provided angles
    panel = panel_normal_np(azimuth_panel, alpha_panel)

    # sunpos = sunpos[sunpos['apparent_elevation'] > 0]

    alpha = np.deg2rad(sunpos.apparent_elevation)
    azimuth = np.deg2rad(sunpos.azimuth)

    cos_azimuth = np.cos(azimuth)
    sin_azitmuth = np.sin(azimuth)
    tan_alpha = np.tan(alpha)

    solar_flux_array = np.array([cos_azimuth, sin_azitmuth, tan_alpha])

    for i in range(len(alpha)):
        if hours_counter == 24:
            hours_counter = 0
            daily_energy_prod.append(daily_energy)
            energy += daily_energy
            daily_energy = 0

        if alpha.iloc[i] > 0:
            solar_flux = solar_flux_array[:, i]*1100 / np.linalg.norm(solar_flux_array[:, i])
            daily_energy += max(0, np.dot(panel, solar_flux))*A0*L*B/1000
        
        hours_counter += 1
        
    daily_energy_prod.append(daily_energy)
    energy += daily_energy
            
    return energy, daily_energy_prod


def flux_function_curved(A0, r, h, sunpos):
    energy = 0
    
    sunpos = sunpos[sunpos['apparent_elevation'] > 0]

    azimuth = np.deg2rad(sunpos.azimuth)

    cos_azimuth = np.cos(azimuth)
    sin_azitmuth = np.sin(azimuth)

    energy_array = (-cos_azimuth*np.sin(np.pi/2) + sin_azitmuth*np.cos(np.pi/2) - (-cos_azimuth*np.sin(-np.pi/2) + sin_azitmuth*np.cos(-np.pi/2))) * A0 *r *h *1100
    energy = np.sum(energy_array)/1000

    return energy


def prod_dtu_1year(alpha_panel=45):
    timezone = "Europe/Copenhagen"
    start_date = "2024-01-01"
    end_date = "2024-12-31"
    delta_time = "H"  # "Min", "H",

    # Definition of Location object. Coordinates and elevation of Amager, Copenhagen (Denmark)
    site = Location(
        55.785469, 12.519103, timezone, 21, "DTU (DK)"
    )  # latitude, longitude, time_zone, altitude, name

    # Definition of a time range of simulation
    times = pd.date_range(
        start_date + " 00:00:00", end_date + " 23:59:00", freq=delta_time, tz=timezone
    )

    sunpos = site.get_solarposition(times)
    return flux_function(180, alpha_panel, 0.5, 1, 1, sunpos)