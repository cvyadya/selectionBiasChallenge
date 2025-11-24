"""
Create the final statistics meme by assembling all four panels.
This function creates a professional 1×4 layout showing:
- Reality (original image)
- Your Model (stippled image)
- Selection Bias (block letter S)
- Estimate (masked stippled image)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


def create_statistics_meme(
    original_img: np.ndarray,
    stipple_img: np.ndarray,
    block_letter_img: np.ndarray,
    masked_stipple_img: np.ndarray,
    output_path: str,
    dpi: int = 150,
    background_color: str = "white"
) -> None:
    """
    Create a professional four-panel statistics meme demonstrating selection bias.
    
    Parameters
    ----------
    original_img : np.ndarray
        Original grayscale image (Reality panel) as 2D array (height, width) with values in [0, 1]
    stipple_img : np.ndarray
        Stippled image (Your Model panel) as 2D array (height, width) with values in [0, 1]
    block_letter_img : np.ndarray
        Block letter image (Selection Bias panel) as 2D array (height, width) with values in [0, 1]
    masked_stipple_img : np.ndarray
        Masked stippled image (Estimate panel) as 2D array (height, width) with values in [0, 1]
    output_path : str
        Path where the output PNG file will be saved
    dpi : int
        Resolution in dots per inch for the output image. Default 150.
        Higher values (200-300) produce better quality for publication.
    background_color : str
        Background color for the meme. Default "white".
        Can be any valid matplotlib color name (e.g., "pink", "lightgray", etc.)
    
    Returns
    -------
    None
        The function saves the meme image to the specified output_path.
    
    Raises
    ------
    ValueError
        If images have incompatible shapes (should all have the same shape).
    """
    # Validate that all images have the same shape
    img_shape = original_img.shape
    images = {
        "original": original_img,
        "stipple": stipple_img,
        "block_letter": block_letter_img,
        "masked_stipple": masked_stipple_img
    }
    
    for name, img in images.items():
        if img.shape != img_shape:
            raise ValueError(
                f"All images must have the same shape. "
                f"{name}_img shape: {img.shape}, expected: {img_shape}"
            )
    
    # Panel labels
    labels = ["Reality", "Your Model", "Selection Bias", "Estimate"]
    panel_images = [original_img, stipple_img, block_letter_img, masked_stipple_img]
    
    # Create figure with 1×4 layout
    # Use GridSpec for better control over spacing
    fig = plt.figure(figsize=(16, 4.5), facecolor=background_color, dpi=dpi)
    gs = GridSpec(1, 4, figure=fig, hspace=0.1, wspace=0.03, 
                  left=0.02, right=0.98, top=0.88, bottom=0.1)
    
    # Create subplots for each panel
    axes = []
    for i in range(4):
        ax = fig.add_subplot(gs[0, i])
        ax.imshow(panel_images[i], cmap='gray', vmin=0, vmax=1, aspect='auto')
        ax.axis('off')
        
        # Add label above each panel
        # Position label slightly above the axes
        ax.text(0.5, 1.08, labels[i], 
                transform=ax.transAxes,
                fontsize=18,
                fontweight='bold',
                ha='center',
                va='bottom',
                color='black')
        
        axes.append(ax)
    
    # Save the figure
    plt.savefig(output_path, dpi=dpi, facecolor=background_color, 
                bbox_inches='tight', pad_inches=0.1)
    plt.close()
    
    # print(f"Statistics meme saved to: {output_path}")

