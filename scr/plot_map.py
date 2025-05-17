from ipyleaflet import Map, Marker, ScaleControl, Popup
from ipywidgets import HTML

def create_taxon_map(df, taxon_cols):
    """
    Create an interactive map from a multi-indexed DataFrame with sampling locations and taxon counts.
    Displays a popup with location, coordinates, and taxon data.
    
    Parameters:
    - df: DataFrame with MultiIndex (country, location), latitude, longitude, and taxon columns
    - taxon_cols: List of column names representing the taxons
    
    Returns:
    - ipyleaflet.Map
    """
    # Reset index to access country and location as columns
    df = df.reset_index()
    

    # Create the map
    m = Map(
        basemap=ipyleaflet.basemaps.OpenStreetMap.Mapnik,
        center=[0, 20],
        zoom=3,
    )

    # Add markers with popup
    for row in df.itertuples():
        taxon_info = "<br>".join(
            f"{col}: {getattr(row, col)}" for col in taxon_cols
        )

        html = HTML()
        html.value = (
            f"<b>{row.location}, {row.country}</b><br>"
            f"({row.latitude:.3f}, {row.longitude:.3f})<br><hr>"
            f"{taxon_info}"
        )

        marker = Marker(
            location=(row.latitude, row.longitude),
            draggable=False,
        )
        marker.popup = Popup(
            child=html,
            close_button=False,
            auto_close=False,
            close_on_escape_key=False
        )
        m.add_layer(marker)

    m.add_control(ScaleControl(position="bottomleft"))
    return m