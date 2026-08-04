def summarize_debug(stage_name, data, as_accordion=True, max_cell_length=15):
    """
    Generate a detailed summary of the data at a given stage for debugging purposes.
    Supports both console output and Panel accordion format.
    
    Parameters:
    - stage_name (str): Name of the debugging stage.
    - data: The data to be summarized (DataFrame, GeoDataFrame, or dict).
    - as_accordion (bool): Whether to return output as a Panel Accordion.
    - max_cell_length (int): Maximum number of characters per cell in the output.
    """
    # Initialize summary content
    summary_md = f"## Debug Summary: {stage_name}\n\n"
    
    # Process data
    if isinstance(data, (pd.DataFrame, gpd.GeoDataFrame)):
        summary_md += "### Data Type: DataFrame/GeoDataFrame\n\n"
        summary_md += f"- **Shape**: {data.shape}\n"
        summary_md += f"- **Columns**: {', '.join(data.columns)}\n\n"
        summary_md += "### Sample Data:\n\n"
        
        # Create a simple Markdown table for the first few rows
        headers = "| " + " | ".join(data.columns) + " |"
        separator = "| " + " | ".join(["---"] * len(data.columns)) + " |"
        
        # Truncate cell content to max_cell_length
        def truncate_cell(value):
            value_str = str(value)
            return value_str[:max_cell_length] + "..." if len(value_str) > max_cell_length else value_str
        
        rows = "\n".join(
            "| " + " | ".join(truncate_cell(cell) for cell in row) + " |"
            for row in data[0:5].itertuples(index=False, name=None)  # Use tuples for efficient iteration
        )
        summary_md += headers + "\n" + separator + "\n" + rows + "\n"
    
    elif isinstance(data, dict):  # For GeoJSON data
        summary_md += "### Data Type: Dictionary (GeoJSON)\n\n"
        summary_md += f"- **Keys**: {', '.join(data.keys())}\n"
        summary_md += f"- **Features Count**: {len(data.get('features', []))}\n"
    else:
        summary_md += "### Data Type: Unknown\n\n"
        summary_md += str(data)
    
    # Console Output
    if not as_accordion:
        print(f"=== {stage_name} ===")
        print(summary_md)
        print("\n")
        return None
    
    # Accordion Output
    summary_pane = pn.pane.Markdown(summary_md, sizing_mode='stretch_width')
    accordion_pane = pn.Accordion((stage_name, summary_pane), sizing_mode='stretch_width')
    
    return accordion_pane