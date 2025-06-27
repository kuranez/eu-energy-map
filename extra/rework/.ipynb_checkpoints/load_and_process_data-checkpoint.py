def load_and_process_data():
    """
    Orchestrates the data loading, merging, cleaning, and formatting steps.
    Returns the final dataset and a collection of Panel Accordions summarizing each step.
    """
    debug_accordions = []  # Collect debug accordions for each step
    
    # Step 1: Load data
    csv_file_path = './data/estat_nrg_ind_ren.cs' 
    geojson_file_path = './data/europe.geojson'
    csv_data = load_csv_data(csv_file_path)
    debug_accordions.append(summarize_debug("Loaded CSV Data", csv_data))
    
    geo_data = load_geojson(geojson_file_path)
    debug_accordions.append(summarize_debug("Loaded GeoJSON File", geo_data))

    # Step 2: Split and melt the CSV data
    melted_data = split_and_melt_data(csv_data)
    debug_accordions.append(summarize_debug("Split and Melted Data", melted_data))

    # Step 3: Clean the melted data
    cleaned_data = clean_data(melted_data)
    debug_accordions.append(summarize_debug("Cleaned and Processed Data", cleaned_data))

    # Step 4: Add country flags
    flagged_data = add_country_flags(cleaned_data)
    debug_accordions.append(summarize_debug("Added Country Flags", flagged_data))

    # Step 5: Merge with GeoJSON data
    merge_key_geo = 'ISO2'  # The key in GeoJSON data
    merge_key_csv = 'Country Code'  # The key in CSV data
    
    merged_data = merge_data(geojson_file_path, flagged_data, merge_key_geo, merge_key_csv)
    merged_data = merged_data.rename(columns={'NAME': 'Country'})
    debug_accordions.append(summarize_debug("Merged GeoJSON and CSV Data", merged_data))

    # Step 6: Filter and sort the final dataset
    final_data = sort_columns(merged_data, final_columns_order)
    debug_accordions.append(summarize_debug("Reordered Columns (Final Data)", final_data))

    return final_data, debug_accordions