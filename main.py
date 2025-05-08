"""
t7c_dowpy - YouTube Downloader
Version: 1.02
Last Updated: 05/08/2025

Changelog:
- Added yt-dlp auto-update feature
- Improved error handling
- Enhanced user interface
- Added playlist download optimization
- Added format selection improvements
- Changed default download directory to 'downloads'

Author: tanbaycu
Contact: dev.tanbaycu@gmail.com
"""

import yt_dlp
import os
import subprocess
import sys
import json
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

# Default configuration
DEFAULT_DOWNLOAD_DIR = 'downloads'
HISTORY_FILE = 'download_history.json'

global_video_format_list = []
global_playlist_format_list = []
formats_displayed = {
    'video': False,
    'playlist': False
}

def load_download_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_download_history(url, filename, format_type):
    history = load_download_history()
    history.append({
        'url': url,
        'filename': filename,
        'format_type': format_type,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=4)
    except:
        console.print("[yellow]Warning: Could not save download history[/yellow]")

def show_download_history():
    history = load_download_history()
    if not history:
        console.print("[yellow]No download history found[/yellow]")
        return

    console.print("\n[bold cyan]Download History:[/bold cyan]")
    for item in history[-10:]:  # Show last 10 downloads
        console.print(f"[green]URL:[/green] {item['url']}")
        console.print(f"[green]File:[/green] {item['filename']}")
        console.print(f"[green]Format:[/green] {item['format_type']}")
        console.print(f"[green]Date:[/green] {item['timestamp']}")
        console.print("-" * 50)

def print_ascii_title():
    figlet = Figlet(font='slant')
    ascii_title = figlet.renderText('t7c_dowpy') #OR YOU CAN CHANGE FOLDER
    console.print(ascii_title, style="bold cyan")


def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def list_formats(url, for_playlist=False):
    format_type = 'playlist' if for_playlist else 'video'
    if formats_displayed[format_type]:
        return global_playlist_format_list if for_playlist else global_video_format_list
    
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'listformats': True,
        'geo_bypass': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        
        if for_playlist:
           
            format_list = [format_info.get('format_id', 'N/A') for format_info in formats]
            global_playlist_format_list.extend(format_list)
        else:
            console.print("[bold cyan]Available formats:[/bold cyan]")
            format_list = []
            for format_info in formats:
                format_id = format_info.get('format_id', 'N/A')
                format_note = format_info.get('format_note', '')
                resolution = format_info.get('height', 'N/A')
                extension = format_info.get('ext', 'N/A')
                format_type = 'audio' if 'audio' in extension else 'video'
                format_list.append({
                    'id': format_id,
                    'note': format_note,
                    'resolution': resolution,
                    'extension': extension,
                    'type': format_type
                })
                console.print(f"[bold green]{format_id}[/bold green] - {format_note} - {resolution}p - {extension} ({format_type})")
            
            global_video_format_list.extend(format_list)
        
        formats_displayed[format_type] = True
        return format_list


def download_from_youtube(url, format_id, download_path=DEFAULT_DOWNLOAD_DIR, filename=None, is_audio=False):
    create_directory_if_not_exists(download_path)

    if not filename:
        filename = '%(title)s.%(ext)s'
    
    ydl_opts = {
        'outtmpl': os.path.join(download_path, filename),
        'progress_hooks': [progress_hook],
        'geo_bypass': True,
    }

    if is_audio:
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = format_id
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            console.print(f"[bold green]Download successful![/bold green]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

def download_playlist(url, format_id, download_path=DEFAULT_DOWNLOAD_DIR, filename=None):
    create_directory_if_not_exists(download_path)  

    if not filename:
        filename = '%(playlist)s/%(title)s.%(ext)s'
    
    ydl_opts = {
        'outtmpl': os.path.join(download_path, filename),
        'progress_hooks': [progress_hook],
        'geo_bypass': True,  
        'format': format_id,
        'noplaylist': False,  
    }

    if format_id == 'bestaudio/best':  
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            console.print(f"[bold green]Playlist download successful![/bold green]")
    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")



def progress_hook(d):
    if d['status'] == 'downloading':
        try:
            percent = d.get('_percent_str', '0%')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            console.print(f"[bold cyan]Downloading: {percent} at {speed} - ETA: {eta}[/bold cyan]", end='\r')
        except:
            pass
    elif d['status'] == 'finished':
        console.print(f"\n[bold green]Download completed: {d['filename']}[/bold green]")


def about_me():
    console.print(Panel(
        Text.from_markup(
            "[bold cyan]About Me[/bold cyan]\n\n"
            "[bold]Version:[/bold] 1.02\n"
            "[bold]Author:[/bold] tanbaycu\n"
            "[bold]Contact:[/bold] tranminhtan4953@gmail.com\n\n"
            "[bold]Functionality of the code:[/bold]\n"
            "This code allows you to download videos or audio from YouTube. You can choose the download format, video quality, and even download playlists.\n\n"
            "[bold]New Features in v1.02:[/bold]\n"
            "1. Added automatic yt-dlp update feature\n"
            "2. Improved download progress display\n"
            "3. Enhanced error handling and user feedback\n"
            "4. Added download speed and ETA information\n"
            "5. Optimized playlist downloads\n\n"
            "[bold]How to use:[/bold]\n"
            "1. Run the program.\n"
            "2. Select the option to download video, audio, or playlist.\n"
            "3. Enter the URL of the video or playlist.\n"
            "4. For videos, view and select from the available formats before downloading.\n"
            "5. For playlists, select the desired format without viewing the format list.\n"
            "6. Enter the storage folder and file name if needed.\n\n"
            "[bold]How to handle errors:[/bold]\n"
            "1. Check your internet connection.\n"
            "2. Ensure you have all dependencies installed such as `yt-dlp` and `ffmpeg`, or `pyfiglet` and `rich`.\n"
            "3. Verify the URL and input options. Make sure the URL is correct and the format ID exists.\n"
            "4. If you encounter issues with format selection, ensure that the format ID is valid and properly entered.\n"
            "5. If the download fails, check if there are any restrictions or issues with the YouTube video or playlist.\n"
            "6. For persistent errors, consult the program's error message or log for more details, and consider contacting the author with the error information.\n"
            "7. Try updating yt-dlp using option 4 in the main menu if you encounter download issues.\n"
        ),
        title="About Me",
        border_style="bold cyan"
    ))



def select_format(formats, is_playlist=False):
    format_dict = {f['id']: f for f in formats}
    if is_playlist:
        console.print("[bold cyan]Select a format for the playlist:[/bold cyan]")
    else:
        console.print("[bold cyan]Select a format for the video:[/bold cyan]")
    
    while True:
        format_id = Prompt.ask("Enter the format ID or 'audio' for audio only", default="audio")
        if format_id.lower() == 'audio':
            return 'bestaudio/best', True
        if format_id in format_dict:
            return format_id, False
        console.print("[bold red]Invalid format ID. Please try again.[/bold red]")

# Function to confirm download
def confirm_download(is_playlist=False):
    if is_playlist:
        message = "Are you sure you want to download this playlist? (y/n)"
    else:
        message = "Are you sure you want to download this video? (y/n)"
    
    confirmation = Prompt.ask(message)
    if confirmation.lower() != 'y':
        console.print("[bold yellow]Download cancelled. Returning to main menu.[/bold yellow]")
        return False
    return True

def update_ytdlp():
    try:
        console.print("[bold yellow]Checking for yt-dlp updates...[/bold yellow]")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"], check=True)
        console.print("[bold green]yt-dlp has been successfully updated![/bold green]")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Failed to update yt-dlp: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

# Main menu
def main_menu():
    print_ascii_title()  
    
    while True:
        console.print(Panel(
            Text.from_markup(
                "[bold cyan]Main Menu[/bold cyan]\n\n"
                "[1] Download YouTube Video\n"
                "[2] Download YouTube Playlist\n"
                "[3] About Me\n"
                "[4] Update yt-dlp\n"
                "[5] Exit\n"
            ),
            title="Youtube Download Video",
            border_style="bold cyan"
        ))
        choice = Prompt.ask("Select an option").strip()

        if choice == '1':
            url = Prompt.ask("Enter the URL of the YouTube video")
            formats = list_formats(url)  
            format_id, is_audio = select_format(formats)
            
            if not confirm_download():
                continue  
            
            download_path = Prompt.ask("Enter the storage folder (leave blank to use the default folder)", default=DEFAULT_DOWNLOAD_DIR)
            filename = Prompt.ask("Enter output file name (leave blank to use default name)", default="")
            
            download_from_youtube(url, format_id, download_path, filename, is_audio)
        elif choice == '2':
            url = Prompt.ask("Enter the URL of the YouTube playlist")
            
            format_id, is_audio = select_format(global_playlist_format_list, is_playlist=True)
            
            if not confirm_download(is_playlist=True):
                continue  
            
            download_path = Prompt.ask("Enter the storage folder (leave blank to use the default folder)", default=DEFAULT_DOWNLOAD_DIR)
            filename = Prompt.ask("Enter output file name (leave blank to use default name)", default="")
            
            download_playlist(url, format_id, download_path, filename)
        elif choice == '3':
            about_me()
        elif choice == '4':
            update_ytdlp()
        elif choice == '5':
            console.print("[bold green]Thank you for using t7c_dowpy![/bold green]")
            break
        else:
            console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")


if __name__ == "__main__":
    main_menu()


