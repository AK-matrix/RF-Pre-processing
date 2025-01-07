import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import glob
import time


def load_and_combine_files(L_path, H_path):
    """
    Load all CSV files from L and H folders and combine them into lists of file paths.
    """
    L_files = glob.glob(L_path + "/*.csv")
    H_files = glob.glob(H_path + "/*.csv")
    return L_files, H_files


def normalize_signal(signal):
    """
    Normalize a 1D signal to the range [-1, 1].
    """
    return (signal - np.min(signal)) / (np.max(signal) - np.min(signal)) * 2 - 1


def create_spectrogram(signal, output_image_path, fs=1000):
    """
    Create a spectrogram image from RF signal data and save it as a PNG image.
    """
    print(f"Creating spectrogram for signal of length {len(signal)}")
    
    # Generate the spectrogram
    f, t, Sxx = spectrogram(signal, fs=fs)
    Sxx_log = np.log(Sxx + 1e-10)  # Convert to log scale for better visualization

    # Plot and save the spectrogram
    plt.figure(figsize=(10, 6))
    plt.pcolormesh(t, f, Sxx_log, shading='auto', cmap='inferno')
    plt.colorbar(label='Log Power')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.title('Spectrogram')
    plt.savefig(output_image_path)
    plt.close()
    print(f"Spectrogram saved to {output_image_path}")


def process_segment(L_file, H_file, output_image_path):
    """
    Process an L-H file pair: load, normalize, combine, and generate a spectrogram.
    """
    print(f"Processing L file: {L_file}")
    print(f"Processing H file: {H_file}")

    # Load the CSV files (single row with many columns)
    L_signal = pd.read_csv(L_file, header=None).values.flatten()
    H_signal = pd.read_csv(H_file, header=None).values.flatten()
    
    # Normalize the signals
    L_signal = normalize_signal(L_signal)
    H_signal = normalize_signal(H_signal)
    
    # Combine the signals (concatenate)
    combined_signal = np.concatenate((L_signal, H_signal))
    print(f"Combined signal length: {len(combined_signal)}")
    
    # Create and save the spectrogram
    create_spectrogram(combined_signal, output_image_path)


# Example Usage

L_path = 'C:\\Users\\Arnav\\Downloads\\f4c2b4n755-1 (1)\\DroneRF\\AR drone\\haha\\RF Data_10111_L'  # Path to L folder
H_path = 'C:\\Users\\Arnav\\Downloads\\f4c2b4n755-1 (1)\\DroneRF\\AR drone\\haha\\RF Data_10111_H'  # Path to H folder

# Load file lists
L_files, H_files = load_and_combine_files(L_path, H_path)

# Process the first pair of files as an example
if len(L_files) > 0 and len(H_files) > 0:
    output_image_path = "C:\\Users\\Arnav\\Downloads\\spectrogram_output.png"  # Adjust the path
    process_segment(L_files[0], H_files[0], output_image_path)
else:
    print("No files found in the specified folders.")
