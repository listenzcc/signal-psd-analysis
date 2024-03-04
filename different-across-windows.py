"""
File: different-across-windows.py
Author: Chuncheng Zhang
Date: 2024-03-04
Copyright & Email: chuncheng.zhang@ia.ac.cn

Purpose:
    Tell the different across different window types, like hann, hamming ...

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
from scipy import fft
from scipy import signal
import matplotlib.pyplot as plt


# %% ---- 2024-03-04 ------------------------
# Function and class
def get_window_names():
    names = [
        e for e in dir(signal.windows) if not e.startswith("_") and "windows" not in e
    ]
    return names


def get_window_shape(name: str, Nx: int = 51) -> np.ndarray:
    return signal.windows.get_window(name, Nx)


def compute_fft(x: np.ndarray) -> dict:
    n = x.shape[-1]
    A = fft.fft(x, 2048) / n
    freq = np.linspace(-0.5, 0.5, A.shape[-1])
    response = np.abs(fft.fftshift(A / np.max(np.abs(A))))
    # response = 20 * np.log10(np.maximum(response, 1e-10))
    return dict(response=response, freq=freq)


# %% ---- 2024-03-04 ------------------------
# Play ground
names = get_window_names()

fig, axs = plt.subplots(2, 1, figsize=(8, 6))

plt.style.use("seaborn")

for name in names:
    try:
        window = get_window_shape(name)
        dct = compute_fft(window)
    except ValueError:
        pass

    axs[0].plot(window, alpha=0.6, label=name)
    axs[1].semilogy(dct["freq"], dct["response"], alpha=0.6, label=name)

axs[1].set_ylim([1e-8, 1])
axs[0].set_title("Frequency responses of the windows")
axs[0].set_ylabel("Amplitude")
axs[1].set_ylabel("Normalized magnitude [dB]")
axs[1].set_xlabel("Normalized frequency [cycles per sample]")

plt.tight_layout()
plt.show()


# %% ---- 2024-03-04 ------------------------
# Pending


# %% ---- 2024-03-04 ------------------------
# Pending
