import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np

pn.extension("echarts")


def remove_empty_vals(df, selected_columns):
    """Filters each of the selected columns, returning a List of Series, each without any empty values."""

    pass


# # Assuming df_mdf_filtered is the DataFrame you want to display and interact with
def create_app(df):
    cols = list(df_mdf_filtered.columns)

    # Create a checkbox group for selecting columns to plot
    column_selector = pn.widgets.CheckBoxGroup(
        name="Select Columns",
        value=["Voltage", "Current"],  # Default selected values
        options=cols,
        # inline=True,
    )

    # Function to update the plot based on selected columns
    @pn.depends(column_selector.param.value)
    def update_plot(selected_columns):
        if not selected_columns:
            return "Please select at least one column to plot."
        vals = df_mdf_filtered[selected_columns]
        vals = vals[np.all(pd.notna(vals), axis=1)]
        print(vals)
        return vals.hvplot()

    gauge = {
        "tooltip": {"formatter": "{a} <br/>{b} : {c}%"},
        "series": [
            {
                "name": "Gauge",
                "type": "gauge",
                "detail": {"formatter": "{value}%"},
                "data": [{"value": 50, "name": "Value"}],
            }
        ],
    }
    gauge_pane = pn.pane.ECharts(gauge, width=400, height=400)

    slider = pn.widgets.IntSlider(value=50, start=0, end=100)

    slider.jscallback(
        args={"gauge": gauge_pane},
        value="""
    gauge.data.series[0].data[0].value = cb_obj.value
    gauge.properties.data.change.emit()
    """,
    )

    # Layout the components
    app_layout = pn.Row(
        pn.Column(slider, gauge_pane),
        pn.Column(
            "## Data Visualisation App",
            update_plot,
            "---",
            "Select columns to plot:",
            column_selector,
        ),
    )

    return app_layout


print("Re-loading the mf4 file")
df_mdf_filtered = pd.read_csv(
    "/Users/michaelkatsoulis/Documents/4QT/CAN Parser/processed_files/filtered_61494E67_00000039_00000001-0B1D281D351973497D3A29B6168B8C9C2A6143BC0B521D2EE92BB91BB844ECC4.csv",
)
df_mdf_filtered.set_index("timestamps", inplace=True)

print("Getting runtime for log:")
print(f"DEBUG: runtime = {df_mdf_filtered.index[-1]} - {df_mdf_filtered.index[0]}")
runtime = df_mdf_filtered.index[-1] - df_mdf_filtered.index[0]
hours, remainder = divmod(runtime, 3600)
minutes, seconds = divmod(remainder, 60)
time_string = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


template = pn.template.FastListTemplate(
    title="4QT IREX Log Parser",
    sidebar=[
        f"## Runtime for Log: {time_string}\n---",
    ],
)

app = create_app(df_mdf_filtered)
template.main.append(app)


# template.main.append(
#     pn.Row(
#         slider,
#         gauge_pane,
#     )
# )


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
