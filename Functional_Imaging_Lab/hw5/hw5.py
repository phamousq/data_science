## Hw 5
# %% Import
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter

from laser_speckle_contrast_imaging import read_raw_basler

# %% Question 1 and 2
# Read raw images (without normalization)
images = read_raw_basler('media/raw.0001')

# Create a figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the raw image
ax1.imshow(images[:, :, 0], cmap='gray')
ax1.set_title('Raw Speckle Image raw.0001 first image')

# Plot histogram of pixel values
ax2.hist(images[:, :, 0].ravel(), bins=256, range=(0, 255), density=True)
ax2.set_title('Histogram of Pixel Values')
ax2.set_xlabel('Pixel IntensityValue')
ax2.set_ylabel('Frequency')

plt.tight_layout()
plt.show()
print("the histogram shows pixel intensity value between 0 and 255 given the 8 bit nature of the image, and the y axit shows frequency of a given pixel intensity value. there appears to be a peak around 35.")

# %% Question 3: Compute and display speckle contrast image
def compute_speckle_contrast(image, window_size):
    """
    Compute speckle contrast image using sliding window operations.
    
    Parameters:
    -----------
    image : numpy.ndarray
        Input image (2D array)
    window_size : int
        Size of the sliding window (must be odd)
        
    Returns:
    --------
    numpy.ndarray
        Speckle contrast image
    """
    
    # Ensure window_size is odd
    if window_size % 2 == 0:
        window_size += 1
    
    # Convert to float for calculations
    image = image.astype(float)
    
    # Calculate mean using uniform filter (sliding window mean)
    mean = uniform_filter(image, size=window_size, mode='reflect')
    
    # Calculate variance using uniform filter
    variance = uniform_filter(image**2, size=window_size, mode='reflect') - mean**2
    
    # Calculate standard deviation
    std = np.sqrt(np.maximum(variance, 0))  # Use maximum to avoid negative values due to numerical errors
    
    # Calculate speckle contrast (K = σ/μ)
    # Add small epsilon to avoid division by zero
    epsilon = 1e-10
    speckle_contrast = std / (mean + epsilon)
    
    return speckle_contrast

window_size = 7  # You can adjust this value
speckle_contrast = compute_speckle_contrast(images[:, :, 0], window_size)

# Display speckle contrast image
plt.figure(figsize=(8, 6))
im = plt.imshow(speckle_contrast, cmap='jet')
plt.colorbar(im)
plt.title(f'Speckle Contrast Image (window size = {window_size})')
plt.axis('image')
plt.show()

# Print statistics
print(f"Speckle contrast range: {speckle_contrast.min():.3f} to {speckle_contrast.max():.3f}")
print("we expect the speckle contrast to have a range between 0 and 1, with 0 meaning no speckle contrast and 1 meaning high speckle contrast. We see some speckle values over 1 here due to how we calculate the contrast.")

# %% Question 4: Compare different averaging approaches
window_size = 7

# 1. Single raw image speckle contrast
single_contrast = compute_speckle_contrast(images[:, :, 0], window_size)

# 2. Average of multiple speckle contrast images
contrast_images = []
for i in range(images.shape[2]):
    contrast = compute_speckle_contrast(images[:, :, i], window_size)
    contrast_images.append(contrast)
avg_contrast_images = np.mean(contrast_images, axis=0)

# 3. Speckle contrast of averaged raw images
avg_raw = np.mean(images, axis=2)
contrast_of_avg = compute_speckle_contrast(avg_raw, window_size)

# Display results
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Single contrast image
im1 = axes[0].imshow(single_contrast, cmap='jet')
axes[0].set_title('Single Image\nSpeckle Contrast')
plt.colorbar(im1, ax=axes[0])

# Average of contrast images
im2 = axes[1].imshow(avg_contrast_images, cmap='jet')
axes[1].set_title('Average of\nSpeckle Contrast Images')
plt.colorbar(im2, ax=axes[1])

