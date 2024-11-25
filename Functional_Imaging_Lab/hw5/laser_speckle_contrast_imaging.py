import numpy as np
import matplotlib.pyplot as plt
import os

# %%
def read_8bit_grayscale_memmap(fname):
    """
    Reads a binary file containing 8-bit grayscale images using memory mapping.
    
    Parameters:
        fname (str): Path to the binary file.
        
    Returns:
        numpy.ndarray: A 3D array (N_images, height, width) representing the image stack.
    """
    try:
        # Read header separately first
        with open(fname, 'rb') as file:
            header = np.fromfile(file, dtype=np.uint16, count=4)
            width, height, n_images, _ = header
            
            # Print header values for debugging
            print(f"Header values - Width: {width}, Height: {height}, N_images: {n_images}")
            
            # Calculate offset for image data (8 bytes for header)
            offset = 8
            
            # Calculate expected size using int64 to avoid overflow
            expected_size = offset + np.int64(width) * np.int64(height) * np.int64(n_images)
            
            # Get file size
            file_size = os.path.getsize(fname)
            print(f"File size: {file_size}, Expected size: {expected_size}")
            
            # # Read a small portion to verify data format
            # file.seek(offset)
            # sample = np.fromfile(file, dtype=np.uint8, count=min(1000, width * height))
            # print(f"Sample data range: {sample.min()} to {sample.max()}")
            
            if file_size < expected_size:
                print(f"Warning: File seems truncated")
                return None
                
            # Memory map the file
            mm = np.memmap(fname, 
                          dtype=np.uint8,
                          mode='r',
                          offset=offset,
                          shape=(n_images, height, width))
            
            # Convert to regular numpy array
            images = np.array(mm)
            
            print(f"Successfully loaded array of shape {images.shape}")
            print(f"Max: {np.max(images)}, Min: {np.min(images)}, Average: {np.mean(images)}")
            return images
            
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# # %%
# for i in range(1, 102):  # Files numbered from 1 to 101
#     filename = f'media/raw.{i:04d}'  # Format filename with leading zeros
#     # roi_means = read_8bit_grayscale(filename)
#     images = read_8bit_grayscale_memmap(filename)
#     for i in range(images.shape[0]):
#         plt.imshow(images[i], cmap='gray')
#         plt.show()

# %%
test =read_8bit_grayscale_memmap('media/raw.0001')
plt.imshow(test[0])

# %%
