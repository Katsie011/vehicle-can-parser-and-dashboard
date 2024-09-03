from typing import Dict
import pandas as pd
import toml
from asammdf import MDF
from rich import print


def get_config(config_path="./settings.toml"):
    with open(config_path, "r") as f:
        config = toml.load(f)
    print("[green]✅ Loaded settings.")
    return config


def mdf_to_df(mf4: MDF, config: Dict[str, str]):
    export_settings = config.get("export_settings", {})
    if type(export_settings) is not Dict:
        print("[red]Config file has bad export settings. Using defaults instead.")
        export_settings = {}
    basenames = bool(export_settings.get("only_basenames", False))
    interpolate = bool(export_settings.get("use_interpolation", False))
    date = bool(export_settings.get("time_as_date", False))

    df = mf4.to_dataframe(
        time_as_date=date, only_basenames=basenames, use_interpolation=interpolate
    )
    start_time = mf4.start_time
    df["time"] = start_time + pd.to_timedelta(df.index, unit='ms')
    return df


def mdf_to_raw_bytes(df_mf4: pd.DataFrame, config: Dict[str, str]):
    # Displaying the data as bytes
    df_display = df_mf4.copy()
    df_display["CAN_DataFrame.CAN_DataFrame.DataBytes"] = df_display[
        "CAN_DataFrame.CAN_DataFrame.DataBytes"
    ].apply(lambda x: " ".join(f"0x{b:02X}" for b in x))
    return df_display
