import yt_dlp
import os
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet


console = Console()

global_video_format_list = []
global_playlist_format_list = []
formats_displayed = {
    'video': False,
    'playlist': False
}


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


def download_from_youtube(url, format_id, download_path='t7c_dowpy', filename=None, is_audio=False):
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

def download_playlist(url, format_id, download_path='t7c_dowpy', filename=None):
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
    if d['status'] == 'finished':
        console.print(f"[bold green]Download completed: {d['filename']}[/bold green]")


def about_me():
    console.print(Panel(
        Text.from_markup(
            "[bold cyan]About Me[/bold cyan]\n\n"
            "[bold]Author:[/bold] T7C\n"
            "[bold]Contact:[/bold] tranminhtan4953@gmail.com\n\n"
            "[bold]Functionality of the code:[/bold]\n"
            "This code allows you to download videos or audio from YouTube. You can choose the download format, video quality, and even download playlists.\n\n"
            "[bold]New Features:[/bold]\n"
            "1. The ability to download entire playlists from YouTube.\n"
            "2. Improved handling of formats where only the selected format is used for playlist downloads without displaying format details.\n\n"
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
                "[4] Exit\n"
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
            
            download_path = Prompt.ask("Enter the storage folder (leave blank to use the current folder)", default='t7c_dowpy')
            filename = Prompt.ask("Enter output file name (leave blank to use default name)", default="")
            
            download_from_youtube(url, format_id, download_path, filename, is_audio)
        elif choice == '2':
            url = Prompt.ask("Enter the URL of the YouTube playlist")
            
            format_id, is_audio = select_format(global_playlist_format_list, is_playlist=True)
            
            if not confirm_download(is_playlist=True):
                continue  
            
            download_path = Prompt.ask("Enter the storage folder (leave blank to use the current folder)", default='t7c_dowpy')
            filename = Prompt.ask("Enter output file name (leave blank to use default name)", default="")
            
            download_playlist(url, format_id, download_path, filename)
        elif choice == '3':
            about_me()
        elif choice == '4':
            console.print("[bold green]thank for using...[/bold green]")
            break
        else:
            console.print("[bold red]Invalid choice. Please select a valid option.[/bold red]")


if __name__ == "__main__":
    main_menu()


"""Once I remind you that this source code may have errors or not work properly, you can share with me, I am always listening. PLEASE CHOOSE OPTION 1 FIRST AND ENTER YOUR URL, YOU WILL SEE FORMATS CONTAINING IDS THAT ARE ASSIGNABLE TO YOUR URL, PLEASE USE THE SOURCE CODE CORRECTLY."""
