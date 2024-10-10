import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.special import j1


# 2.
class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.first_as_tuple = (self.x1, self.y1)
        self.last_as_tuple = (self.x2, self.y2)
        self.xline = [self.x1, self.x2]
        self.yline = [self.y1, self.y2]


def normalize_array(arr):
    norm_arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr))
    return norm_arr


class Image:
    def __init__(self, png: str):
        self.img = plt.imread(png)
        self.img_gray = cv2.imread(png, cv2.IMREAD_GRAYSCALE)

    def show_image(self):
        plt.imshow(self.img, cmap="gray")


def plot_intensity(x: Image, line: Line):
    x_vals = []
    intensities = []

    for i in np.linspace(line.x1, line.x2, line.x2 - line.x1 - 1):
        x_vals.append(int(i))
        intensities.append(int(x[line.y1, int(i)]))
    plt.figure()
    plt.plot(x_vals, normalize_array(intensities), linewidth=2, label="Intensity")
    plt.xlabel("X-Coordinate")
    plt.ylabel("Intensity")
    plt.title("Intensity at Given X Coordinates")
    # plt.legend()
    plt.grid(True)
    plt.show()


def plot_lines(lines: list[Line]):
    for line in lines:
        plt.plot(
            line.xline,
            line.yline,
            color="green",
            linewidth=2,
        )


lines = []
lines.append(Line(420, 100, 570, 100))
lines.append(Line(700, 300, 800, 300))
lines.append(Line(320, 800, 420, 800))

neuron = Image("hippocampalneuron_gray.png")
# neuron.overlay_lines(lines)
plot_lines(lines)
neuron.show_image()

# 2b. Plot the intensity profile through 3 lines of interest in the image. Also indicate where the lines are located on the image. You can select the locations of the lines, but I suggest looking at some profiles across axons. The length of the lines should be at least 100 pixels.
for line in lines:
    plot_intensity(neuron.img_gray, line)

# 2c. Estimate the resolution of the image by analyzing some intensity profiles? How does it compare to that of a diffraction limited image (assuming a given objective and wavelength)? This question requires you to make some assumptions and doesn't have one correct answer - just state the assumptions that you make. Also remember that the pixel size of an image is not the same as the resolution of an image and your estimates on resolution should be in microns, not pixels.

x_vals = []
intensities = []
for i in np.linspace(lines[1].x1, lines[1].x2, lines[1].x2 - lines[1].x1 - 1):
    x_vals.append(int(i))
    intensities.append(int(neuron.img_gray[lines[1].y1, int(i)]))

# dict of pixel: intensity
# Calculate observed resolution using full width maximum height method
res = dict(zip(x_vals, intensities))
swap_res = {v: k for k, v in res.items()}
pixel_max_intensity = max(res, key=res.get)
max_intensity = res[pixel_max_intensity]
print(dict((k, v) for k, v in res.items() if v >= max_intensity))
# shows 2nd local max at 773

print(
    f"max intensities: {max_intensity}, half of max intensities for determining resolution in pixels: {max_intensity/2}"
)

inten_obs_res = next(
    iter(
        dict(
            (k, v)
            for k, v in res.items()
            if v <= max_intensity / 2 and k >= pixel_max_intensity
        ).values()
    )
)
pixel_length = 50e-3  # nm to microns
resolution_observed = (swap_res[inten_obs_res] - swap_res[max_intensity]) * pixel_length

print(
    f"We can see a local max of {max_intensity} at x value of {swap_res[max_intensity]}, half of this is about {max_intensity/2}, the next x value that measures less than half of the maximum intensity occurs at x val {swap_res[inten_obs_res]} with intensity of {inten_obs_res}. this means the resolution is {resolution_observed} microns."
)

# solve for Rayleigh criterion which determines the diffraction limited resolution
# Assumes objective has oil immersion to maximize NA at 1.4 and microscope wavelength of 0.50micrometers
objective_NA = 1.4
microscope_wavelength = 0.50  # micrometers

rayleigh = 0.61 * microscope_wavelength / objective_NA
print(
    f"smallest detail that can be resolved by the system is {rayleigh} micrometers and this is the diffraction limit of resolution"
)

print(
    f"observed resolution of {resolution_observed} micrometers is slightly better than {rayleigh} micrometers, the theoretical diffraction limit which is unexpected. aberrations, pixelation, and user error increase the overall margin of error contribute to errors in observed resolution. Given that pixel length was given, this could be a source of error."
)


