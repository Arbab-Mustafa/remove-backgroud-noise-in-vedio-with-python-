# Video Noise Reduction Tool

This tool removes background noise from video files by processing the audio track.

## Features

- Extracts audio from video files
- Applies advanced noise reduction algorithms
- Merges cleaned audio back to video
- Supports various video formats
- Uses temporary files for safe processing
- Robust error handling and validation

## Requirements

- Python 3.11+
- FFmpeg (must be installed and in PATH)
- Virtual environment (recommended)

## Installation

1. Clone or download this project
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line

```bash
# Activate virtual environment first
venv\Scripts\activate

# Run the script
python denoise_video.py input_video.mp4
```

### Using Batch Files (Windows)

```bash
# For Command Prompt
run_denoise.bat input_video.mp4

# For PowerShell
.\run_denoise.ps1 input_video.mp4
```

## Output

The processed video will be saved as `denoised_[original_filename]` in the same directory as the input file.

## Troubleshooting

1. **FFmpeg not found**: Install FFmpeg from https://ffmpeg.org/download.html
2. **Import errors**: Make sure you're using the virtual environment
3. **Audio issues**: Ensure the input video has an audio track
4. **Permission errors**: Check file permissions and available disk space

## Dependencies

- moviepy: Video processing
- noisereduce: Audio noise reduction
- scipy: Scientific computing
- numpy: Numerical operations
- matplotlib: Plotting (dependency of noisereduce)
