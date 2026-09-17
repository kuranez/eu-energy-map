# Python 3.13 Migration

## Issue: Plotly 6.x changes requires modification of `map.py`

### Isolated Error Message

```text
AttributeError: module 'plotly.graph_objects' has no attribute 'Choroplethmapbox'. Did you mean: 'Choroplethmap'?
```

**Trigger Point:**
`components/map.py` Line 32
```python
File "/home/kuranez/Projects_new/python/eu-energy-map/components/map.py", line 32, in create_choropleth_map
    fig = go.Figure(go.Choroplethmapbox(
                    ^^^^^^^^^^^^^^^^^^^
```

---

### Summary

* **What broke:** In **Plotly v6.0.0**, all Mapbox-specific trace classes (`Choroplethmapbox`, `Scattermapbox`, `Densitymapbox`) and their layout counterparts (`layout.mapbox`, `mapbox_style`, etc.) were completely **removed**.
* **Why it changed:** Plotly migrated its mapping engine from proprietary **Mapbox GL JS** to the open-source **MapLibre GL JS**. This eliminates mandatory Mapbox access tokens for standard basemaps (like Carto/OSM) and unifies map traces.
* **Direct replacement:**
  * `go.Choroplethmapbox` to `go.Choroplethmap`
  * `mapbox_style` to `map_style`
  * `mapbox_zoom` to `map_zoom`
  * `mapbox_center` to `map_center`

---

### Fix

#### **1. Replace `go.Choroplethmapbox with go.Choroplethmap` with `go.Choroplethmap`**

@ `components/map.py` Line 32

**Current Code:**
```python
    fig = go.Figure(go.Choroplethmapbox(
        # Load the GeoJSON file for Europe
        geojson=json.load(open(GEOJSON_PATH)),
```

**Edit to:**
```python
    fig = go.Figure(go.Choroplethmap(
        # Load the GeoJSON file for Europe
        geojson=json.load(open(GEOJSON_PATH)),
```

#### **2. Update layout parameters from `mapbox_*` to `map_*`**

@ `components/map.py` Lines 63-74

**Current Code:**
```python
    # Update the layout of the map
    # Set the mapbox style, zoom level, and center
    fig.update_layout(
        # Set the Mapbox access token
        mapbox_accesstoken=MAPBOX_TOKEN,
        # Use a predefined Mapbox style
        mapbox_style="carto-positron",
        # Set the initial zoom level and center of the map
        mapbox_zoom=2.75,
        # Center the map on Europe
        mapbox_center={"lat": 56, "lon": 8},
        # Remove margins around the map
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
```

**Edit to:**
```python
    # Update the layout of the map
    # Set the map style, zoom level, and center
    fig.update_layout(
        # Use a predefined MapLibre style (carto-positron does not require an access token)
        map_style="carto-positron",
        # Set the initial zoom level and center of the map
        map_zoom=2.75,
        # Center the map on Europe
        map_center={"lat": 56, "lon": 8},
        # Remove margins around the map
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
```

---

### Official Citations & Documentation

1. **Plotly v6.0.0 Release Notes (GitHub)**:
   > *"Breaking changes: Removed deprecated Mapbox traces (`scattermapbox`, `choroplethmapbox`, `densitymapbox`) in favor of MapLibre traces (`scattermap`, `choroplethmap`, `densitymap`)."*  
   > 🔗 [Plotly.py Release v6.0.0](https://github.com/plotly/plotly.py/releases/tag/v6.0.0)

2. **Plotly MapLibre Migration Guide**:
   > Details the full transition from Mapbox to MapLibre, trace renames, and parameter mapping.  
   > 🔗 [Plotly MapLibre Migration Guide](https://plotly.com/python/maplibre-migration/)

3. **Plotly Tile Map Documentation**:
   > Reference documentation and examples for `go.Choroplethmap`.  
   > 🔗 [Plotly Choropleth Map Documentation](https://plotly.com/python/choropleth-maps/)
