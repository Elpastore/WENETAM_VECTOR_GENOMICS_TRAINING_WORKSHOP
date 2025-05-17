import pandas as pd
import plotly.express as px
from typing import Optional, Union, List
from textwrap import dedent

def plot_frequencies_heatmap(
    df: pd.DataFrame,
    index: Optional[Union[str, List[str]]] = "label",
    max_len: Optional[int] = 100,
    col_width: int = 40,
    row_height: int = 20,
    x_label: Optional[str] = "Cohorts",
    y_label: Optional[str] = "Variants",
    colorbar: bool = True,
    width: Optional[int] = None,
    height: Optional[int] = None,
    text_auto: Union[bool, str] = ".0%",
    aspect: str = "auto",
    color_continuous_scale: str = "Reds",
    title: Union[bool, str, None] = True,
    show: bool = True,
    renderer: Optional[str] = None,
    **kwargs,
):
    # Check for too many rows
    if max_len and len(df) > max_len:
        raise ValueError(dedent(
            f"""
            Input DataFrame is longer than max_len parameter value {max_len}, which means
            that the plot is likely to be very large. If you really want to go ahead,
            please rerun the function with max_len=None.
            """
        ))

    # Handle title
    if title is True:
        title = df.attrs.get("title", None)

    # Determine index column
    if index is None:
        index = list(df.index.names)

    df = df.reset_index().copy()

    if isinstance(index, list):
        index_col = (
            df[index]
            .astype(str)
            .apply(lambda row: ", ".join([o for o in row if o is not None]), axis="columns")
        )
    else:
        assert isinstance(index, str)
        index_col = df[index].astype(str)

    if not index_col.is_unique:
        raise ValueError(f"{index} does not produce a unique index")

    # Extract columns that start with 'frq_'
    frq_cols = [col for col in df.columns if col.startswith("frq_")]
    heatmap_df = df[frq_cols].copy()
    heatmap_df.set_index(index_col, inplace=True)
    heatmap_df.columns = heatmap_df.columns.str.lstrip("frq_")

    # Calculate width and height
    if width is None:
        width = 400 + col_width * len(heatmap_df.columns)
        if colorbar:
            width += 40
    if height is None:
        height = 200 + row_height * len(heatmap_df)
        if title is not None:
            height += 40

    # Create heatmap
    fig = px.imshow(
        img=heatmap_df,
        zmin=0,
        zmax=1,
        width=width,
        height=height,
        text_auto=text_auto,
        aspect=aspect,
        color_continuous_scale=color_continuous_scale,
        title=title,
        **kwargs,
    )

    fig.update_xaxes(side="bottom", tickangle=30)
    if x_label is not None:
        fig.update_xaxes(title=x_label)
    if y_label is not None:
        fig.update_yaxes(title=y_label)

    fig.update_layout(
        coloraxis_colorbar=dict(
            title="Frequency",
            tickvals=[0, 0.2, 0.4, 0.6, 0.8, 1.0],
            ticktext=["0%", "20%", "40%", "60%", "80%", "100%"],
        )
    )

    if not colorbar:
        fig.update(layout_coloraxis_showscale=False)

    if show:
        fig.show(renderer=renderer)
        return None
    else:
        return fig
