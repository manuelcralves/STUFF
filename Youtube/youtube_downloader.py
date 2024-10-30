import yt_dlp
import sys
import os
from tabulate import tabulate

def quiet_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes', 0)
        downloaded_bytes = d.get('downloaded_bytes', 0)

        if total_bytes > 0:
            percent = (downloaded_bytes / total_bytes) * 100
            bar_length = 40  
            block = int(bar_length * downloaded_bytes / total_bytes)
            progress_bar = '#' * block + '-' * (bar_length - block)

            sys.stdout.write(f'\rDownloading: |{progress_bar}| {percent:.2f}% ({downloaded_bytes / (1024 * 1024):.2f} MB of {total_bytes / (1024 * 1024):.2f} MB)')
            sys.stdout.flush()

    elif d['status'] == 'finished':
        sys.stdout.write('\rDownload completed!\n')  
        sys.stdout.flush()

def download_youtube_video(url, output_path='downloads'):
    try:
        os.makedirs(output_path, exist_ok=True)

        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            print("Fetching video information...")
            info_dict = ydl.extract_info(url, download=False)

            formats = info_dict.get('formats', [])
            unique_resolutions = set()  
            available_formats = []

            for f in formats:
                height = f.get('height')
                format_id = f.get('format_id')
                if height is not None and height >= 360:
                    unique_resolutions.add(height)
                    available_formats.append((height, format_id))

            if not available_formats:
                print("No available formats found with resolution 360p or higher.")
                return

            unique_resolutions = sorted(unique_resolutions)  
            table = [[i + 1, res] for i, res in enumerate(unique_resolutions)]
            headers = ["#", "Resolution"]
            print(tabulate(table, headers, tablefmt="fancy_grid"))

            choice = int(input("Select the resolution by number: ")) - 1

            if choice < 0 or choice >= len(unique_resolutions):
                print("Invalid selection. Please try again.")
                return

            selected_resolution = unique_resolutions[choice]

            selected_format = next(format_id for height, format_id in available_formats if height == selected_resolution)

            ydl_opts = {
                'format': selected_format,
                'progress_hooks': [quiet_hook],
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'quiet': True,  
                'no_warnings': True  
            }

            print(f"Starting download in {selected_resolution}p resolution...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL: ")
    download_youtube_video(video_url)
