import cv2
import matplotlib.pyplot as plt
import numpy as np


# 2.
class Line:
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.first_as_tuple = (self.x1, self.y1)
        self.last_as_tuple = (self.x2, self.y2)


class Image:
    def __init__(self, png: str):
        self.img = cv2.imread(png)
        self.img_gray = cv2.imread(png, cv2.IMREAD_GRAYSCALE)

    def show_image(self):
        cv2.imshow("PRESS ANY KEY TO EXIT", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        cv2.waitKey(1)

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
line1 = Line(420, 100, 570, 100)
line2 = Line(700, 300, 800, 300)
line3 = Line(320, 800, 420, 800)
neuron = Image("neuron.png")

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
plt.figure()
plt.plot(x_vals, intensities, linewidth=2, label="Intensity")
plt.xlabel("X-Coordinate")
plt.ylabel("Intensity")
plt.title("Intensity at Given X Coordinates")
# plt.legend()
plt.grid(True)
plt.show()

res = dict(zip(x_vals, intensities))

inten_max = max(intensities)

# return first xval where inten < 0.5*maxintensity
for key in res:
    print(f"{key}, {res[key]}")

# We can see a local max of 235 at x value of 773, half of this is about 117.5, the next x value that measures less than half of the maximum intensity occurs at x val 777 with intensity of 92. this means the resolution is 4 pixels.

# ! left off at this point

# 3a. Generate and display the 2D PSF of each of the objectives at a wavelength of 500 nm. To do this you will need to create a 2D grid of values with spacings appropriate for the objective. The PSF can be displayed as an intensity map or a surface map and should have axes labeled in microns. The lecture notes have examples of 2D displays of PSF's.


# 3b. Plot the profile through the center of the PSF for both objectives. The x axis should be in microns.
## Condition for divide by zero at the center of PSF; take into account "isnan"

# 4. If the neurons are imaged with the two objectives above, what will the images look like? To answer this question, you should create 2 new images numerically in matlab using the principles of image formation and point spread functions calculated in problem 3. You should include an explanation of your work and matlab code that you write. Your analysis should include at least the following:

# 4a. Calculated images of the neuron for each objective.
# 4b. Intensity profiles through a few regions in the original and calculated images. How do these intensity profiles compare to your results from problem 2? What is the cause of any differences?
