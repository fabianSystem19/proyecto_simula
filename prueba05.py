import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# Cargar datos
data = pd.read_csv('planets02.csv')

# Create figura
fig, ax = plt.subplots(figsize=(8,8))

# Plotear el sol
ax.scatter([0], [0], color='orange')

# Relacion de aspecto
ax.set_aspect('equal', adjustable='box')

planets = []

# For each planet
for _, planet_data in data.iterrows():
    # Extraer informacion necesaria
    orbital_period = planet_data['Orbital Period (days)']
    distance_from_sun = planet_data['Distance from Sun (10^6 km)']
    orbital_velocity = planet_data['Orbital Velocity (km/s)']
    orbital_eccentricity = planet_data['Orbital Eccentricity']

    # Limpiar dataset
    if isinstance(orbital_period, str):
        orbital_period = float(orbital_period.replace(',', ''))
    if isinstance(distance_from_sun, str):
        distance_from_sun = float(distance_from_sun.replace(',', '')) * 10**6  # Convert to km
    if isinstance(orbital_velocity, str):
        orbital_velocity = float(orbital_velocity.replace(',', ''))
    if isinstance(orbital_eccentricity, str):
        orbital_eccentricity = float(orbital_eccentricity.replace(',', ''))

    # Simular la orbita
    t = np.linspace(0, 2*np.pi, 1000)  # Generate a fixed number of points
    r = distance_from_sun * (1 - orbital_eccentricity**2) / (1 + orbital_eccentricity * np.cos(t))
    x = r * np.cos(t)
    y = r * np.sin(t)

    # Plotear planetas en
    ax.plot(x, y)

    # Create planet marker
    planet, = ax.plot([], [], 'o')
    planets.append((planet, x, y, orbital_period))  # Store orbital period as a float

# Update function for animation
def update(num):
    for planet, x, y, period in planets:
        idx = int(num * (365.25 / period)) % len(x)  # Adjust index for each planet's orbital period
        planet.set_data(x[idx], y[idx])
    return planets,

# Create animation
ani = FuncAnimation(fig, update, frames=range(1000), interval=50)

plt.show()
