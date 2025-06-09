# utils/flags.py

# Method to convert ISO2 country code to flag emoji
def iso2_to_flag(iso2_code: str) -> str:
    """
    Convert ISO2 country code to flag emoji.
    Example: 'DE' -> 🇩🇪
    
    Args:
        iso2_code (str): A two-letter ISO 3166-1 alpha-2 country code.
    
    Returns:
        str: The corresponding flag emoji or an empty string if the input is invalid.
    """
    if not isinstance(iso2_code, str) or len(iso2_code) != 2:
        return ""
    return chr(0x1F1E6 + ord(iso2_code[0].upper()) - ord('A')) + chr(0x1F1E6 + ord(iso2_code[1].upper()) - ord('A'))