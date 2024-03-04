"""
File: analysis.py
Author: Chuncheng Zhang
Date: 2024-03-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Analysis the signal loaded from load_data.py

Functions:
    1. Requirements and constants
    2. Function and class
    3. Play ground
    4. Pending
    5. Pending
"""

# %% ---- 2024-03-04 ------------------------
# Requirements and constants
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

import numpy as np
from scipy import fft
from scipy import signal

from pathlib import Path
from load_data import load_data, fs, ch_names


# %% ---- 2024-03-04 ------------------------
# Function and class
window_names = [
    e.strip()
    for e in """
boxcar

triang

blackman

hamming

hann

bartlett

flattop

parzen

bohman

blackmanharris

nuttall

barthann

cosine

exponential

tukey

taylor

lanczos
""".split(
        "\n"
    )
    if e.strip()
]


def compute_psd(window: str = "hann", **kwargs):
    data = load_data(Path("data/4hz/S0.mat"))
    print(kwargs)
    f, Pxx_den = signal.welch(data, fs, window, **kwargs)
    df = mk_df(Pxx_den, ch_names, f)
    return f, Pxx_den, df


def mk_df(Pxx_den, ch_names, f):
    array = []
    for i in range(Pxx_den.shape[0]):
        for j, ch in enumerate(ch_names):
            for k, freq in enumerate(f):
                array.append(
                    dict(epoch_idx=i, ch_name=ch, freq=freq, value=Pxx_den[i][j][k])
                )
    df = pd.DataFrame(array)
    return df


# %% ---- 2024-03-04 ------------------------
# Play ground
if __name__ == "__main__":
    data = load_data(Path("data/4hz/S0.mat"))

    # --------------------
    fig, ax = plt.subplots(1, 1, figsize=(6, 3))
    ax.plot(data[0][0])

    # --------------------
    f_1, Pxx_den_1 = signal.welch(data, fs, window="hamming")
    f_2, Pxx_den_2 = signal.welch(data, fs, window="hann")
    diff = np.abs(Pxx_den_1 - Pxx_den_2)
    f = f_1

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    for j in range(diff.shape[0]):
        ax.semilogy(f, diff[j][0], label=f"Epochs {j}")
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("PSD [V**2/Hz]")
    ax.set_title(f"Difference between hamming and hann window")

    # --------------------
    f, Pxx_den = signal.welch(data, fs, window="hamming")
    print(Pxx_den.shape)

    fig, ax = plt.subplots(1, 1, figsize=(6, 4))
    for j in range(Pxx_den.shape[0]):
        ax.semilogy(f, Pxx_den[j][0], label=f"Epochs {j}")
        ax.set_xlabel("frequency [Hz]")
        ax.set_ylabel("PSD [V**2/Hz]")

    plt.show()

# %%

# %% ---- 2024-03-04 ------------------------
# Pending


# %% ---- 2024-03-04 ------------------------
# Pending
