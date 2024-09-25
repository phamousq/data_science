import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Read the CSV file
data = pd.read_csv("test.csv")

# Calculate absorbance from transmission
data["Absorbance"] = -np.log10(data["Transmission"])

# Calculate concentration using Beer-Lambert law
# Assuming path length b = 1 cm
data["Concentration"] = data["Absorbance"] / (data["Molar Extinction (cm-1/M)"] * 1)

# Plot concentration vs wavelength
plt.figure(figsize=(10, 6))
plt.plot(data["Wavelength (nm)"], data["Concentration"])
plt.xlabel("Wavelength (nm)")
plt.ylabel("Concentration (M)")
plt.title("Concentration vs Wavelength for Acridine Orange")
plt.grid(True)
plt.show()

# Calculate average concentration
avg_concentration = data["Concentration"].mean()
print(f"Average concentration: {avg_concentration:.6f} M")


# PART B
# Calculate extinction coefficient using average concentration
data["Calculated Extinction"] = data["Absorbance"] / (avg_concentration * 1)

# Plot calculated extinction coefficient
plt.figure(figsize=(10, 6))
plt.plot(data["Wavelength (nm)"], data["Calculated Extinction"], label="Calculated")
plt.plot(data["Wavelength (nm)"], data["Molar Extinction (cm-1/M)"], label="Reference")
plt.xlabel("Wavelength (nm)")
plt.ylabel("Extinction Coefficient (cm-1/M)")
plt.title("Calculated vs Reference Extinction Coefficient")
plt.legend()
plt.grid(True)
plt.show()

data["Difference between Calculated and Reference"] = (
    data["Calculated Extinction"] - data["Molar Extinction (cm-1/M)"]
)

# Plot difference between calculated and reference extinction coefficient
plt.figure(figsize=(10, 6))
plt.plot(
    data["Wavelength (nm)"],
    data["Calculated Extinction"] - data["Molar Extinction (cm-1/M)"],
)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Difference in Extinction Coefficient (cm-1/M)")
plt.title("Difference between Calculated and Reference Extinction Coefficient")
plt.grid(True)
plt.show()
