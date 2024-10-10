% Load the neuron image (replace with your image file)
neuron_img = imread('neuron.png');

% Parameters
wavelength = 0.5; % Wavelength in microns (500 nm)
NA1 = 1.4; % Numerical aperture for first objective
NA2 = 0.85; % Numerical aperture for second objective
k = 2 * pi / wavelength; % Wavenumber

% Create 2D grid for PSF calculation
grid_size = 10; % Grid size extends from -5 to 5 microns in both directions
step_size = 0.01; % Step size in microns
x = -grid_size:step_size:grid_size;
y = -grid_size:step_size:grid_size;
[X, Y] = meshgrid(x, y);
r = sqrt(X.^2 + Y.^2); % Radial distance from the center

% Airy Disk PSF formula: PSF(r) = (2 * J1(k * r * NA) / (k * r * NA))^2
% PSF for Objective 1 (NA = 1.4)
PSF1 = (2 * besselj(1, k * r * NA1) ./ (k * r * NA1)).^2;
PSF1(r == 0) = 1; % Handle singularity at r = 0

% PSF for Objective 2 (NA = 0.85)
PSF2 = (2 * besselj(1, k * r * NA2) ./ (k * r * NA2)).^2;
PSF2(r == 0) = 1; % Handle singularity at r = 0

% Normalize the PSFs to ensure they sum to 1
PSF1 = PSF1 / sum(PSF1(:));
PSF2 = PSF2 / sum(PSF2(:));

% Perform convolution to simulate image formation for Objective 1
neuron_img_obj1 = conv2(double(neuron_img), PSF1, 'same');

% Perform convolution to simulate image formation for Objective 2
neuron_img_obj2 = conv2(double(neuron_img), PSF2, 'same');

% Display the original and convolved images
figure;

subplot(1, 3, 1);
imshow(neuron_img, []);
title('Original Neuron Image');
axis off;

subplot(1, 3, 2);
imshow(neuron_img_obj1, []);
title('Neuron Image with Objective 1 (NA 1.4)');
axis off;

subplot(1, 3, 3);
imshow(neuron_img_obj2, []);
title('Neuron Image with Objective 2 (NA 0.85)');
axis off;