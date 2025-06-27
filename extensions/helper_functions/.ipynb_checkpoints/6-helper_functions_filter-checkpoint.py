@pn.cache
def filter_by_country_codes(dataset, country_codes):
    """
    Filters the dataset based on a list of country codes.
    """
    return dataset[dataset['Country Code'].isin(country_codes)]