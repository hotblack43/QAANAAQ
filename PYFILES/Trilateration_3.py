import pandas as pd
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Constants
c = 343  # m/s
c /= 1000  # km/s

# Read data
df = pd.read_csv("../DATA/offsets.txt", sep=",")
coords = pd.read_csv("../DATA/coordinates.txt", sep=",")

# Merge data frames
merged_df = pd.merge(df, coords, on="Station", how="outer")
df = merged_df

# Plot coordinates
plt.scatter(coords["Longitude"], coords["Latitude"], marker="o")
for i, txt in enumerate(coords["Station"]):
    plt.annotate(txt, (coords["Longitude"][i], coords["Latitude"][i]))
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()

# Convert coordinates to UTM
from pyproj import Proj, transform

def transform_coordinates(longitude, latitude):
    in_proj = Proj(init="epsg:4326")  # WGS 84
    out_proj = Proj(init="epsg:32619")  # UTM Zone 19N
    easting, northing = transform(in_proj, out_proj, longitude, latitude)
    return easting / 1000, northing / 1000  # Convert to km

df["easting"], df["northing"] = zip(*df.apply(lambda row: transform_coordinates(row["Longitude"], row["Latitude"]), axis=1))

plt.scatter(df["easting"], df["northing"], marker="o")
plt.xlabel("Easting (km)")
plt.ylabel("Northing (km)")
plt.show()

# Calculate source easting and northing
source_easting, source_northing = transform_coordinates(-69.0, 76.9)

# Define prior function
def prior_function(parameters):
    min_easting, max_easting = 0, 1000
    min_northing, max_northing = 7000, 9000
    min_height, max_height = 0, 100
    min_t0, max_t0 = 0, 500
    if not (min_easting <= parameters[0] <= max_easting and
            min_northing <= parameters[1] <= max_northing and
            min_height <= parameters[2] <= max_height and
            min_t0 <= parameters[3] <= max_t0):
        return 1e-17  # Return small number for parameters outside plausible range
    return 0  # Assuming uniform prior, so prior probability is constant

# Define error function
def error_function(parameters, y, X):
    easting, northing, height, t0 = parameters
    predicted_times = calculate_predicted_times(easting, northing, height, t0, y, X)
    errors = y - predicted_times
    sigma = np.array([0.05] * 8)  # Assuming constant variance
    negative_log_likelihood = -0.5 * np.sum((errors / sigma) ** 2 + np.log(2 * np.pi * sigma ** 2))
    return negative_log_likelihood

# Define log merit function
def log_merit_function(parameters, y, X):
    negative_log_likelihood = error_function(parameters, y, X)
    prior = prior_function(parameters)
    log_likelihood = -negative_log_likelihood
    log_posterior = log_likelihood + prior
    return log_posterior

# MCMC
n_iter = 1000000  # Number of iterations
n_burn = 5000  # Number of burn-in iterations
initial_guess = np.array([454., 8685., 80., 334.])  # Initial guess

# Call MCMC sampling function
y = df["t_offset"]
X = df[["easting", "northing"]].assign(intercept=1)
#posterior_samples = MCMCmetrop1R(log_merit_function, y=y, X=X, mcmc=n_iter + n_burn, thin=1, tune=1, theta.init=initial_guess, verbose=1000)
posterior_samples = MCMCmetrop1R(log_merit_function, y, X, n_iter + n_burn, 1, 1, initial_guess, 1000)


# Plot posterior samples
fig, axs = plt.subplots(2, 2)
for i, ax in enumerate(axs.flat):
    ax.plot(posterior_samples[:, i])
    ax.set_title(f"Parameter {i+1}")
plt.tight_layout()
plt.show()

