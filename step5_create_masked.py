"""
Step 5: Create a masked stippled image by applying the block letter mask.
This demonstrates selection bias by systematically removing data points
in the shape of the mask (block letter "S").
"""

import numpy as np


def create_masked_stipple(
    stipple_img: np.ndarray,
    mask_img: np.ndarray,
    threshold: float = 0.5
) -> np.ndarray:
    """
    Apply the block letter mask to the stippled image.
    
    Where the mask is dark (below threshold), stipples are removed (set to white/1.0).
    Where the mask is light (above threshold), stipples are kept as they are.
    This creates the "biased estimate" by systematically removing data points.
    
    Parameters
    ----------
    stipple_img : np.ndarray
        Stippled image as 2D array (height, width) with values in [0, 1].
        0.0 = black dot (stipple), 1.0 = white background.
    mask_img : np.ndarray
        Mask image (block letter) as 2D array (height, width) with values in [0, 1].
        0.0 = black (mask area, remove stipples here),
        1.0 = white (keep area, preserve stipples here).
        Must have the same shape as stipple_img.
    threshold : float
        Threshold value that determines what counts as "part of the mask".
        Pixels with mask values below threshold are considered part of the mask
        and will have their stipples removed. Default 0.5.
    
    Returns
    -------
    masked_stipple : np.ndarray
        2D numpy array (height, width) with values in [0, 1].
        Same shape as input images.
        Pixels where mask < threshold are set to 1.0 (white, stipples removed).
        Pixels where mask >= threshold keep their original stipple values.
    
    Raises
    ------
    ValueError
        If stipple_img and mask_img have different shapes.
    """
    # Validate that images have the same shape
    if stipple_img.shape != mask_img.shape:
        raise ValueError(
            f"Images must have the same shape. "
            f"stipple_img shape: {stipple_img.shape}, "
            f"mask_img shape: {mask_img.shape}"
        )
    
    # Make a copy of the stippled image to avoid modifying the original
    masked_stipple = stipple_img.copy()
    
    # Apply the mask:
    # - Where mask is dark (below threshold): remove stipples by setting to 1.0 (white)
    # - Where mask is light (above threshold): keep stipples as they are
    # The mask image has 0.0 = black (mask area) and 1.0 = white (keep area)
    mask_area = mask_img < threshold
    
    # Set masked areas to white (1.0), effectively removing stipples
    masked_stipple[mask_area] = 1.0
    
    return masked_stipple

