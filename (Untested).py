import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def normalize_data(df):
    """Normalize the data between -1 and 1."""
    return (df - df.min()) / (df.max() - df.min()) * 2 - 1

def load_and_pair_files(L_path, H_path):
    """
    Load and pair L and H files based on their segment identifiers.
    """
    L_files = sorted(glob.glob(os.path.join(L_path, "*.csv")))
    H_files = sorted(glob.glob(os.path.join(H_path, "*.csv")))

    # Ensure L and H files are matched by shared prefix
    paired_files = []
    for l_file in L_files:
        base_name = os.path.basename(l_file).replace("L", "")  # Remove 'L' from name
        matching_h_file = [h for h in H_files if base_name in os.path.basename(h)]
        if matching_h_file:
            paired_files.append((l_file, matching_h_file[0]))

    return paired_files

def combine_and_normalize_segments(L_file, H_file):
    """
    Load and combine 'L' and 'H' parts of a segment, normalize the data.
    """
    # Read the 'L' and 'H' parts
    df_L = pd.read_csv(L_file, header=None)
    df_H = pd.read_csv(H_file, header=None)
    
    # Normalize the signal data
    df_L = normalize_data(df_L)
    df_H = normalize_data(df_H)
    
    # Concatenate both parts of the segment into one DataFrame
    combined_df = pd.concat([df_L, df_H], axis=0, ignore_index=True)
    
    return combined_df

def create_spectrogram(data, output_file):
    """
    Generate and save a spectrogram from the given data.
    """
    plt.figure(figsize=(10, 4))
    plt.specgram(data.values.flatten(), Fs=1, cmap='viridis')  # Use colormap 'viridis' for better contrast
    plt.colorbar(label="Intensity (dB)")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.title("Spectrogram")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def process_files(L_path, H_path, output_dir):
    """
    Process paired L and H files to generate combined spectrograms.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load and pair L and H files
    paired_files = load_and_pair_files(L_path, H_path)

    # Process each pair
    for i, (l_file, h_file) in enumerate(paired_files):
        print(f"Processing pair: {os.path.basename(l_file)} and {os.path.basename(h_file)}")
        
        # Combine and normalize the segments
        combined_data = combine_and_normalize_segments(l_file, h_file)
        
        # Generate a spectrogram
        output_file = os.path.join(output_dir, f"segment_{i + 1}.png")
        create_spectrogram(combined_data, output_file)
        print(f"Spectrogram saved to: {output_file}")

# Define paths
L_path = 'C:\\Users\\Arnav\\Downloads\\f4c2b4n755-1 (1)\\DroneRF\\AR drone\\haha\\RF Data_10111_L'  # Path to L folder
H_path = 'C:\\Users\\Arnav\\Downloads\\f4c2b4n755-1 (1)\\DroneRF\\AR drone\\haha\\RF Data_10111_H'  # Path to H folder

output_dir = "C:\\Users\\Arnav\\Downloads\\f4c2b4n755-1 (1)\\DroneRF\\AR drone\\haha"

# Run the processing
process_files(L_path, H_path, output_dir)
