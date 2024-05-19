import os
from pydub import AudioSegment, silence

# Folder path
import sys
folder_path = sys.argv[1]
# Delete existing output file if it exists
output_file_path = os.path.join(folder_path, "output.mp3")
if os.path.exists(output_file_path):
    os.remove(output_file_path)
    print("Deleted existing output.mp3 file.")

# Parameters
silence_thresh = -50  # silence threshold in dB
min_silence_len = 1000  # minimum length of silence to consider in milliseconds

# Initialize an empty audio segment for the final output
final_processed_audio = AudioSegment.silent(duration=0)

# Iterate through all .mp3 files in the folder
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".mp3"):
        file_path = os.path.join(folder_path, filename)
        print(f"Processing file: {filename}")

        # Load the audio file
        audio = AudioSegment.from_mp3(file_path)

        # Find nonsilent chunks
        nonsilent_chunks = silence.detect_nonsilent(
            audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
        print(f"Detected nonsilent chunks in {filename}")

        # Create a new audio segment from nonsilent chunks
        processed_audio = AudioSegment.silent(duration=0)  # Initialize an empty audio segment
        print(f"Initialized an empty audio segment for {filename}")
        for start, end in nonsilent_chunks:
            processed_audio += audio[start:end]
            processed_audio += AudioSegment.silent(duration=1000)  # Add 1 second of silence between chunks

        # Store processed_audio in a subfolder called 'processed'
        processed_folder_path = os.path.join(folder_path, "processed")
        os.makedirs(processed_folder_path, exist_ok=True)
        processed_file_path = os.path.join(processed_folder_path, filename)
        processed_audio.export(processed_file_path, format="mp3")
        print(f"Stored {filename} in processed folder.")
        # Append processed audio to the final output
        final_processed_audio += processed_audio
        print(f"Added processed chunks from {filename} to final output.")

# Export the final processed audio to a single file
final_processed_audio.export(output_file_path, format="mp3")
print(f"Exported the final processed audio to {output_file_path}.")
