import numpy as np
import matplotlib.pyplot as plt

# Constants
n1 = 1.332  # Refractive index of water
n2 = 1.309  # Refractive index of ice
I0 = 5  # Incident intensity in mW/cm^2


# Function to calculate reflection coefficients
def reflection_coefficients(theta_i):
    theta_t = np.arcsin(n1 * np.sin(theta_i) / n2)

    # Handle potential invalid values for arcsin
    rs = np.where(
        np.isfinite(theta_t),
        (n1 * np.cos(theta_i) - n2 * np.cos(theta_t))
        / (n1 * np.cos(theta_i) + n2 * np.cos(theta_t)),
        0,
    )
    rp = np.where(
        np.isfinite(theta_t),
        (n2 * np.cos(theta_i) - n1 * np.cos(theta_t))
        / (n2 * np.cos(theta_i) + n1 * np.cos(theta_t)),
        0,
    )

    return rs**2, rp**2


# Generate incident angles
theta_i = np.linspace(0, np.pi / 2, 1000)

# Calculate reflection coefficients
Rs, Rp = reflection_coefficients(theta_i)

# Calculate reflected intensities
Is = I0 * Rs
Ip = I0 * Rp

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(np.degrees(theta_i), Is, label="s-polarization")
plt.plot(np.degrees(theta_i), Ip, label="p-polarization")
plt.xlabel("Incident Angle (degrees)")
plt.ylabel("Reflected Intensity (mW/cm²)")
plt.title("Reflected Intensity vs Incident Angle for Water-Ice Interface")
plt.legend()
plt.grid(True)
plt.show()
