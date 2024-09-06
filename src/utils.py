import pandas as pd
import panel as pn
import styling


def get_indicators(df: pd.DataFrame, debug: bool = False):
    if len(df.index):

        if debug:
            print("Getting runtime for log:")
        if debug:
            print(f"DEBUG: runtime = {df.index[-1]} - {df.index[0]}")
        runtime = df.index[-1] - df.index[0]
        hours, remainder = divmod(runtime, 3600)
        minutes, seconds = divmod(remainder, 60)
        time_string = f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

        if debug:
            print(f"DEBUG: total_power = ")

        if "Voltage" in df.columns and "Current" in df.columns:
            total_power = df["Voltage"] * df["Current"]
            total_power = total_power[pd.notna(total_power)].sum()
            total_power_kwh = total_power / 1000 / 60 / 60
        else:
            total_power_kwh = -1
    else:
        total_power_kwh = -1
        time_string = "Empty data"
    indicators = pn.FlexBox(
        pn.indicators.String(
            value=time_string,
            name="Total Runtime",
            # format="{value:,s}",
            styles=styling.CARD_STYLE,
        ),
        pn.indicators.Number(
            value=total_power_kwh,
            name="Power Consumed (kWh)",
            format="{value:,.3f}",
            styles=styling.CARD_STYLE,
        ),
        pn.indicators.Number(
            value=4.20,
            name="Distance Travelled (km)",
            format="{value:,.2f}",
            styles=styling.CARD_STYLE,
        ),
        pn.indicators.Number(
            value=6.9,
            name="CO2 Emmisions Saved (kg)",
            format="{value:,.2f}",
            styles=styling.CARD_STYLE,
        ),
        pn.indicators.Number(
            value=9.999,
            name="Electricity Cost (chf)",
            format="{value:,.2f}",
            styles=styling.CARD_STYLE,
        ),
        margin=(20, 5),
    )