# 3a. Generate and display the 2D PSF of each of the objectives at a wavelength of 500 nm. To do this you will need to create a 2D grid of values with spacings appropriate for the objective. The PSF can be displayed as an intensity map or a surface map and should have axes labeled in microns. The lecture notes have examples of 2D displays of PSF's.
# Constants
wavelength_nm = 500
NA1 = 0.28  # Numerical aperture for objective 1
NA2 = 0.95  # Numerical aperture for objective 2
grid_size = 10  # Size of the grid in microns
pixel_size_microns = 0.01  # Pixel size in microns

# Convert wavelength to microns
wavelength_microns = wavelength_nm / 1000

# Create a grid of spatial coordinates
x = np.linspace(-grid_size / 2, grid_size / 2, int(grid_size / pixel_size_microns))
y = np.linspace(-grid_size / 2, grid_size / 2, int(grid_size / pixel_size_microns))
X, Y = np.meshgrid(x, y)
R = np.sqrt(X**2 + Y**2)


# Function to calculate Airy disk PSF
def airy_psf(R, wavelength, NA):
    k = (2 * np.pi * NA) / wavelength
    return (2 * j1(k * R) / (k * R)) ** 2


# Calculate PSFs for both objectives
psf1 = airy_psf(R, wavelength_microns, NA1)
psf2 = airy_psf(R, wavelength_microns, NA2)

# Plotting the PSFs
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(
    psf1,
    extent=(-grid_size / 2, grid_size / 2, -grid_size / 2, grid_size / 2),
    cmap="hot",
)
ax[0].set_title(f"PSF for Objective 1 (NA={NA1})")
ax[0].set_xlabel("Microns")
ax[0].set_ylabel("Microns")

ax[1].imshow(
    psf2,
    extent=(-grid_size / 2, grid_size / 2, -grid_size / 2, grid_size / 2),
    cmap="hot",
)
ax[1].set_title(f"PSF for Objective 2 (NA={NA2})")
ax[1].set_xlabel("Microns")
ax[1].set_ylabel("Microns")

plt.tight_layout()
plt.show()


# 3b. Plot the profile through the center of the PSF for both objectives. The x axis should be in microns.
# Plotting the profiles through the center
center_index = len(x) // 2

plt.figure(figsize=(15, 5))
plt.plot(x, psf1[center_index, :], label=f"Objective 1 (NA={NA1})")
plt.plot(x, psf2[center_index, :], label=f"Objective 2 (NA={NA2})")
plt.title("PSF Profiles through Center")
plt.xlabel("Microns")
plt.ylabel("Intensity")
plt.legend()
plt.grid(True)
plt.show()

# 4. If the neurons are imaged with the two objectives above, what will the images look like? To answer this question, you should create 2 new images numerically in matlab using the principles of image formation and point spread functions calculated in problem 3. You should include an explanation of your work and matlab code that you write. Your analysis should include at least the following:
# 4a. Calculated images of the neuron for each objective.
# ! for some reason after convolution, having values in 1000s when expecting very small values
# Convolve the image with each PSF
simulated_image1 = signal.convolve(neuron.img, psf1, mode="same")
simulated_image2 = signal.convolve(neuron.img, psf2, mode="same")

# Plotting the simulated images
fig, ax = plt.subplots(1, 3, figsize=(12, 6))
ax[0].imshow(simulated_image1, cmap="gray")
ax[0].set_title(f"Simulated Image with Objective 1 (NA={NA1})")
ax[0].axis("off")

ax[1].imshow(simulated_image2, cmap="gray")
ax[1].set_title(f"Simulated Image with Objective 2 (NA={NA2})")
ax[1].axis("off")

ax[2].imshow(neuron.img, cmap="gray")
ax[2].set_title("reference image")
ax[2].axis("off")

plt.tight_layout()
plt.show()

# 4b. Intensity profiles through a few regions in the original and calculated images. How do these intensity profiles compare to your results from problem 2? What is the cause of any differences?

# Select a line of interest for profile comparison
for line in lines:
    plot_intensity(simulated_image1, line)

print(
    "new calculated intensities are more smooth and do not show peaks where the original peaks were as the image as the convolution process has 'blurred' the image; other points on the image will contribute to the intensity of the other points meaning discrete points which could be seen clearly before can no longer be seen clearly."
)
