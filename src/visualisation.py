from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import panel as pn
import seaborn as sns


sns.set_theme(style="whitegrid")

empty_plot = pn.Spacer(
    styles={"background": "gray"},
    sizing_mode="stretch_both",
)


def plot_lines(sampled_df: pd.DataFrame, interesting_cols: List[str], fig_path=None):
    # Plotting the interesting columns with improved performance and cleaner rendering for high density of points
    fig, ax = plt.subplots(figsize=(10, 6))
    for col in interesting_cols:
        subset = sampled_df[pd.notna(sampled_df[col])]
        ax.plot(subset.index, subset[col], label=col, linewidth=0.5)
        # ax.scatter(sampled_df.index, sampled_df[col], label=col)

    ax.set_xlabel("Timestamps")
    ax.set_ylabel(", ".join(interesting_cols))  # Set y-label based on input columns
    ax.set_title("Interesting Columns Over Time")
    ax.legend(title="Legend")  # Add a legend with a title
    ax.grid(True)

    plt.tight_layout(pad=3.0)  # Optimize space in the layout

    if fig_path is not None:
        fig.savefig(
            fig_path, format="png", dpi=300
        )  # Save as high-resolution image if path is provided
    plt.show()
    return fig


def multi_plot_line(
    sampled_df: pd.DataFrame, columns_sets_per_plot: List[List[str]], fig_path=None
):
    fig, axes = plt.subplots(
        nrows=len(columns_sets_per_plot),
        ncols=1,
        figsize=(10, 6 * len(columns_sets_per_plot)),
    )
    if len(columns_sets_per_plot) == 1:
        axes = [
            axes
        ]  # Ensure axes is always a list for consistency in single subplot scenarios

    for ax, cols in zip(axes, columns_sets_per_plot):
        for col in cols:
            ax.plot(sampled_df.index, sampled_df[col], label=col)
        ax.set_xlabel("Timestamps")
        ax.set_ylabel(", ".join(cols))
        ax.set_title("Plot of " + ", ".join(cols))
        ax.legend()
        ax.grid(True)

    plt.tight_layout()

    if fig_path is not None:
        fig.savefig(
            fig_path, format="png", dpi=300
        )  # Save as high-resolution image if path is provided
    plt.show()


import contextlib
from rich.errors import NotRenderableError


def rich_display_dataframe(
    df: pd.DataFrame, title="Dataframe", lim_cols=10, lim_rows=20
) -> None:
    """Display dataframe as table using rich library.
    Args:
        df (pd.DataFrame): dataframe to display
        title (str, optional): title of the table. Defaults to "Dataframe".
    Raises:
        NotRenderableError: if dataframe cannot be rendered
    Returns:
        rich.table.Table: rich table
    """
    from rich import print
    from rich.table import Table

    # ensure dataframe contains only string values
    df = df.astype(str)
    table = Table(title=title)
    for c, col in enumerate(df.columns):
        if c > lim_cols:
            print(f"Skipping the rest of the columns after {lim_cols}")
            break
        table.add_column(col)
    for r, row in enumerate(df.values):
        if r > lim_rows:
            print(f"Skipping the rest of the rows after {lim_rows}")
            break
        with contextlib.suppress(NotRenderableError):
            print(f"Adding row: {row}")
            table.add_row(*row[:lim_rows])
    print(table)


def hvplot_df_by_col(df: pd.DataFrame, cols: List[str], xlabel="", ylabel=""):
    """
    Recursively plot data from a DataFrame using Holoviews for each specified column.

    This function takes a DataFrame and a list of column names, plotting each column
    using Holoviews. If multiple columns are specified, it overlays the plots of all
    columns. The function handles missing data by dropping NA values before plotting.

    Args:
        df (pd.DataFrame): The DataFrame containing the data to plot.
        cols (List[str]): A list of column names to be plotted. The function plots
                          the first column and then recursively calls itself to plot
                          the remaining columns, overlaying each subsequent plot.

    Returns:
        hvPlot object if columns are provided, otherwise None.

    Example:
        >>> hvplot_df_by_col(df, ['column1', 'column2'])
        This will overlay the plots of 'column1' and 'column2' after dropping NAs.
    """
    if len(cols) < 1 or len(df) == 0:
        return empty_plot

    name = cols.pop(0)
    while name not in df.columns and len(cols) > 1:
        print(f"[yellow bold]🚧WARNING: Could not find {name} in data... skipping.")
        name = cols.pop(0)

    if len(cols) > 0:
        return df[name].dropna().hvplot(
            alpha=0.7, grid=True, xlabel=xlabel, ylabel=ylabel
        ) * hvplot_df_by_col(df, cols, xlabel=xlabel, ylabel=ylabel)
    else:
        return (
            df[name].dropna().hvplot(alpha=0.7, grid=True, xlabel=xlabel, ylabel=ylabel)
        )


def power_plot(df: pd.DataFrame, voltage_col="Voltage", current_col="Current"):
    if len(df) == 0:
        return

    power = df[voltage_col] * df[current_col]

    # filter out nan where there were missing messages
    power = power[pd.notna(power)] / 1000

    # render plot:
    return power.hvplot.area(
        ylabel="Power (kW)",
        color="green",
        alpha=0.7,
        grid=True,
        line_color="darkgreen",
        line_alpha=0.6,
    )


def plot_temperatures(
    df: pd.DataFrame,
):
    temp_cols = [
        "TempCurrCool1",
        "TempCurr1",
        "ElectricMachineTemperature1",
        "InverterTemperature1",
        "TempCurrRotor1",
    ]

    print("Plotting temperatures: ", temp_cols)
    return hvplot_df_by_col(df=df, cols=temp_cols, ylabel="Temperature ( ºC )")
