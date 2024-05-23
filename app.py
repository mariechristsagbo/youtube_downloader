from flask import Flask, render_template, request, redirect, url_for
from pytube import Playlist, YouTube
import re
from pathlib import Path

def get_download_path():
    home_directory = Path.home()
    download_dirs = ["Téléchargements", "Downloads", "Telechargements", "Telechargement", "Téléchargement"]

    for dir_name in download_dirs:
        download_path = home_directory / dir_name
        if download_path.exists() and download_path.is_dir():
            return download_path
    return home_directory / "Downloads"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    home_directory = get_download_path()
    pattern = r'list=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    try:
        if match:
            download_links = []
            playlist = Playlist(url)
            playlist_title = playlist.title
            playlist_directory = home_directory / playlist_title

            for video in playlist.videos:
                video_stream = video.streams.get_highest_resolution()
                video_stream.download(output_path=playlist_directory)
                download_links.append(playlist_directory / f"{video.title}.mp4")
            
            return render_template('index.html', download_links=download_links)
        
        elif 'youtube.com/watch' in url:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download(output_path=home_directory)
            download_link = home_directory / f"{yt.title}.mp4"
            
            return render_template('index.html', download_link=download_link)
        
        else:
            return 'URL invalide.'
    
    except Exception as e:
        return f'Erreur : {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
