import polars as pl
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Question 3a
## Importing Data and cleaning
headers = []
data = []

with open("transmission_ao.txt", "r") as file:
    for line in file:
        if "%" in line:
            headers = line[3:].strip().split(", ")
        else:
            data.append(line[2:].strip().split("    "))

for x in range(len(data)):
    for y in range(len(data[x])):
        data[x][y] = float(data[x][y])

df = pl.DataFrame(
    data,
    schema={"Wavelength (nm)": pl.Float64, "Transmission": pl.Float64},
)

data = []
headers = []

## Calculate absorbance from transmission
### Inport data from reference Acradine data
with open("AcradineOrangeExt.txt", "r") as file:
    for line in file:
        if re.search(r"^[\d]", line):
            data.append(line.strip().split("\t"))

for x in range(len(data)):
    for y in range(len(data[x])):
        data[x][y] = float(data[x][y])

df_acradine = pl.DataFrame(
    data,
    schema={"Wavelength (nm)": pl.Float64, "Molar Extinction (cm-1/M)": pl.Float64},
)

# Add extinction coefficient to original dataframe
df = df.join(df_acradine, on="Wavelength (nm)", how="left")

# Calculate absorbance from transmission
df = df.with_columns((-np.log10(pl.col("Transmission"))).alias("Absorbance"))

# Calculate concentration given molar extinction c = A/(ε * b)
df = df.with_columns(
    (pl.col("Absorbance") / pl.col("Molar Extinction (cm-1/M)")).alias("Concentration")
)


# Plot concentration vs wavelength
plt.figure(figsize=(10, 6))
plt.plot(df.select(pl.col("Wavelength (nm)")), df.select(pl.col("Concentration")))
plt.xlabel("Wavelength (nm)")
plt.ylabel("Concentration (M)")
plt.title("Concentration vs Wavelength for Acridine Orange")
plt.grid(True)
plt.show()

# Question 3b
conc_mean = df.select(pl.mean("Concentration")).item()
print("Average Concentration", conc_mean, "M")
# Use the Beer-Lambert law: A = εbc, Rearranging to solve for ε: ε = A / (bc)
# A (absorbance) = -log(T), where T is the measured transmission
# b is the path length (1 cm)
# c is the assumed concentration

# Calculate my own extinction coefficients
df = df.with_columns(
    (pl.col("Absorbance") / conc_mean).alias("My Extinction Coefficient")
)

# Calculate difference between my ext coeff and reference ext coeff
df = df.with_columns(
    (pl.col("My Extinction Coefficient") - pl.col("Molar Extinction (cm-1/M)")).alias(
        "diff in ext coeff"
    )
)


# Plot calculated extinction coefficient
plt.figure(figsize=(10, 6))
plt.plot(
    df.select(pl.col("Wavelength (nm)")), df.select(pl.col("My Extinction Coefficient"))
)
plt.plot(
    df.select(pl.col("Wavelength (nm)")),
    df.select(pl.col("Molar Extinction (cm-1/M)")),
    label="Reference",
)
plt.xlabel("Wavelength (nm)")
plt.ylabel("Extinction Coefficient (cm-1/M)")
plt.title("Calculated vs Reference Extinction Coefficient")
plt.legend()
plt.grid(True)
plt.show()


# overlying the two plots
sns.lineplot(
    data=df,
    x="Wavelength (nm)",
    y="diff in ext coeff",
    label="Diff in extinction coefficients",
)
ax2 = plt.twinx()
sns.lineplot(
    data=df,
    x="Wavelength (nm)",
    ax=ax2,
    y="Concentration",
    color="red",
    label="Concentration",
)
