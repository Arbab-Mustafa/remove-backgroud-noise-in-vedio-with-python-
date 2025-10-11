# Changelog

## Fixed Issues

### Code Issues Fixed:

1. **Import Error**: Fixed `from moviepy.editor import VideoFileClip` to `from moviepy import VideoFileClip`
2. **Verbose Parameter Error**: Removed unsupported `verbose=False` parameter from `write_audiofile()`
3. **Error Handling**: Added comprehensive try-catch blocks with specific error messages
4. **Dependency Validation**: Added FFmpeg availability check before processing
5. **Audio Format Handling**: Improved audio data type conversion (int16, int32, float32)
6. **Temporary Files**: Used `tempfile.TemporaryDirectory()` for safer file cleanup
7. **Output Naming**: Changed output naming to `denoised_[original_name]` for clarity
8. **FFmpeg Parameters**: Improved FFmpeg command with better audio codec settings and error suppression
9. **Memory Management**: Added explicit memory cleanup for video objects

### Dependency Issues Fixed:

1. **Package Installation**: Properly installed all required packages in virtual environment
2. **Version Compatibility**: Updated to compatible package versions:
   - moviepy==2.2.1
   - noisereduce==3.0.3
   - scipy==1.16.2
   - numpy>=1.25.0
3. **Requirements File**: Created comprehensive requirements.txt
4. **Virtual Environment**: Ensured proper virtual environment usage

### Improvements Made:

1. **Better Audio Processing**:
   - Improved sample rate (22050 Hz)
   - Better noise reduction parameters
   - Proper audio format conversion
2. **Robust Error Messages**: Specific error handling for different failure scenarios
3. **Cross-platform Support**: Added both .bat and .ps1 scripts for Windows
4. **Documentation**: Created comprehensive README.md with usage instructions

### Files Created/Modified:

- `denoise_video.py` - Main script (improved)
- `requirements.txt` - Package dependencies
- `run_denoise.bat` - Windows batch script
- `run_denoise.ps1` - PowerShell script
- `README.md` - Documentation
- `CHANGELOG.md` - This file

## Usage

The script now works properly with the virtual environment. Use:

```bash
.\venv\Scripts\python.exe denoise_video.py input_video.mp4
```

Or use the provided batch/PowerShell scripts for easier execution.
