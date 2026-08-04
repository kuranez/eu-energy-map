#@pn.cache
def clean_data(melted_data):
    """
    Cleans the melted data by renaming columns and processing values.
    """
    # Rename Columns for better readability
    cleaned_data = melted_data.rename(columns={
        'nrg_bal': 'Energy Type',
        'geo': 'Country Code',
        'value': 'Renewable Percentage'
    })
    
    # Data Conversion
    cleaned_data['Year'] = pd.to_numeric(cleaned_data['year'].str.extract(r'(\d{4})', expand=False), errors='coerce')
    cleaned_data['Renewable Percentage'] = pd.to_numeric(cleaned_data['Renewable Percentage'], errors='coerce').round(1)
    cleaned_data = cleaned_data.dropna(subset=['Year', 'Renewable Percentage'])

    # Rename entries in 'Energy Type'
    cleaned_data['Energy Type'] = cleaned_data['Energy Type'].replace({
        'REN': 'Renewable Energy Total',
        'REN_ELC': 'Renewable Electricity',
        'REN_HEAT_CL': 'Renewable Heating and Cooling',
        'REN_TRA': 'Renewable Energy in Transport'
    })

    # Dropping unnecessary columns
    cleaned_data = cleaned_data.drop(columns=['unit', 'freq', 'year'], errors='ignore')

    # Debugging: Print column names after cleanup
    # print("Columns after cleanup:", cleaned_data.columns.tolist())
    
    return cleaned_data