# Contrast of averaged raw
im3 = axes[2].imshow(contrast_of_avg, cmap='jet')
axes[2].set_title('Speckle Contrast of\nAveraged Raw Images')
plt.colorbar(im3, ax=axes[2])

# Set same scale for all images
vmin = min(single_contrast.min(), avg_contrast_images.min(), contrast_of_avg.min())
vmax = max(single_contrast.max(), avg_contrast_images.max(), contrast_of_avg.max())
for im in [im1, im2, im3]:
    im.set_clim(vmin, vmax)

plt.tight_layout()
plt.show()

# Print statistics for comparison
print("\nSpeckle Contrast Statistics:")
print(f"Single image - Mean: {np.mean(single_contrast):.4f}, Std: {np.std(single_contrast):.4f}")
print(f"Averaged contrasts - Mean: {np.mean(avg_contrast_images):.4f}, Std: {np.std(avg_contrast_images):.4f}")
print(f"Contrast of averaged raw - Mean: {np.mean(contrast_of_avg):.4f}, Std: {np.std(contrast_of_avg):.4f}")

# Explanation of differences
print("\nAnalysis of averaging approaches:")
print("1. Single image shows more noise but preserves temporal information")
print("2. Averaging contrast images reduces noise while maintaining speckle contrast sensitivity")
print("3. Computing contrast of averaged raw images reduces speckle contrast due to temporal averaging")
print("\nThe two averaging approaches are not equivalent because:")
print("- Averaging contrast images preserves the speckle statistics of each frame")
print("- Averaging raw images first reduces speckle pattern variation before contrast calculation. This results in loss of temporal information in the speckle pattern.")


# %% Question 5: 
def process_file(filename, window_size, rois):
    """
    Process a single file and return mean speckle contrast for each ROI
    """
    # Read images
    images = read_raw_basler(filename)
    
    # Compute and average speckle contrast images
    contrast_images = []
    for i in range(images.shape[2]):
        contrast = compute_speckle_contrast(images[:, :, i], window_size)
        contrast_images.append(contrast)
    avg_contrast = np.mean(contrast_images, axis=0)
    
    # Calculate mean for each ROI
    roi_means = []
    for roi in rois:
        y_slice, x_slice = roi
        roi_mean = np.mean(avg_contrast[y_slice, x_slice])
        roi_means.append(roi_mean)
    
    return roi_means

# Define ROIs as slices (y_start:y_end, x_start:x_end)
# You can adjust these coordinates based on your regions of interest
rois = [
    (slice(100, 150), slice(100, 150)),  # ROI 1
    (slice(200, 250), slice(200, 250)),  # ROI 2
    (slice(300, 350), slice(300, 350)),  # ROI 3
]

# Process all files
window_size = 7
roi_names = [f'ROI {i+1}' for i in range(len(rois))]
time_points = np.arange(102) * 24  # 102 time points, 24 seconds apart

# Initialize array to store results
roi_timecourse = np.zeros((len(rois), 102))

# Process each file
for i in range(1, 102):  # Files numbered from 1 to 101
    filename = f'media/raw.{i:04d}'  # Format filename with leading zeros
    roi_means = process_file(filename, window_size, rois)
    roi_timecourse[:, i-1] = roi_means

# Plot results
plt.figure(figsize=(12, 6))
for i in range(len(rois)):
    plt.plot(time_points, roi_timecourse[i], label=roi_names[i], marker='o', markersize=3)

plt.xlabel('Time (miliseconds)')
plt.ylabel('Mean Speckle Contrast')
plt.title('Speckle Contrast Time Course for Different ROIs')
plt.legend()
plt.grid(True)
plt.show()

# Print some statistics
print("\nROI Statistics:")
for i, name in enumerate(roi_names):
    mean_val = np.mean(roi_timecourse[i])
    std_val = np.std(roi_timecourse[i])
    print(f"{name} - Mean: {mean_val:.4f}, Std: {std_val:.4f}")
# %%
