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

    # Si aucun des dossiers n'existe, renvoie simplement le dossier de l'utilisateur
    return home_directory / "Downloads"


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    home_directory = Path.home() / "Downloads"
    pattern = r'list=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    if match:
        if 'index' not in url:
            try:
                playlist = Playlist(url)
                playlist_title = playlist.title
                playlist_directory = home_directory / playlist_title

                for video in playlist.videos:
                    video.streams.get_highest_resolution().download(output_path=playlist_directory)
                return 'Téléchargement de la playlist terminé.'
            except Exception as e:
                return f'Erreur : {str(e)}'
        else:
            try:
                yt = YouTube(url)
                video = yt.streams.get_highest_resolution()
                video.download(output_path = home_directory)
                return f"Le téléchargement de la vidéo '{video.title}' terminé."
            except Exception as e:
                return f'Erreur : {str(e)}'
    elif 'youtube.com/watch' in url:
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download(output_path = home_directory)
            return f"Le téléchargement de la vidéo '{video.title}' terminé."
        except Exception as e:
            return f'Erreur : {str(e)}'
    else:
        return 'URL invalide.'

if __name__ == '__main__':
    app.run(debug=True)