#@pn.cache
def split_and_melt_data(data):
    """
    Reformat dataset into long format (with 'year' and 'value' columns).
    """
    try:
        # Ensure the first column is of type string
        data.iloc[:, 0] = data.iloc[:, 0].astype(str)

        # Split the first column into separate columns for freq, nrg_bal, siec, unit, and geo
        split_data = data.iloc[:, 0].str.split(',', expand=True)

        # Check if the number of splits matches the expected number of columns
        if split_data.shape[1] != 5:
            raise ValueError(f"Expected 5 columns after splitting, but got {split_data.shape[1]}.")

        # Assign proper column names
        split_data.columns = ['freq', 'nrg_bal', 'siec', 'unit', 'geo']

        # Drop the original combined column and append split columns to the dataframe
        data = pd.concat([split_data, data.drop(columns=data.columns[0])], axis=1)

        # Melt the dataset to long format:
        melted_data = pd.melt(
            data,
            id_vars=['freq', 'nrg_bal', 'siec', 'unit', 'geo'],
            var_name='year',
            value_name='value'
        )

        return melted_data

    except Exception as e:
        print(f"Error during split_and_melt_data: {e}")
        return None
