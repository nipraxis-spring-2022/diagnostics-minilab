""" Module with routines for finding outliers
"""

import os.path as op
from glob import glob
from functools import partial

import numpy as np
import nibabel as nib

from findoutlie.detectors import std_detector, iqr_detector
from findoutlie.metrics import dvars
from findoutlie.spm_funcs import get_spm_globals

def detect_outliers(fname, metric='vol_means', detector='std', 
                    n_stds=2, iqr_proportion=1.5, mask_join='or'):
    """
    Choose a timecourse metric and outlier detection method to apply to a given
    file.

    Parameters
    ----------
    fname : str, the timeseries file to be processed for outliers 

    metric options : can be a str or list of options
        The metric used for summarizing timecourse data across volumes before
        applying outlier detecton method.

        Options can include:
        -'vol_means'
        -'dvars'
        -'spm_global'
        -'all' (chooses all of the above)
        -list of some or all of the above options

    detector options : can be a str or list of options
        The outlier detection method to use.

        Options can include:
        -'std'
        -'iqr'
        -'all' (chooses all of the above)
        -list of some or all of the above options
    
    n_stds : int or float (default=2)
        The standard deviation threshold used with the 'std' 
        detector method.

    iqr_proportion : int or float (default=1.5)
        The interquartile proportion threshold to use with the
        'iqr' method.

    mask_join : str (default='or')
        The method used to join outlier masks obtained when multiple
        metrics or detection methods are used.

        Options can be 'or' for np.logical_or or 'and' for np.logical_and.
    """

    metric_funcs = {
        'vol_means': (lambda file: np.mean(nib.load(file).get_fdata(), axis=(0,1,2))),
        'dvars': (lambda file: dvars(nib.load(file))),
        'spm_global': (lambda file: np.array(get_spm_globals(file)))
    }

    detector_funcs = {
        'std': partial(std_detector, n_stds=n_stds),
        'iqr': partial(iqr_detector, iqr_proportion=iqr_proportion)
    }
    assert type(metric) in [list, str], "'metric' must be a str or list"
    assert type(detector) in [list, str], "'detector' must be str or list"
    assert mask_join in ['or', 'and'], "'mask_join' must be 'or' or 'and'"

    if mask_join == 'or':
        mask_join = np.logical_or
    elif mask_join == 'and':
        mask_join = np.logical_and
    
    if type(metric) == str:
        if metric == 'all':
            metric = list(metric_funcs.keys())
        else:
            metric = [metric]
    if type(detector) == str:
        if detector == 'all':
            detector = list(detector_funcs.keys())
        else:
            detector = [detector]

    n_trs = nib.load(fname).shape[-1]
    master_mask = np.full(n_trs, fill_value=False)
    for m in metric:
        metric_data = metric_funcs[m](fname)
        for d in detector:
            outlier_mask = detector_funcs[d](metric_data)
            if m=='dvars':
                outlier_mask = np.append(True, outlier_mask) # pass dvars mask with a True
            master_mask = mask_join(master_mask, outlier_mask)

    if len(master_mask) == 0:
        return [None]
    else:
        return np.where(master_mask)[0] # return True value indices


def find_outliers(data_directory, metric='vol_means', detector='std',
                n_stds=2, iqr_proportion=1.5, mask_join='or'):
    """ Return filenames and outlier indices for images in `data_directory`.

    Parameters
    ----------
    data_directory : str
        Directory containing containing images.

    Returns
    -------
    outlier_dict : dict
        Dictionary with keys being filenames and values being lists of outliers
        for filename.
    """
    image_fnames = glob(op.join(data_directory, '**', 'sub-*.nii.gz'),
                        recursive=True)
    outlier_dict = {}
    for fname in image_fnames:
        print(f"Finding outliers for {fname}")
        outliers = detect_outliers(fname, metric, detector, 
                            n_stds, iqr_proportion, mask_join)
        outlier_dict[fname] = outliers
    return outlier_dict
