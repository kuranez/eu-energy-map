@pn.cache
def merge_data(geojson_file, csv_data, merge_key_geo, merge_key_csv):
    """
    Merge GeoJSON and CSV data on specified keys and cache the result.
    """
    geo_df = gpd.read_file(geojson_file)
    return geo_df.merge(csv_data, left_on=merge_key_geo, right_on=merge_key_csv)