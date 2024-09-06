import io
from typing import List
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import visualisation as vis
import utils


pn.extension()
# pn.extension(theme="dark")


# # Assuming df_mdf_filtered is the DataFrame you want to display and interact with
def create_app(df: pd.DataFrame):
    cols = list(df_mdf_filtered.columns)

    # Create a checkbox group for selecting columns to plot
    column_selector = pn.widgets.CheckBoxGroup(
        value=["Voltage", "Current"],  # Default selected values
        options=cols,
        # inline=True,
    )

    # Function to update the plot based on selected columns
    @pn.depends(column_selector.param.value)
    def update_plot(selected_columns: List[str]):
        if not selected_columns:
            return "Please select at least one column to plot."
        return vis.hvplot_df_by_col(df=df, cols=selected_columns)

    # Layout the components
    app_layout = pn.Row(
        pn.Column(
            "## Temperatures",
            vis.plot_temperatures(df=df),
            "---",
            "## Data Visualiser",
            pn.panel(update_plot),
            "---",
            "### Select columns to plot:",
            pn.panel(column_selector, max_height=100),
        ),
        pn.Column(
            "## Power Consumption",
            pn.panel(
                vis.power_plot(df=df, voltage_col="Voltage", current_col="Current")
            ),
        ),
    )

    return app_layout


print("Re-loading the mf4 file")


# File selector GUI added for user to select or upload a file.
file_input = pn.widgets.FileInput(accept=".csv", name="Upload CSV File")


@pn.depends(file_input.param.value, watch=True)
def load_data():
    if file_input.value is not None:

        df = pd.read_csv(io.BytesIO(file_input.value))
        df.set_index("timestamps", inplace=True)
        return df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no file is selected


df_mdf_filtered = load_data()


indicators = utils.get_indicators(df=df_mdf_filtered)


sidebar = [
    "# IREX Dashboard\n---",
    pn.Spacer(sizing_mode="stretch_both"),
    file_input,
    pn.Spacer(sizing_mode="stretch_both"),
    pn.panel(
        "https://static.wixstatic.com/media/7429ff_c332d4103e494ce0b1149da82afde237~mv2.png/v1/fill/w_248,h_72,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/Copy%20of%20NewLogo_rectangle_4QT.png"
    ),
]


######################
#   Rendering
######################
template = pn.template.FastListTemplate(
    title="4QT IREX Log Parser",
    sidebar=sidebar,
    accent="#4099da",
)

# TODO create pannels to plot each of: Motion, Temperature, Battery, Emissions.
app = create_app(df_mdf_filtered)

# TODO in sideline add summaries for: runtime, power used, power generaed, distance travelled

template.main.append(indicators)
template.main.append(app)
template.servable()


# col_options = list(df_mdf_filtered.columns)
# column_selector = pn.widgets.CrossSelector(name='Columns of Interest', value=col_options[:2], options = col_options)

# column_selector = pn.widgets.CheckBoxGroup(
#     name='Select Columns',
#     value=['timestamps', 'Voltage', 'Current'],  # Default selected values
#     options=list(df_mdf_filtered.columns),
#     inline=True
# )

# plot_opts = dict(
#     responsive=True, min_height=400,
#     # Align the curves' color with the template's color
#     color=pn.template.FastListTemplate.accent_base_color
# )
# @pn.depends(column_selector.param.value)
# def update_plot(selected_columns):
#     if not selected_columns:
#         return "Please select at least one column to plot."
#     df =  df_mdf_filtered[pd.notna(df_mdf_filtered[selected_columns])]
#     return df.hvplot()

# template = pn.template.FastListTemplate(
#     title="FastListTemplate",
# )


# app_layout = pn.Column(
#     "## Data Visualisation App",
#     "Select columns to plot:",
#     column_selector,
#     update_plot
# )

# template.main.append(
#     app_layout
# )

# template.servable();
