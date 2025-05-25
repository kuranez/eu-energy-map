# utils/colors.py

from plotly.colors import sample_colorscale, hex_to_rgb
import plotly.express as px

# Define the Viridis colorscale from Plotly Express

VIRIDIS = px.colors.sequential.Viridis

# Color conversion utilities

def _tuple_to_hex(rgb_tuple):
    """Convert (r, g, b) tuple to hex string."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)

def _hex_to_rgba(hex_color, alpha):
    """Convert hex color to rgba string."""
    r, g, b = hex_to_rgb(hex_color)
    return f"rgba({r},{g},{b},{alpha})"

# Global Viridis colorscale

def get_colorscale():
    """Return global Viridis scale."""
    return VIRIDIS

# Normalize value to [0, 1] range

def normalize_value(value: float, scale_max: float = 100.0) -> float:
    """
    Normalize a value to [0, 1] range based on the maximum.
    """
    return min(max(value / scale_max, 0), 1)

# Sample Viridis color based on normalized value

def get_viridis_color(value: float, scale_max: float = 100.0, fmt: str = 'hex', alpha: float = 1.0) -> str:
    """
    Sample a color from Viridis scale in hex or rgba.

    Parameters:
    - value: input percentage (0–100)
    - scale_max: max value for normalization (default: 100)
    - fmt: 'hex' or 'rgba'
    - alpha: transparency level for rgba format (0–1)

    Returns:
    - Color string in hex or rgba
    """
    normalized = normalize_value(value, scale_max)
    hex_color = sample_colorscale(VIRIDIS, normalized)[0]

    # Ensure hex_color is a string
    if isinstance(hex_color, tuple):
        hex_color = _tuple_to_hex(hex_color)

    if fmt == 'hex':
        return hex_color
    elif fmt == 'rgba':
        return _hex_to_rgba(hex_color, alpha)
    else:
        raise ValueError("fmt must be either 'hex' or 'rgba'")