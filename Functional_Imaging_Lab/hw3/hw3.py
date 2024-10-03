import polars as pl
import cv2
import matplotlib.pyplot as plt

# 2.

# 2a. Show image
img = cv2.imread("neuron.png")
cv2.imshow("title", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# 2b. Plot the intensity profile through 3 lines of interest in the image. Also indicate where the lines are located on the image. You can select the locations of the lines, but I suggest looking at some profiles across axons. The length of the lines should be at least 100 pixels.

# 2c. Estimate the resolution of the image by analyzing some intensity profiles? How does it compare to that of a diffraction limited image (assuming a given objective and wavelength)? This question requires you to make some assumptions and doesn't have one correct answer - just state the assumptions that you make. Also remember that the pixel size of an image is not the same as the resolution of an image and your estimates on resolution should be in microns, not pixels.

# 3a. Generate and display the 2D PSF of each of the objectives at a wavelength of 500 nm. To do this you will need to create a 2D grid of values with spacings appropriate for the objective. The PSF can be displayed as an intensity map or a surface map and should have axes labeled in microns. The lecture notes have examples of 2D displays of PSF's.

# 3b. Plot the profile through the center of the PSF for both objectives. The x axis should be in microns.

# 4. If the neurons are imaged with the two objectives above, what will the images look like? To answer this question, you should create 2 new images numerically in matlab using the principles of image formation and point spread functions calculated in problem 3. You should include an explanation of your work and matlab code that you write. Your analysis should include at least the following:

# 4a. Calculated images of the neuron for each objective.
# 4b. Intensity profiles through a few regions in the original and calculated images. How do these intensity profiles compare to your results from problem 2? What is the cause of any differences?
