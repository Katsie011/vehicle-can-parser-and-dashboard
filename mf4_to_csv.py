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


db = cantools.db.load_file('DBCs/Standard_Electrical_Drive_OHW_v1.7_HYB(1) (1).dbc')


dbc_database_dir = "DBCs"
mf4_file = input("Input the path to the mf4 file you would like to parse:\n")
dbc_files: List[types.DbcFileType] = []
import os
for root, dirs, files in os.walk(dbc_database_dir):
    for file in files:
        if file.endswith(".dbc"):
            dbc_files.append((os.path.join(root, file),0))


mdf = MDF(mf4_file)
dbcs: Dict[types.BusType, Iterable[types.DbcFileType]] = {"CAN": dbc_files, "LIN": []}

filtered_bus = mdf.extract_bus_logging(database_files=dbcs)
