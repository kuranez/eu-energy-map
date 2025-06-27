# Get the list of unique countries, EU countries, available years and energy types
all_countries = final_dataset[['Country Code', 'Country', 'Country Flag']].drop_duplicates()
eu_countries = final_dataset[final_dataset['Country Code'].isin(eu_country_codes)][['Country Code', 'Country', 'Country Flag']].drop_duplicates()
energy_types = final_dataset['Energy Type'].drop_duplicates().sort_values()
years = sorted(final_dataset['Year'].unique())

# Create Markdown Pane for All Countries (with flag first)
all_countries_md = f"### All Countries ({len(all_countries)})\n"
all_countries_md += "\n".join([f"- {flag} **{iso2}**: {country}" for iso2, country, flag in all_countries.values])

# Wrap in Accordion Pane
all_countries_pane = pn.pane.Markdown(all_countries_md)
countries_accordion = pn.Accordion(('All Countries', all_countries_pane), sizing_mode='stretch_width')

# Helper for missing country data
def identify_missing_eu_countries(dataset, expected_eu_countries):
    """
    Identifies missing EU countries by comparing expected and actual country codes.
    
    Args:
        dataset (pd.DataFrame): The dataset containing country information. Must include a 'Country Code' column.
        expected_eu_countries (iterable of str): A collection of expected EU country ISO2 codes.

    Returns:
        list of tuples: A list of missing countries, each represented as a tuple 
                        (ISO2 code, country name, country flag).
    """
    # Extract actual country codes from the dataset
    actual_country_codes = set(dataset['Country Code'].unique())

    # Find missing country codes
    missing_country_codes = set(eu_country_codes) - actual_country_codes

    # Retrieve country details for missing codes
    missing_countries = [
        (iso2, get_country_name(iso2), iso2_to_flag(iso2))
        for iso2 in missing_country_codes
    ]
    return missing_countries

def get_country_name(iso2_code):
    """
    Retrieve country name from ISO2 code using dataset or fallback mapping.
    
    Args:
        iso2_code (str): The two-character ISO code for the country.

    Returns:
        str: The name of the country if found, or "Unknown" if not.
    """
    # Attempt to look up in dataset first
    country_row = final_dataset[final_dataset['Country Code'] == iso2_code]
    if not country_row.empty:
        return country_row.iloc[0]['Country']

    # Fallback to static mapping
    country_name_mapping = {
        'GR': 'Greece',
        # Add additional mappings if necessary
    }
    return country_name_mapping.get(iso2_code, "Unknown")

# Map countries to flags (ensure dataset is loaded)
country_flag_map = {iso2: iso2_to_flag(iso2) for iso2 in final_dataset['Country Code'].unique()}

# Identify missing EU countries
missing_eu_countries = identify_missing_eu_countries(final_dataset, eu_country_codes)

# Create Missing EU Countries Markdown
if missing_eu_countries:
    missing_md = "### Missing Data for:\n"
    missing_md += "\n".join([f"- {flag} **{iso2}**: {name}" for iso2, name, flag in missing_eu_countries])
else:
    missing_md = "### All EU Countries Have Data"

# Combine EU countries and missing data into one Markdown string
eu_countries_md = f"### EU Countries ({len(eu_countries)})\n"
eu_countries_md += "\n".join([f"- {flag} **{iso2}**: {country}" for iso2, country, flag in eu_countries.values])
eu_countries_md += f"\n\n{missing_md}"  # Append missing data here

# Create Markdown pane
eu_countries_pane = pn.pane.Markdown(eu_countries_md)

# Wrap in Accordion Pane
eu_accordion = pn.Accordion(('EU Countries', eu_countries_pane), sizing_mode='stretch_width')

# Create Markdown Pane for Available Years (with count)
years_md = f"### Available Years ({len(years)})\n"
years_md += "\n".join([f"- {year}" for year in years])

# Wrap in Accordion Pane
years_pane = pn.pane.Markdown(years_md, sizing_mode='stretch_width')
years_accordion = pn.Accordion(('Years', years_pane), sizing_mode='stretch_width')

# Create Markdown Pane for Energy Types (with count)
energy_types_md = f"### Energy Types ({len(energy_types)})\n"
energy_types_md += "\n".join([f"- {etype}" for etype in energy_types])

# Wrap in Accordion Pane
energy_types_pane = pn.pane.Markdown(energy_types_md, sizing_mode='stretch_width')
energy_types_accordion = pn.Accordion(('Energy Types', energy_types_pane), sizing_mode='stretch_width')

# Combine panes into a single section with all the accordions
countries_and_energy_types = pn.Column(
    pn.pane.Markdown("## Data Summary: List of Countries, Energy Types and Available Years"),
    energy_types_accordion,
    pn.Row(countries_accordion, eu_accordion, years_accordion),
    sizing_mode='stretch_width'
)