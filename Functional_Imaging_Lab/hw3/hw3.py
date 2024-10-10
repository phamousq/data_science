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


test_img = cv2.imread("hippocampalneuron_gray.png", cv2.IMREAD_GRAYSCALE)
plt_img = plt.imread("hippocampalneuron_gray.png")
plt.imshow(test_img, cmap="gray")


class Image:
    def __init__(self, png: str):
        self.img = cv2.imread(png)
        self.img_gray = cv2.imread(png, cv2.IMREAD_GRAYSCALE)

    def show_image(self):
        plt.imshow(self.img)
        # cv2.imshow("PRESS ANY KEY TO EXIT", self.img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.waitKey(1)

    def plot_intensity(self, line: Line):
        x_vals = []
        intensities = []
        for i in np.linspace(line.x1, line.x2, line.x2 - line.x1 - 1):
            x_vals.append(int(i))
            intensities.append(int(self.img_gray[line.y1, int(i)]))
        plt.figure()
        plt.plot(x_vals, intensities, linewidth=2, label="Intensity")
        plt.xlabel("X-Coordinate")
        plt.ylabel("Intensity")
        plt.title("Intensity at Given X Coordinates")
        # plt.legend()
        plt.grid(True)
        plt.show()

    def overlay_lines(self, list_lines: list[Line]):
        overlays = []
        for i in range(len(list_lines)):
            overlays.append(
                cv2.line(
                    self.img,
                    list_lines[i].first_as_tuple,
                    list_lines[i].last_as_tuple,
                    (0, 255, 0),
                    2,
                )
            )


line1 = Line(420, 100, 570, 100)
line2 = Line(700, 300, 800, 300)
line3 = Line(320, 800, 420, 800)
neuron = Image("hippocampalneuron_gray.png")

# Show image with 3 lines of interest
neuron.overlay_lines([line1, line2, line3])
neuron.show_image()

# 2b. Plot the intensity profile through 3 lines of interest in the image. Also indicate where the lines are located on the image. You can select the locations of the lines, but I suggest looking at some profiles across axons. The length of the lines should be at least 100 pixels.
neuron.plot_intensity(line1)
neuron.plot_intensity(line2)
neuron.plot_intensity(line3)

# 2c. Estimate the resolution of the image by analyzing some intensity profiles? How does it compare to that of a diffraction limited image (assuming a given objective and wavelength)? This question requires you to make some assumptions and doesn't have one correct answer - just state the assumptions that you make. Also remember that the pixel size of an image is not the same as the resolution of an image and your estimates on resolution should be in microns, not pixels.

x_vals = []
intensities = []
for i in np.linspace(line2.x1, line2.x2, line2.x2 - line2.x1 - 1):
    x_vals.append(int(i))
    intensities.append(int(neuron.img_gray[line2.y1, int(i)]))

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
pixel_length = 50  # nannometer
resolution_observed = (
    swap_res[inten_obs_res] - swap_res[max_intensity]
) * 50  # nanometers


print(
    f"We can see a local max of {max_intensity} at x value of {swap_res[max_intensity]}, half of this is about {max_intensity/2}, the next x value that measures less than half of the maximum intensity occurs at x val {swap_res[inten_obs_res]} with intensity of {inten_obs_res}. this means the resolution is {resolution_observed} nanometers."
)

# Known pixel density
print(f"observed resolution of {resolution_observed} nanometers")


# solve for Rayleigh criterion which determines the diffraction limited resolution
# Assumes objective has oil immersion to maximize NA at 1.4 and microscope wavelength of 0.50micrometers
objective_NA = 1.4
microscope_wavelength = 0.50  # micrometers

rayleigh = 0.61 * microscope_wavelength / objective_NA
print(
    f"smallest detail that can be resolved by the system is {rayleigh} micrometers and this is the diffraction limit of resolution"
)

print(
    f"observed resolution of {resolution_observed * 1E-3} micrometers is higher resolution than diffraction limit {rayleigh} micrometers which is not expected. We expect diffraction limit to be the best resolution that we would be able to achieve with aberrations, pixelation, and user error increase the overall margin of error for the observed resolution."
)


# 3a. Generate and display the 2D PSF of each of the objectives at a wavelength of 500 nm. To do this you will need to create a 2D grid of values with spacings appropriate for the objective. The PSF can be displayed as an intensity map or a surface map and should have axes labeled in microns. The lecture notes have examples of 2D displays of PSF's.
# Constants
wavelength_nm = 500
NA1 = 0.28  # Numerical aperture for Mitutoyo M Plan Apo 10x
NA2 = 0.95  # Numerical aperture for Zeiss Plan Neofluar 63x/0.95 Corr M27
grid_size = 5  # Size of the grid in microns
pixel_size_microns = 0.001  # Pixel size in microns

# Convert wavelength to microns
wavelength_microns = wavelength_nm / 1e3

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

# Load the original image and ensure it's grayscale
image = neuron.img
center_index = psf1.shape[0] // 2  # Find the center index
img_index = image.shape[0] // 2

# Extract the central row to create a 1D profile
psf1_1d = psf1[center_index, :]
img_1d = image[center_index, :]

# Convolve the image with each PSF
simulated_image1 = signal.convolve(image, psf1, mode="same")
simulated_image2 = signal.convolve(image, psf2, mode="same")

# Plotting the simulated images
fig, ax = plt.subplots(1, 2, figsize=(12, 6))
ax[0].imshow(simulated_image1, cmap="gray")
ax[0].set_title(f"Simulated Image with Objective 1 (NA={NA1})")
ax[0].axis("off")

ax[1].imshow(simulated_image2, cmap="gray")
ax[1].set_title(f"Simulated Image with Objective 2 (NA={NA2})")
ax[1].axis("off")

plt.tight_layout()
plt.show()

# 4b. Intensity profiles through a few regions in the original and calculated images. How do these intensity profiles compare to your results from problem 2? What is the cause of any differences?
# Select a line of interest for profile comparison
y_pos = 100  # Example y-coordinate

# Extract intensity profiles
original_profile = image[y_pos, :]
simulated_profile1 = simulated_image1[y_pos, :]
simulated_profile2 = simulated_image2[y_pos, :]

# Plotting the profiles
plt.figure(figsize=(10, 5))
plt.plot(original_profile, label="Original Image", linestyle="--")
plt.plot(simulated_profile1, label="Simulated Image 1 (NA=1.4)")
plt.plot(simulated_profile2, label="Simulated Image 2 (NA=1.0)")
plt.title("Intensity Profiles Comparison")
plt.xlabel("X Pixel Position")
plt.ylabel("Intensity")
plt.legend()
plt.grid(True)
plt.show()


plt.imshow(simulated_image1, cmap="gray")
plt.imshow(simulated_image2, cmap="gray")
