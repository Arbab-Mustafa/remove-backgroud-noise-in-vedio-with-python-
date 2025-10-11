import argparse
import os
import sys
import tempfile
import shutil
from pathlib import Path

try:
    from moviepy import VideoFileClip
    from scipy.io import wavfile
    import noisereduce as nr
    import numpy as np
    import subprocess
except ImportError as e:
    print(f"Missing required package: {e}")
    print("Please install required packages with: pip install moviepy noisereduce scipy numpy")
    sys.exit(1)

def validate_dependencies():
    """Check if all required dependencies are available."""
    # Check FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode != 0:
            raise FileNotFoundError("FFmpeg not found")
    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not in PATH.")
        print("Please install FFmpeg from https://ffmpeg.org/download.html")
        return False
    return True

def main(input_video):
    try:
        # Validate dependencies
        if not validate_dependencies():
            return
            
        # Validate input file
        input_path = Path(input_video)
        if not input_path.exists():
            raise FileNotFoundError(f"Video file {input_video} not found.")
        
        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            audio_path = temp_path / 'audio.wav'
            denoised_audio = temp_path / 'denoised_audio.wav'
            
            # Step 1: Extract audio from video
            print("Extracting audio...")
            try:
                videoclip = VideoFileClip(str(input_path))
                if videoclip.audio is None:
                    raise ValueError("Video file has no audio track")
                    
                # Extract audio with better parameters
                videoclip.audio.write_audiofile(
                    str(audio_path), 
                    fps=22050,  # Better sample rate for noise reduction
                    nbytes=2, 
                    logger=None
                )
                videoclip.close()
                del videoclip  # Explicitly delete to free memory
            except Exception as e:
                raise RuntimeError(f"Failed to extract audio: {e}")
            
            # Step 2: Remove noise from audio
            print("Reducing noise...")
            try:
                rate, data = wavfile.read(str(audio_path))
                
                # Handle different audio formats
                if data.dtype != np.float32:
                    if data.dtype == np.int16:
                        data = data.astype(np.float32) / 32768.0
                    elif data.dtype == np.int32:
                        data = data.astype(np.float32) / 2147483648.0
                    else:
                        data = data.astype(np.float32)
                
                # Convert to mono if stereo
                if len(data.shape) > 1:
                    data = np.mean(data, axis=1)
                
                # Apply noise reduction with better parameters
                reduced_noise = nr.reduce_noise(
                    y=data, 
                    sr=rate, 
                    stationary=False,  # Better for varying noise
                    prop_decrease=0.8  # Reduce noise by 80%
                )
                
                # Convert back to int16 for compatibility
                if reduced_noise.dtype == np.float32:
                    reduced_noise = (reduced_noise * 32767).astype(np.int16)
                
                wavfile.write(str(denoised_audio), rate, reduced_noise)
            except Exception as e:
                raise RuntimeError(f"Failed to reduce noise: {e}")
            
            # Step 3: Merge cleaned audio back into video
            print("Merging cleaned audio...")
            output_video = input_path.parent / f"denoised_{input_path.name}"
            
            # Use more robust FFmpeg command with error suppression
            ffmpeg_cmd = [
                'ffmpeg', '-y',  # Overwrite output file
                '-loglevel', 'error',  # Only show errors
                '-i', str(input_path),  # Input video
                '-i', str(denoised_audio),  # Input audio
                '-map', '0:v:0',  # Map video from first input
                '-map', '1:a:0',  # Map audio from second input
                '-c:v', 'copy',  # Copy video codec
                '-c:a', 'aac',   # Use AAC audio codec
                '-b:a', '128k',  # Audio bitrate
                '-shortest',     # Match shortest stream
                str(output_video)
            ]
            
            result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"FFmpeg failed: {result.stderr}")
        
        print(f"Success! Processed video saved as: {output_video}")
        
    except Exception as e:
        print(f"Error: {e}")
        if "FFmpeg" in str(e):
            print("Make sure FFmpeg is properly installed and accessible.")
        elif "moviepy" in str(e).lower():
            print("Try reinstalling moviepy: pip install --upgrade moviepy")
        else:
            print("Check that the input video file is valid and accessible.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove background noise from a video's audio.")
    parser.add_argument("video_path", help="Path to the input video file (e.g., video.mp4)")
    args = parser.parse_args()
    main(args.video_path)