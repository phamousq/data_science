import numpy as np
# import os

def read_raw_basler(fname, n_images=None, normalize=False):
    """
    Read raw Basler camera data from a binary file.
    
    Parameters:
    -----------
    fname : str
        Path to the input file
    n_images : int, optional
        Number of images to read. If None, reads all images in file
    normalize : bool, optional
        If True, normalizes the output to range [0, 1]
        
    Returns:
    --------
    numpy.ndarray or int
        3D array of image data (height x width x n_images) if successful,
        -1 if file cannot be opened
    """
    try:
        with open(fname, 'rb') as fp:
            # Read header information
            n1 = int.from_bytes(fp.read(2), byteorder='little', signed=False)
            n2 = int.from_bytes(fp.read(2), byteorder='little', signed=False)
            N = int.from_bytes(fp.read(2), byteorder='little', signed=False)
            
            # Use provided n_images if specified, otherwise use N from file
            n_images = N if n_images is None else n_images
            
            # Read image data
            data = np.frombuffer(fp.read(n1 * n2 * n_images), dtype=np.uint8)
            
            # Reshape data into 3D array (height x width x n_images)
            images = data.reshape((n2, n1, n_images))
            
            if normalize:
                # Convert to float and normalize to [0, 1]
                images = images.astype(np.float32) / 255.0
                
            return images
            
    except FileNotFoundError:
        print(f"\ncould not open {fname} for reading")
        return -1
