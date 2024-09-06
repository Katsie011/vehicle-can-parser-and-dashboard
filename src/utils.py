import pandas as pd
import panel as pn
import styling
from math import pi

VEHICLE_EFFICIENCY = 1
GEAR_RATIO = 2 * pi / 60 / (6 * 2.741 * 4.75) * 0.5 * 3.6
ELECTRICITY_COST_CHF_PER_KWh = 98 / 1000


def litres_diesel_to_co2_kg(litres: float):
    """
    From: https://connectedfleet.michelin.com/blog/calculate-co2-emissions/#:~:text=One%20litre%20of%20diesel%20creates,has%20emitted%20in%20a%20month.
        - One litre of diesel creates 2.54kg of CO2. So you can simply multiply the number of litres you’ve used by 2.54 to work out how many kilograms of CO2 your fleet has emitted in a month
    """
    return litres * 2.54


def kwh_to_l_diesel(kilowatt_hours: float):
    # 9,8 kWh/Liter
    return kilowatt_hours / 9.8


def kwh_to_co2_saved(kilowatt_hours):
    return litres_diesel_to_co2_kg(
        litres=kwh_to_l_diesel(kilowatt_hours=kilowatt_hours) * VEHICLE_EFFICIENCY
    )


def distance_from_speed(df: pd.DataFrame, speed_column: str, gear_ratio: int):
    """
    Calculate the distance travelled using speed data over time.

    Parameters:
    - timestamps (pd.Series): The timestamps in seconds since the start.
    - speed (pd.Series): The speed values at each timestamp, may contain NaNs.

    Returns:
    - float: Total distance travelled in the same units as speed (e.g., km if speed is in km/h).
    """
    # Ensure that speed is a pandas Series and drop NaN values

    speed = df[speed_column].copy().dropna().abs() * gear_ratio
    timestamps = speed.index

    # Calculate the time differences in hours between each timestamp
    time_diffs = timestamps.diff().fillna(0) / 3600  # Convert seconds to hours

    # Calculate the distance segments by multiplying speed with time differences
    distance_segments = speed * time_diffs

    # Sum up all distance segments to get the total distance travelled
    total_distance = distance_segments.sum()
    print("Total distance travelled is:", total_distance)
    return total_distance


def get_indicators(df: pd.DataFrame, debug: bool = False):
    total_power_kwh = -1
    total_distance = -1
    running_cost = -1
    time_string = "Empty data"

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

        if "Speed1" in df.columns:
            total_distance = distance_from_speed(
                df, speed_column="Speed1", gear_ratio=GEAR_RATIO
            )
        else:
            print("Speed1 not in columns, skipping card update")

    indicators = pn.FlexBox(
        pn.indicators.String(
            value=time_string,
            name="Total Runtime",
            styles=styling.CARD_STYLE,
            font_size="48pt",
        ),
        pn.indicators.Number(
            value=total_power_kwh,
            name="Power Consumed (kWh)",
            format="{value:,.3f}",
            styles=styling.CARD_STYLE,
            font_size="48pt",
        ),
        pn.indicators.Number(
            value=total_distance,
            name="Distance Travelled (km)",
            format="{value:,.2f}",
            styles=styling.CARD_STYLE,
            font_size="48pt",
        ),
        pn.indicators.Number(
            value=kwh_to_co2_saved(total_power_kwh),
            name="CO2 Emmisions Saved (kg)",
            format="{value:,.2f}",
            styles=styling.CARD_STYLE,
            font_size="48pt",
        ),
        pn.indicators.Number(
            value=total_power_kwh * ELECTRICITY_COST_CHF_PER_KWh,
            name="Electricity Cost (chf)",
            format="{value:,.2f}",
            styles=styling.CARD_STYLE,
            font_size="48pt",
        ),
        margin=(20, 5),
    )
    return indicators
