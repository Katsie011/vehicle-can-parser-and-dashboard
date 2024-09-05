from typing import List
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import visualisation as vis

pn.extension()
# pn.extension(theme="dark")

# STYLING
BRAND_COLOR = "teal"
BRAND_TEXT_ON_COLOR = "white"

CARD_STYLE = {
    "box-shadow": "rgba(50, 50, 93, 0.25) 0px 6px 12px -2px, rgba(0, 0, 0, 0.3) 0px 3px 7px -3px",
    "padding": "10px",
    "border-radius": "5px",
}


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

# TODO add a file selector GUI.
df_mdf_filtered = pd.read_csv(
    "processed_files/filtered_61494E67_00000039_00000001-0B1D281D351973497D3A29B6168B8C9C2A6143BC0B521D2EE92BB91BB844ECC4.csv",
)

df_mdf_filtered.set_index("timestamps", inplace=True)

print("Getting runtime for log:")
print(f"DEBUG: runtime = {df_mdf_filtered.index[-1]} - {df_mdf_filtered.index[0]}")
runtime = df_mdf_filtered.index[-1] - df_mdf_filtered.index[0]
hours, remainder = divmod(runtime, 3600)
minutes, seconds = divmod(remainder, 60)
time_string = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


print(f"DEBUG: total_power = ")
total_power = df_mdf_filtered["Voltage"] * df_mdf_filtered["Current"]
total_power = total_power[pd.notna(total_power)].sum()
total_power_kwh = total_power / 1000 / 60 / 60


indicators = pn.FlexBox(
    pn.indicators.String(
        value=time_string,
        name="Total Runtime",
        # format="{value:,s}",
        styles=CARD_STYLE,
    ),
    pn.indicators.Number(
        value=total_power_kwh,
        name="Power Consumed (kWh)",
        format="{value:,.3f}",
        styles=CARD_STYLE,
    ),
    pn.indicators.Number(
        value=4.20,
        name="Distance Travelled (km)",
        format="{value:,.2f}",
        styles=CARD_STYLE,
    ),
    pn.indicators.Number(
        value=6.9,
        name="CO2 Emmisions Saved (kg)",
        format="{value:,.2f}",
        styles=CARD_STYLE,
    ),
    pn.indicators.Number(
        value=9.999,
        name="Electricity Cost (chf)",
        format="{value:,.2f}",
        styles=CARD_STYLE,
    ),
    margin=(20, 5),
)


sidebar = [
    "# IREX Dashboard\n---",
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
