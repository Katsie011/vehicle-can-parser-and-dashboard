"""
Program Flow Description for MF4 to CSV Converter:

1. Introduction to Key Concepts:
   - CAN Messages: In vehicle networks, CAN (Controller Area Network) messages are packets of data sent between electronic control units (ECUs). Each message contains identifiers and data bytes.
   - MF4 Files: These are binary files used to store data from CAN networks. MF4 stands for Measurement Data Format version 4, which is commonly used for recording data in automotive testing.
   - DBC Files: A DBC file (Database CAN) is a text file that defines the structure of CAN messages in the network, allowing for the interpretation of message content from raw data.

2. Importing MF4 Files:
   - The program starts by loading an MF4 file which contains raw CAN data collected during vehicle tests.

3. Reading CAN Messages:
   - Utilizing the `python-can` library, the program reads the CAN messages from the MF4 file. This library provides tools for working with CAN data in Python.

4. Filtering Messages:
   - Only the messages defined in the DBC file are relevant for our analysis. The program uses the DBC file as a reference to filter out all unrelated CAN messages from the MF4 file.

5. Converting to CSV:
   - After filtering, the relevant CAN messages are converted into a CSV format. Each row in the CSV represents a single CAN message with columns for time, identifier, and data bytes.

6. Output:
   - The final CSV file is saved to a specified location. This file now contains only the necessary information as structured data, making it easier for further analysis or reporting.

This structured approach ensures that only pertinent data is extracted, reducing processing time and improving clarity in the resulting dataset.
"""

from typing import Dict, Iterable, List
import can
from  asammdf import MDF, types
import cantools
import pandas as pd
import numpy as np
from rich import print, spinner
from rich.console import Console
import os
import visualisation as vis
import mf4_helpers

console = Console()


mf4_file = None
while mf4_file is None: 
   text = input("Input the path to the mf4 file you would like to parse:\n")
   if not os.path.splitext(text)[1].lower() == 'mf4':
      print("[red bold]The file path you have given is not an mf4")
      continue
   if not os.path.exists(text):
      print("[red bold]The path you have given does not exist")
      continue

   mf4_file = text

name_input = os.path.splitext(os.path.basename(mf4_file))[0]

config = mf4_helpers.get_config()
paths = config.get("paths", {})
if type(paths) is not Dict:
   print("[yellow]⚠️Paths not setup in the settings. Using defaults. Otherwise, add a [paths] section to include.")
   paths: Dict[str, str] = {}

export_dir = paths.get("export_dir", "./processed_files/")
os.makedirs(export_dir, exist_ok=True)

dbc_database_dir = paths.get("dbcs_dir", "./DBCs/")

print(f"[bold yellow]Importing all DBCs from:\n{os.path.abspath(dbc_database_dir)}")

# with spinner.Spinner(name="spnr_dbc", text="Loading DBCs", style='aesthetic') as spinner:
with console.status("Loading DBCs") as status:
   dbc_files: List[types.DbcFileType] = []
   import os
   for root, dirs, files in os.walk(dbc_database_dir):
      for file in files:
         if file.endswith(".dbc"):
               dbc_files.append((os.path.join(root, file),0))

   dbcs: Dict[types.BusType, Iterable[types.DbcFileType]] = {"CAN": dbc_files, "LIN": []}


with console.status("Loading MF4 File:") as status:
   mdf = MDF(mf4_file)
   df_raw_mdf = mf4_helpers.mdf_to_df(mdf, config=config)
   mf4_helpers.mdf_to_raw_bytes(df_mf4=df_raw_mdf, config=config).to_csv(os.path.join(export_dir, f"raw_bytes_{name_input}"))

with console.status("Filtering for messages from DBCs") as status:
   filtered_bus = mdf.extract_bus_logging(database_files=dbcs)
   df_mdf_filtered = mf4_helpers.mdf_to_df(filtered_bus, config=config)
   df_mdf_filtered.to_csv(os.path.join(export_dir, f"filtered_{name_input}"))


if input("Would you like to preview the data?").lower() == 'y':
   vis.rich_display_dataframe(df_mdf_filtered)

   if input("Are there any messages you would like to plot?").lower() == 'y':
      cols = input("Input the column names separated by commas. e.g. voltage, current, DC_MaxCurrentHV1").split(',')
      fig = vis.plot_lines(sampled_df=df_mdf_filtered, interesting_cols=cols)
      if input("Save figure?").lower() == 'y':
         path = input("Enter the path to save to:")
         fig.savefig(path,format='png', dpi=300)  )