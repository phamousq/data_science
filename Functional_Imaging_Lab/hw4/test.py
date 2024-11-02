import tifffile as tiff
import numpy as np
import matplotlib.pyplot as plt

# Load the image stack
data = tiff.imread("210827.tif")

# Determine pixel value range
pixel_min, pixel_max = data.min(), data.max()
print(f"Pixel value range: {pixel_min} to {pixel_max}")

# Maximum intensity projection for depth 100-200 µm (slices 33 to 66)
mip_100_200 = np.max(data[33:67, :, :], axis=0)

# Maximum intensity projection for depth 400-500 µm (slices 133 to 166)
mip_400_500 = np.max(data[133:167, :, :], axis=0)

# Display MIP images and histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# MIP for 100-200 µm
axes[0, 0].imshow(mip_100_200, cmap="gray", vmin=pixel_min, vmax=pixel_max)
axes[0, 0].set_title("MIP 100-200 µm")
axes[0, 1].hist(mip_100_200.ravel(), bins=256, range=(pixel_min, pixel_max))
axes[0, 1].set_title("Histogram 100-200 µm")

# MIP for 400-500 µm
axes[1, 0].imshow(mip_400_500, cmap="gray", vmin=pixel_min, vmax=pixel_max)
axes[1, 0].set_title("MIP 400-500 µm")
axes[1, 1].hist(mip_400_500.ravel(), bins=256, range=(pixel_min, pixel_max))
axes[1, 1].set_title("Histogram 400-500 µm")

plt.tight_layout()
plt.show()
