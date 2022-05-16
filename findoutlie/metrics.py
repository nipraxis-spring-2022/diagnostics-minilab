""" Scan outlier metrics
"""

#+ Your imports here.
import numpy as np
import nibabel as nib

def dvars(img):
    """ Calculate dvars metric on Nibabel image `img`

    The dvars calculation between two volumes is defined as the square root of
    (the sum of the (voxel differences squared) divided by the number of
    voxels).

    Parameters
    ----------
    img : nibabel image

    Returns
    -------
    dvals : 1D array
        One-dimensional array with n-1 elements, where n is the number of
        volumnes in `img`.
    """
    data = img.get_fdata()
    d = data[..., 1:] - data[..., :-1]
    result = np.sqrt(np.mean(d**2, axis=(0,1,2))) 
    return result