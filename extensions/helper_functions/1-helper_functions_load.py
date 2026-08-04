# Simple CSV loading function

#@pn.cache
def load_csv_data(file_path):
    """
    Load CSV data from a given file path and handle potential mixed types.
    """
    try:
        # Attempt to load the CSV with low_memory=False to avoid dtype inference warnings
        return pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None

# Enhanced CSV loading function

# @pn.cache
def load_and_combine_csv_data(file_path):
    """
    Loads and combines multiple CSV files from the specified folder.
    Handles potential dtype issues and suppresses warnings.
    Returns the combined dataset as a DataFrame.
    """
    # # Get all CSV files in the folder
    # csv_files = glob.glob(os.path.join(file_path, "*.csv"))
    
    # Get all CSV files matching the pattern `estat_nrg_cb_*`
    csv_files = glob.glob(os.path.join(file_path, "estat_nrg_cb_*.csv"))
    
    # Load and combine all matching CSV files into a single DataFrame
    data_frames = []
    for file in csv_files:
        try:
            # Load each file with low_memory=False to suppress DtypeWarning
            df = pd.read_csv(file, low_memory=False)
            data_frames.append(df)
        except Exception as e:
            print(f"Error loading file {file}: {e}")
    
    # Combine all loaded DataFrames
    data = pd.concat(data_frames, ignore_index=True)
    
    return data

#@pn.cache
def load_geojson(file_path):
    """
    Load GeoJSON data from a given file path and cache it.
    """
    with open(file_path) as f:
        return json.load(f)