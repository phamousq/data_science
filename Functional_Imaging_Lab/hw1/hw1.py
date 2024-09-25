import numpy as np
import matplotlib.pyplot as plt

n_1 = 1.333  # Refractive index of water per google
n_2 = 1.31  # Refractive index of ice per google
I0 = 5  # Incident intensity in mW/cm^2

# Angle range from 0 to 90 degrees
theta_i_rad = np.linspace(0, np.pi / 2, 1000)

# Preallocate arrays for reflection intensities
R_s = np.zeros_like(theta_i_rad)
R_p = np.zeros_like(theta_i_rad)

for i, theta_i in enumerate(theta_i_rad):
    # Calculate the transmission angle using Snell's law
    sin_theta_t = (n_1 / n_2) * np.sin(theta_i)
    # Total internal reflection scenario (not physically realizable)
    if -1 <= sin_theta_t <= 1:
        theta_t = np.arcsin(sin_theta_t)

        # s-polarized reflection coefficient
        R_s[i] = (n_1 * np.cos(theta_i) - n_2 * np.cos(theta_t)) / (
            n_1 * np.cos(theta_i) + n_2 * np.cos(theta_t)
        )

        # p-polarized reflection coefficient
        R_p[i] = (n_1 * np.cos(theta_t) - n_2 * np.cos(theta_i)) / (
            n_1 * np.cos(theta_t) + n_2 * np.cos(theta_i)
        )
    else:
        R_s[i] = 1
        R_p[i] = 1

# Calculate reflected intensities
I_s = R_s**2 * I0
I_p = R_p**2 * I0

# Plotting
plt.figure()
plt.plot(np.degrees(theta_i_rad), I_s, "r", linewidth=2, label="s-polarized")
plt.plot(np.degrees(theta_i_rad), I_p, "b", linewidth=2, label="p-polarized")
plt.xlabel("Incident Angle (degrees)")
plt.ylabel("Reflected Intensity (mW/cm^2)")
plt.title("Reflected Intensity vs Incident Angle at Water-Ice Interface")
plt.legend()
plt.grid(True)
plt.show()
