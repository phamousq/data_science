import numpy as np
import matplotlib.pyplot as plt
from scipy.special import j1  # Bessel function of the first kind
from scipy.ndimage import convolve
from scipy import signal
from skimage import io  # For reading the image

# Load the neuron image (replace with your image file)
neuron_img = io.imread("hippocampalneuron_gray.png")

# Parameters
wavelength = 0.5  # Wavelength in microns (500 nm)
NA1 = 0.28  # Numerical aperture for first objective
NA2 = 0.95  # Numerical aperture for second objective
k = 2 * np.pi / wavelength  # Wavenumber

# Create 2D grid for PSF calculation
grid_size = 10  # Grid size extends from -5 to 5 microns in both directions
step_size = 0.01  # Step size in microns
x = np.arange(-grid_size, grid_size, step_size)
y = np.arange(-grid_size, grid_size, step_size)
X, Y = np.meshgrid(x, y)
r = np.sqrt(X**2 + Y**2)  # Radial distance from the center

# Airy Disk PSF formula: PSF(r) = (2 * J1(k * r * NA) / (k * r * NA))^2
# PSF for Objective 1 (NA = 1.4)
PSF1 = (2 * j1(k * r * NA1) / (k * r * NA1)) ** 2
PSF1[r == 0] = 1  # Handle singularity at r = 0

# PSF for Objective 2 (NA = 0.85)
PSF2 = (2 * j1(k * r * NA2) / (k * r * NA2)) ** 2
PSF2[r == 0] = 1  # Handle singularity at r = 0

# Normalize the PSFs to ensure they sum to 1
PSF1 = PSF1 / PSF1.sum()
PSF2 = PSF2 / PSF2.sum()

# Perform convolution to simulate image formation for Objective 1
neuron_img_obj1 = signal.convolve(neuron_img.astype(float), PSF1, mode="same")

# Perform convolution to simulate image formation for Objective 2
neuron_img_obj2 = signal.convolve(neuron_img.astype(float), PSF2, mode="same")

# Display the original and convolved images
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.imshow(neuron_img, cmap="gray")
plt.title("Original Neuron Image")
plt.axis("off")

plt.subplot(1, 3, 2)
plt.imshow(neuron_img_obj1, cmap="gray")
plt.title("Neuron Image with Objective 1 (NA 1.4)")
plt.axis("off")

plt.subplot(1, 3, 3)
plt.imshow(neuron_img_obj2, cmap="gray")
plt.title("Neuron Image with Objective 2 (NA 0.85)")
plt.axis("off")

plt.tight_layout()
plt.show()
