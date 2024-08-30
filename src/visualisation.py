from typing import List
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns



sns.set_theme(style='whitegrid')

def plot_lines(sampled_df: pd.DataFrame, interesting_cols: List[str], fig_path=None):
    # Plotting the interesting columns with improved performance and cleaner rendering for high density of points
    fig, ax = plt.subplots(figsize=(10, 6))
    for col in interesting_cols:
        ax.plot(sampled_df.index, sampled_df[col], "-", label=col, linewidth=0.5)

    ax.set_xlabel('Timestamps')
    ax.set_ylabel(', '.join(interesting_cols))  # Set y-label based on input columns
    ax.set_title('Interesting Columns Over Time')
    ax.legend(title="Legend")  # Add a legend with a title
    ax.grid(True)
    
    plt.tight_layout()  # Optimize space in the layout

    if fig_path is not None:
        fig.savefig(fig_path, format='png', dpi=300)  # Save as high-resolution image if path is provided
    plt.show()
    return fig


def multi_plot_line(sampled_df: pd.DataFrame, columns_sets_per_plot: List[List[str]], fig_path=None):
    fig, axes = plt.subplots(nrows=len(columns_sets_per_plot), ncols=1, figsize=(10, 6 * len(columns_sets_per_plot)))
    if len(columns_sets_per_plot) == 1:
        axes = [axes]  # Ensure axes is always a list for consistency in single subplot scenarios

    for ax, cols in zip(axes, columns_sets_per_plot):
        for col in cols:
            ax.plot(sampled_df.index, sampled_df[col], label=col)
        ax.set_xlabel('Timestamps')
        ax.set_ylabel(', '.join(cols))
        ax.set_title('Plot of ' + ', '.join(cols))
        ax.legend()
        ax.grid(True)

    plt.tight_layout()

    if fig_path is not None:
        fig.savefig(fig_path, format='png', dpi=300)  # Save as high-resolution image if path is provided
    plt.show()


import contextlib
from rich.errors import NotRenderableError
def rich_display_dataframe(df, title="Dataframe", lim_cols = 20, lim_rows = 50) -> None:
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
        if c>lim_cols: break
        table.add_column(col)
    for r, row in enumerate(df.values):
        if r>lim_rows:
            break
        with contextlib.suppress(NotRenderableError):
            table.add_row(*row)
    print(table)