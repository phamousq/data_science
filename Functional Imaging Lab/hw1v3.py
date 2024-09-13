import numpy as np
import matplotlib.pyplot as plt

# Refractive indices
n1 = 1.33  # Refractive index of medium 1 (air)
n2 = 1.0  # Refractive index of medium 2 (glass)
I0 = 5e-1  # Incident intensity in mW/cm^2

# Incident angles from 0 to 90 degrees
angles_rads = np.linspace(0, np.pi / 2, 1000)

# Initialize lists for reflection coefficients
r_TE = np.zeros_like(angles_rads)
r_TM = np.zeros_like(angles_rads)

for i, angle in enumerate(angles_rads):
    cos_theta1 = np.cos(angle)
    sin_theta2 = n1 / n2 * np.sin(angle)
    # Handle the case where sin_theta2 is out of the valid range [-1, 1]
    cos_theta2 = np.cos(np.arcsin(sin_theta2)) if -1 <= sin_theta2 <= 1 else 0

    r_TE[i] = (
        (n1 * cos_theta1 - n2 * cos_theta2) / (n1 * cos_theta1 + n2 * cos_theta2)
    ) ** 2 * I0

    r_TM[i] = (
        (n2 * cos_theta1 - n1 * cos_theta2) / (n2 * cos_theta1 + n1 * cos_theta2)
    ) ** 2 * I0

# Plotting
plt.plot(np.degrees(angles_rads), r_TE, label="TE", color="red")
plt.plot(np.degrees(angles_rads), r_TM, label="TM", color="blue")
plt.xlabel("angle")
plt.ylabel("R")
plt.title("TE and TM Reflection Intensity vs Incident Angle")
plt.legend()
plt.grid(True)
plt.show()
