## Hw 5
# %% Import
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter
from scipy.io import loadmat
from scipy.interpolate import interp1d

# %% Question 1 and 2
def read_mat_file(fname):
    """
    Read MATLAB .mat file containing image stack and return in [stack, width, height] format.
    
    Parameters:
        fname (str): Path to the .mat file
        
    Returns:
        numpy.ndarray: Image stack in shape [stack, width, height]
    """
    # Load the .mat file
    data = loadmat(fname)
    
    # Extract and transpose the array to get [stack, width, height]
    # Original shape is [height, width, stack]
    images = data['I'].transpose(2, 0, 1)
    
    print(f"Loaded image stack {fname[6:][:3]} of shape {images.shape}")
    return images
    
# Read raw images (without normalization)
images = read_mat_file('media/001.mat')

# Create a figure with two subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot the raw image
ax1.imshow(images[0], cmap='gray')
ax1.set_title('Raw Speckle Image raw.001 first image')

# Plot histogram of pixel values
ax2.hist(images[0].ravel(), bins=256, range=(0, 255), density=True)
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
speckle_contrast = compute_speckle_contrast(images[0, :, :], window_size)

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
single_contrast = compute_speckle_contrast(images[0, :, :], window_size)

# 2. Average of multiple speckle contrast images
contrast_images = []
for i in range(images.shape[0]):
    contrast = compute_speckle_contrast(images[i, :, :], window_size)
    contrast_images.append(contrast)
avg_contrast_images = np.mean(contrast_images, axis=0)

# 3. Speckle contrast of averaged raw images
avg_raw = np.mean(images, axis=0)
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

# %% Question 5: ROI Analysis
def process_mat_file(filename, window_size, rois):
    """
    Process a single .mat file and return mean speckle contrast for each ROI
    
    Parameters:
        filename (str): Path to the .mat file
        window_size (int): Window size for speckle contrast calculation
        rois (list): List of ROI tuples (y_slice, x_slice)
        
    Returns:
        list: Mean speckle contrast values for each ROI
    """
    # Read images
    images = read_mat_file(filename)
    
    # Compute and average speckle contrast images
    contrast_images = []
    for i in range(images.shape[0]):
        contrast = compute_speckle_contrast(images[i], window_size)
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
rois = [
    (slice(150, 200), slice(200, 250)),     # ROI 1
    (slice(400, 450), slice(50, 100)),      # ROI 2
    (slice(800, 850), slice(760, 810)),     # ROI 3
]

# Process parameters
window_size = 7
roi_names = [f'ROI {i+1}' for i in range(len(rois))]
time_points = np.arange(101) * 24  # 101 time points, 24 seconds apart

# Initialize array to store results
roi_timecourse = np.zeros((len(rois), 101))

# Process each file
for i in range(1, 102):  # Files numbered from 1 to 101
    filename = f'media/{i:03d}.mat'  # Format filename with leading zeros
    roi_means = process_mat_file(filename, window_size, rois)
    roi_timecourse[:, i-1] = roi_means

# Create visualization of ROIs on first image
first_image = read_mat_file('media/001.mat')[0]
speckle_contrast = compute_speckle_contrast(first_image, window_size)

plt.figure(figsize=(10, 8))
plt.imshow(speckle_contrast, cmap='jet')
plt.colorbar(label='Speckle Contrast')

# Highlight ROIs
colors = ['r', 'g', 'b']
for (roi, color, name) in zip(rois, colors, roi_names):
    y_slice, x_slice = roi
    rect = plt.Rectangle((x_slice.start, y_slice.start), 
                        x_slice.stop - x_slice.start, 
                        y_slice.stop - y_slice.start,
                        fill=False, color=color, linewidth=2)
    plt.gca().add_patch(rect)
    # Add text label near the ROI
    plt.text(x_slice.start, y_slice.start-5, name, color=color, 
             fontsize=10, fontweight='bold')

plt.title('Speckle Contrast Image with ROIs')
plt.axis('image')
plt.show()

# Plot time course
plt.figure(figsize=(12, 6))
for i, (values, name, color) in enumerate(zip(roi_timecourse, roi_names, colors)):
    plt.plot(time_points, values, label=name, color=color, 
             marker='o', markersize=3, linestyle='-', linewidth=1)

plt.xlabel('Time (seconds)')
plt.ylabel('Mean Speckle Contrast')
plt.title('Speckle Contrast Time Course for Different ROIs')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Print statistics
print("\nROI Statistics:")
for i, name in enumerate(roi_names):
    mean_val = np.mean(roi_timecourse[i])
    std_val = np.std(roi_timecourse[i])
    print(f"{name} - Mean: {mean_val:.4f}, Std: {std_val:.4f}")

# %% Question 6: Convert Speckle Contrast to Correlation Times
def speckle_contrast_equation(x, T):
    """
    Calculate speckle contrast from correlation time using Eq 2.
    K^2 = (tau/2T) * (1 - exp(-2T/tau))
    
    Parameters:
        x (float or array): Correlation time tau (ms)
        T (float): Exposure time (ms)
    
    Returns:
        float or array: Speckle contrast squared (K^2)
    """
    return (x/(2*T)) * (1 - np.exp(-2*T/x))

def create_speckle_interpolator(T, num_points=1000):
    """
    Create an interpolation function to convert K^2 to correlation time.
    
    Parameters:
        T (float): Exposure time (ms)
        num_points (int): Number of points for interpolation
        
    Returns:
        function: Interpolation function that converts K^2 to correlation time
    """
    # Create range of correlation times (log space)
    tau_range = np.logspace(-2, 2, num_points)
    
    # Calculate corresponding K^2 values
    K2_values = speckle_contrast_equation(tau_range, T)
    
    # Create interpolation function (K^2 -> tau)
    return interp1d(K2_values, tau_range, bounds_error=False, fill_value=(tau_range[0], tau_range[-1]))

# Camera exposure time (ms)
T = 5.0

# Create interpolation function
get_correlation_time = create_speckle_interpolator(T)

# Convert speckle contrast values to correlation times
correlation_times = np.zeros_like(roi_timecourse)
for i in range(len(rois)):
    # Square the contrast values to get K^2
    K2_values = roi_timecourse[i] ** 2
    
    # Convert to correlation times
    correlation_times[i] = get_correlation_time(K2_values)

# Plot 1/Tc vs time
plt.figure(figsize=(12, 6))
for i, (values, name, color) in enumerate(zip(correlation_times, roi_names, colors)):
    # Calculate 1/Tc (1/ms)
    inverse_tc = 1000 / values  # Convert to 1/s
    
    plt.plot(time_points, inverse_tc, label=name, color=color,
             marker='o', markersize=3, linestyle='-', linewidth=1)

plt.xlabel('Time (seconds)')
plt.ylabel('1/Tc (1/s)')
plt.title('Inverse Correlation Time vs Time')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Print statistics for correlation times
print("\nCorrelation Time Statistics:")
for i, name in enumerate(roi_names):
    tc_mean = np.mean(correlation_times[i])
    tc_std = np.std(correlation_times[i])
    print(f"{name} - Mean Tc: {tc_mean:.2f} ms, Std: {tc_std:.2f} ms")
    
    inv_tc_mean = np.mean(1000 / correlation_times[i])
    inv_tc_std = np.std(1000 / correlation_times[i])
    print(f"{name} - Mean 1/Tc: {inv_tc_mean:.2f} 1/s, Std: {inv_tc_std:.2f} 1/s")

# %%
