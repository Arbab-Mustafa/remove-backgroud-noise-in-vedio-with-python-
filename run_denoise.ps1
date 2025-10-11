#!/usr/bin/env pwsh
Set-Location $PSScriptRoot
& .\venv\Scripts\Activate.ps1
& python denoise_video.py @args
