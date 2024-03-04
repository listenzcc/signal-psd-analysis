"""
File: load_data.py
Author: Chuncheng Zhang
Date: 2024-03-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Load the ./data/*/*.mat files 

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""

# %% ---- 2024-03-04 ------------------------
# Requirements and constants
import numpy as np
import scipy.io as scio

from loguru import logger
from pathlib import Path
from rich import print, inspect

# %%
fs = 200  # Hz
ch_names = [
    "FP1",
    "FPZ",
    "FP2",
    "AF3",
    "AF4",
    "F7",
    "F5",
    "F3",
    "F1",
    "FZ",
    "F2",
    "F4",
    "F6",
    "F8",
    "FT7",
    "FC5",
    "FC3",
    "FC1",
    "FCZ",
    "FC2",
    "FC4",
    "FC6",
    "FT8",
    "T7",
    "C5",
    "C3",
    "C1",
    "CZ",
    "C2",
    "C4",
    "C6",
    "T8",
    "TP7",
    "CP5",
    "CP3",
    "CP1",
    "CPZ",
    "CP2",
    "CP4",
    "CP6",
    "TP8",
    "P7",
    "P5",
    "P3",
    "P1",
    "PZ",
    "P2",
    "P4",
    "P6",
    "P8",
    "PO7",
    "PO5",
    "PO3",
    "POZ",
    "PO4",
    "PO6",
    "PO8",
    "O1",
    "OZ",
    "O2",
]
n_points = 1601


# %% ---- 2024-03-04 ------------------------
# Function and class
def load_data(path: Path) -> np.ndarray:
    """
    Data size is 28 x 60 x 1601
    - 28: 28 Cut windows;
    - 60: 60 EEG sensors;
    - 1601: 1601 time points, 8 seconds at 200 Hz sampling.
    """
    raw = scio.loadmat(path)
    data = raw["windows_data"]
    logger.info(f"Got data {path}: {data.shape} | {type(data)}")
    return data


# %% ---- 2024-03-04 ------------------------
# Play ground
if __name__ == "__main__":
    data = load_data(Path("./data/4hz/S0.mat"))
    data = load_data(Path("./data/10hz/S0.mat"))


# %% ---- 2024-03-04 ------------------------
# Pending


# %% ---- 2024-03-04 ------------------------
# Pending
