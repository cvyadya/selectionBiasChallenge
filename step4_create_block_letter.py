"""
Step 4: Create a block letter "S" matching image dimensions.
Generates a block letter pattern for the selection bias meme.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Optional
import platform
import os


def _find_font_path() -> Optional[str]:
    """
    Try to find a suitable bold font path across different operating systems.
    
    Returns
    -------
    font_path : Optional[str]
        Path to a bold font file, or None if no suitable font is found.
    """
    system = platform.system()
    
    # Common font paths by operating system
    font_paths = []
    
    if system == "Windows":
        font_paths = [
            "C:/Windows/Fonts/arialbd.ttf",  # Arial Bold
            "C:/Windows/Fonts/arial.ttf",    # Arial (fallback)
            "C:/Windows/Fonts/calibrib.ttf", # Calibri Bold
            "C:/Windows/Fonts/calibri.ttf",  # Calibri (fallback)
            "C:/Windows/Fonts/impact.ttf",   # Impact
            "C:/Windows/Fonts/timesbd.ttf",  # Times Bold
        ]
    elif system == "Darwin":  # macOS
        font_paths = [
            "/Library/Fonts/Arial Bold.ttf",
            "/Library/Fonts/Arial.ttf",
            "/Library/Fonts/Helvetica Bold.ttf",
            "/Library/Fonts/Helvetica.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
    else:  # Linux
        font_paths = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        ]
    
    # Try each font path
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    
    return None


def create_block_letter_s(
    height: int,
    width: int,
    letter: str = "S",
    font_size_ratio: float = 0.9
) -> np.ndarray:
    """
    Create a block letter pattern matching the specified image dimensions.
    
    Parameters
    ----------
    height : int
        Height of the output image in pixels
    width : int
        Width of the output image in pixels
    letter : str
        Letter to render (default: "S")
    font_size_ratio : float
        Ratio of font size to image dimension (default: 0.9).
        Font size will be calculated as min(height, width) * font_size_ratio
    
    Returns
    -------
    letter_array : np.ndarray
        2D numpy array (height × width) with values in [0, 1].
        Black letter (0.0) on white background (1.0).
    """
    # Create a white background image
    img = Image.new('L', (width, height), color=255)  # 'L' mode = grayscale, 255 = white
    draw = ImageDraw.Draw(img)
    
    # Calculate font size based on image dimensions
    font_size = int(min(height, width) * font_size_ratio)
    
    # Try to load a bold font, fall back to default if not found
    font = None
    font_path = _find_font_path()
    if font_path:
        try:
            font = ImageFont.truetype(font_path, font_size)
        except (OSError, IOError):
            font = None
    
    # If no font found, use default (may not be bold but will work)
    if font is None:
        try:
            # Try default font (PIL's default)
            font = ImageFont.load_default()
        except:
            font = None
    
    # Calculate text position to center it
    # Get text bounding box to calculate position
    bbox = None
    if font:
        try:
            # Try newer Pillow API (8.0.0+)
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), letter, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                bbox_y_offset = bbox[1]
            else:
                # Fallback to older API (textsize)
                text_width, text_height = draw.textsize(letter, font=font)
                bbox_y_offset = 0
        except (AttributeError, TypeError):
            # Fallback: estimate size
            text_width = font_size * len(letter) * 0.6
            text_height = font_size
            bbox_y_offset = 0
    else:
        # No font available, estimate size
        text_width = font_size * len(letter) * 0.6
        text_height = font_size
        bbox_y_offset = 0
    
    # Center the text
    x = (width - text_width) / 2
    y = (height - text_height) / 2 - bbox_y_offset
    
    # Draw the letter in black (0 = black in 'L' mode)
    if font:
        draw.text((x, y), letter, fill=0, font=font)  # fill=0 = black
    else:
        draw.text((x, y), letter, fill=0)  # fill=0 = black
    
    # Convert PIL image to numpy array and normalize to [0, 1]
    # PIL 'L' mode: 0=black, 255=white
    # Normalized: 0.0=black, 1.0=white (which is what we want)
    letter_array = np.array(img, dtype=np.float32) / 255.0
    
    return letter_array

