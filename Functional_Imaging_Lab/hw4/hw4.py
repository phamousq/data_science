# hw4
import matplotlib.pyplot as plt
import cv2
import tifffile as tiff
import numpy as np


# ? Question 1
def split_tiff(input_file, output_dir):
    list_tiff = []
    with tiff.TiffFile(input_file) as tif:
        for i, page in enumerate(tif.pages):
            list_tiff.append(page.asarray())
            # output_path = f"{output_dir}/page_{i}.tif"
            # tifffile.imwrite(output_path, page.asarray())
    return list_tiff


# Slieces are 1.34um x 1.34 um. Each slice separated by 3um.
# images are 512x512 pixels
between_slices = 3  # um

# * read data into 3d array of intensity values
list_of_2d_arrays_from_tiff = split_tiff(
    "210827.tif", "/Users/qpair/Documents/data_science/Functional_Imaging_Lab/hw4"
)
len(list_of_2d_arrays_from_tiff) * between_slices  # 234 total slices; 702um imaged.

# * function to get the "maxiumum intensity projections"
# From 100 - 200 um
np.amax(
    list_of_2d_arrays_from_tiff[
        round(100 / between_slices) : round(200 / between_slices)
    ],
    axis=0,
)

np.max(
    list_of_2d_arrays_from_tiff[
        round(400 / between_slices) : round(500 / between_slices)
    ],
    axis=0,
)

# * print out range of pixel values
print(list_of_2d_arrays_from_tiff.min())
print(np.amax(list_of_2d_arrays_from_tiff))


# * render images as grayscale over an appropraite range of intensity values
tiff.imwrite(
    "temp.tif",
    np.max(
        list_of_2d_arrays_from_tiff[33:67],
        axis=0,
    ),
    photometric="minisblack",
)

# * create histograms of intensity values

# * final code should include two images and two histograms

# ? Question 2
"""
Create a fly through of the image stack (axially) by displaying the maximum intensity projection of the images in 30 um thick moving axial sections. What effect does a 2D median filter have on the images? Compare the image contrast with and without a median filter. You should turn in videos of the fly through with and without the median filter, a short description of the effect of the median filter, and all matlab code.
"""
