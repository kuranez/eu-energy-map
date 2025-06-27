@pn.cache
def sort_columns(data, column_order):
    """
    Sort the DataFrame columns in the specified order.
    """
    return data[column_order]