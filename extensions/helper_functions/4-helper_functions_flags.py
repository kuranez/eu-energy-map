#@pn.cache
def iso2_to_flag(iso2_code):
    """
    Convert an ISO2 country code to its corresponding flag emoji.
    """
    try:
        return ''.join(chr(127397 + ord(c)) for c in iso2_code.upper())
    except Exception:
        return '🏳️'  # Default fallback flag

#@pn.cache
def add_country_flags(data):
    """
    Add country flags to the dataset using country codes.
    """
    data['Country Flag'] = data['Country Code'].apply(iso2_to_flag)
    return data