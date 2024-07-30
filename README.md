# Download Video Youtube - @T7C

## Introduction

T7C Dowpy is a command-line tool for downloading videos and audio from YouTube. This tool allows you to choose the download format, video quality, and even download YouTube playlists. Built with Python and libraries like `yt-dlp`, `rich`, and `pyfiglet`, T7C Dowpy offers a user-friendly interface.

## Features

- Download videos or audio from YouTube.
- Choose download format (mp4, mp3, webm, or video).
- Select maximum video quality (up to 1080p).
- Download YouTube playlists.
- Automatically create a directory for saving downloaded files.
- User interface with clear and understandable notifications.

## Installation

1. **Install Python**: Make sure Python 3.x is installed on your system.
2. **Install dependencies**: Run the following command to install the required libraries:
   ```bash
   pip install yt-dlp rich pyfiglet 

## Usage
1. Run the program: Execute the yt_vidow.py file with the following command:
   ```bash
   python getvideoyt.py

## Error Handling
- Internet Connection: Ensure you have a stable internet connection.
- Dependencies: Check that libraries like yt-dlp and ffmpeg are properly installed.
- URL and Options: Verify that the URL and input options are correct.
- Support: If issues persist, send a detailed error message to the author via email.


# Installing FFmpeg using Chocolatey

If you want to install `ffmpeg` using Chocolatey on Windows, follow these steps:

## 1. Install Chocolatey (if not already installed)

1. Open Command Prompt as Administrator:
   - Search for "cmd" in the Start Menu.
   - Right-click on "Command Prompt" and select "Run as administrator".

2. Run the following command to install Chocolatey:

    ```bash
    @powershell -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"
    ```

3. After installation, restart Command Prompt or open a new Command Prompt window to ensure Chocolatey is recognized.

## 2. Install FFmpeg

1. Open Command Prompt as Administrator.

2. Run the following command to install `ffmpeg`:

    ```bash
    choco install ffmpeg
    ```

3. Wait for the installation to complete. Chocolatey will automatically download and install `ffmpeg` along with all necessary dependencies.

## 3. Verify Installation

1. After installation, check if `ffmpeg` has been installed correctly by running the following command in Command Prompt:

    ```bash
    ffmpeg -version
    ```

2. This command will display the version of `ffmpeg` if the installation was successful.

## End

- Make sure to open Command Prompt with Administrator privileges to perform the installation of Chocolatey and FFmpeg.
- You can use Chocolatey to manage other software packages on Windows, making it easy to update and maintain the tools you need.

With this method, you can easily and quickly install `ffmpeg` on Windows.


## Disadvantage

- if download playlist, it make happen with lists_format because any video have different format, pls keep link of the videos you like - download each for a better experience, or you want download all pls wait for format loading and choose id for you download.

## Hope
- i ways for feedback of you with my code, i will hear opinions from you. gook luck
