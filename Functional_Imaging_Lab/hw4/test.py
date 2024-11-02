import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from skimage import filters
from tifffile import imread

# Read the TIFF stack
image_stack = imread("210827.tif")

# Get the dimensions of the stack
z, y, x = image_stack.shape
print(f"Image stack dimensions: {z} x {y} x {x}")


# Convert depth in micrometers to slice indices
def depth_to_slice(depth):
    return int(depth / 3)


# Create maximum intensity projections
mip_100_200 = np.max(image_stack[depth_to_slice(100) : depth_to_slice(200)], axis=0)
mip_400_500 = np.max(image_stack[depth_to_slice(400) : depth_to_slice(500)], axis=0)

# Get the range of pixel values
print(f"Range of pixel values in 100-200 µm: {mip_100_200.min()} - {mip_100_200.max()}")
print(f"Range of pixel values in 400-500 µm: {mip_400_500.min()} - {mip_400_500.max()}")


def plot_image_and_histogram(image, title):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Display image
    im = ax1.imshow(image, cmap="gray")
    ax1.set_title(f"{title} - Image")
    plt.colorbar(im, ax=ax1)

    # Create histogram
    ax2.hist(image.ravel(), bins=256)
    ax2.set_title(f"{title} - Histogram")
    ax2.set_xlabel("Pixel Value")
    ax2.set_ylabel("Frequency")

    plt.tight_layout()
    plt.show()


plot_image_and_histogram(mip_100_200, "Depth 100-200 µm")
plot_image_and_histogram(mip_400_500, "Depth 400-500 µm")


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
original_slice = image_stack[slice_index]
filtered_slice = filters.median(original_slice)

compare_contrast(original_slice, filtered_slice)
