## Hw 5
import numpy as np
import matplotlib.pyplot as plt

# Please submit the code you wrote for reading in the images and displaying the images, and an image of one raw frame

from laser_speckle_contrast_imaging import read_raw_basler

# Read all images from a file
images = read_raw_basler('media/raw.0001')

# Or read specific number of images
images = read_raw_basler('your_file.raw', n_images=10)

images.shape

# Display the first image
plt.imshow(images[0], cmap='gray')

plt.imshow(images)