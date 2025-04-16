import sys
import os
import math
from pydub import AudioSegment, silence

def prepare_audio_for_createml(
    input_path,
    output_dir="output",
    window_duration=0.975,
    silence_thresh=-50,
    min_silence_len=300,
    padding=100
):
    # Ensure the output directory exists, create it if it doesn't
    os.makedirs(output_dir, exist_ok=True)

    # Extract the file extension and convert it to lowercase for consistency
    ext = os.path.splitext(input_path)[-1].lower()
    
    # Load the audio file based on its format. Raise an error if the format is unsupported.
    try:
        if ext == ".mp3":
            audio = AudioSegment.from_mp3(input_path)
        elif ext == ".m4a":
            audio = AudioSegment.from_file(input_path, format="m4a")
        elif ext == ".flac":
            audio = AudioSegment.from_file(input_path, format="flac")
        elif ext == ".ogg":
            audio = AudioSegment.from_ogg(input_path)
        elif ext == ".wav":
            audio = AudioSegment.from_wav(input_path)
        else:
            raise ValueError(f"❌ Format {ext} is not supported.")
    except Exception as e:
        # Print an error message and exit if the file cannot be loaded
        print(f"Error loading the file: {e}")
        sys.exit(1)

    # Trim silence from the audio file based on the specified silence threshold and padding
    trimmed = audio.strip_silence(
        silence_thresh=silence_thresh,
        padding=padding
    )

    # Calculate the duration of each segment in milliseconds
    window_ms = int(window_duration * 1000)
    # Get the total duration of the trimmed audio in milliseconds
    total_ms = len(trimmed)
    # Calculate the total number of segments that can be created
    total_segments = math.floor(total_ms / window_ms)

    # Extract the base filename (without extension) for naming the output files
    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    for i in range(total_segments):
        # Calculate the start and end times for each segment
        start = i * window_ms
        end = start + window_ms
        # Extract the segment from the trimmed audio
        segment = trimmed[start:end]
        # Define the output path for the segment
        segment_path = os.path.join(output_dir, f"{base_filename}_{i+1:03d}.wav")
        # Export the segment as a WAV file
        segment.export(segment_path, format="wav")

    # Print a success message with the number of files created and the output directory
    print(f"✅ {total_segments} WAV files saved in '{output_dir}'.")

# Command-line interface (CLI) entry point
if __name__ == "__main__":
    # Check if the user provided an input file as an argument
    if len(sys.argv) < 2:
        # Print an error message and usage instructions if no file is provided
        print("❌ Please provide the path to the audio file:\n   python main.py input.mp3")
        sys.exit(1)

    # Get the input file path from the command-line arguments
    input_file = sys.argv[1]
    # Call the function to process the audio file
    prepare_audio_for_createml(input_file)

