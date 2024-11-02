# hw4
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import tifffile as tiff
from scipy.ndimage import median_filter
from skimage import filters

# import cv2


# HW4 Canvas: https://utexas.instructure.com/courses/1398652/assignments/6856706
# ? Question 1
def split_tiff(input_file, output_dir):
    list_tiff = []
    with tiff.TiffFile(input_file) as tif:
        for i, page in enumerate(tif.pages):
            list_tiff.append(page.asarray())
            # output_path = f"{output_dir}/page_{i}.tif"
            # tifffile.imwrite(output_path, page.asarray())
    return np.array(list_tiff)


# Slieces are 1.34um x 1.34 um. Each slice separated by 3um.
# images are 512x512 pixels
between_slices = 3  # um


def depth_to_slice(depth):
    return int(depth / 3)


# * read data into 3d array of intensity values
list_of_2d_arrays_from_tiff = split_tiff(
    "210827.tif", "/Users/qpair/Documents/data_science/Functional_Imaging_Lab/hw4"
)
len(list_of_2d_arrays_from_tiff) * between_slices  # 234 total slices; 702um imaged.
image_stack = tiff.imread("210827.tif")


# * function to get the "maxiumum intensity projections"
# From 100 - 200 um
max_100_200 = np.amax(
    list_of_2d_arrays_from_tiff[depth_to_slice(100) : depth_to_slice(200)],
    axis=0,
)

max_400_500 = np.max(
    list_of_2d_arrays_from_tiff[depth_to_slice(400) : depth_to_slice(500)],
    axis=0,
)

# * print out range of pixel values
# ! these values don't seem typical to me... looks like there are outliers that skew the data heavily.
range_min = np.amin(list_of_2d_arrays_from_tiff)
range_max = np.amax(list_of_2d_arrays_from_tiff)

# * create histograms of intensity values
# Display MIP images and histograms
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# MIP for 100-200 µm
axes[0, 0].imshow(max_100_200, cmap="gray", vmin=range_min, vmax=range_max)

axes[0, 0].set_title("MIP 100-200 µm")
axes[0, 1].hist(max_100_200.ravel(), bins=256, range=(range_min, range_max))
axes[0, 1].set_title("Histogram 100-200 µm")

# MIP for 400-500 µm
axes[1, 0].imshow(max_400_500, cmap="gray", vmin=range_min, vmax=range_max)
axes[1, 0].set_title("MIP 400-500 µm")
axes[1, 1].hist(max_400_500.ravel(), bins=256, range=(range_min, range_max))
axes[1, 1].set_title("Histogram 400-500 µm")

plt.tight_layout()
plt.show()


# ? Question 2
"""
Create a fly through of the image stack (axially) by displaying the maximum intensity projection of the images in 30 um thick moving axial sections. What effect does a 2D median filter have on the images? Compare the image contrast with and without a median filter. You should turn in videos of the fly through with and without the median filter, a short description of the effect of the median filter, and all matlab code.
"""

# camera = Camera(fig)


# Define function to generate fly-through frames
def create_flythrough(data, filter_median=False):
    frames = []
    for start in range(0, data.shape[0] - 10, 1):  # Slide 10-slice window
        mip = np.max(data[start : start + 10, :, :], axis=0)
        if filter_median:
            mip = median_filter(mip, size=(3, 3))
        frames.append(mip)
        # camera.snap()
    return frames


# Generate fly-through frames with and without median filtering
frames_unfiltered = create_flythrough(image_stack, filter_median=False)

frames_filtered = create_flythrough(image_stack, filter_median=True)

# Create animation for unfiltered and filtered fly-throughs


def create_flythrough(image_stack, slice_thickness, with_median_filter=False):
    z, y, x = image_stack.shape

    fig, ax = plt.subplots()

    slices = range(0, z - slice_thickness, 5)  # Step by 5 for smoother animation

    ims = []
    for i in slices:
        mip = np.max(image_stack[i : i + slice_thickness], axis=0)
        if with_median_filter:
            mip = filters.median(mip)
        im = ax.imshow(mip, animated=True, cmap="gray")
        ims.append([im])

    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat_delay=1000)

    plt.close()
    return ani


# Create fly-through without median filter
ani_without_filter = create_flythrough(image_stack, depth_to_slice(30))
ani_without_filter.save("flythrough_without_filter.gif")

# Create fly-through with median filter
ani_with_filter = create_flythrough(
    image_stack, depth_to_slice(30), with_median_filter=True
)
ani_with_filter.save("flythrough_with_filter.gif")


def compare_contrast(image, filtered_image):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.imshow(image, cmap="gray")
    ax1.set_title("Original Image")

    ax2.imshow(filtered_image, cmap="gray")
    ax2.set_title("Median Filtered Image")

    plt.tight_layout()
    plt.show()


# Compare a single slice
slice_index = depth_to_slice(200)
original_slice = list_of_2d_arrays_from_tiff[slice_index]
filtered_slice = filters.median(original_slice)

compare_contrast(original_slice, filtered_slice)
