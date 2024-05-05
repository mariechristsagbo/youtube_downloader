from flask import Flask, render_template, request, redirect, url_for
from pytube import Playlist, YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    if 'youtube.com/playlist' in url:
        try:
            playlist = Playlist(url)
            for video in playlist.videos:
                video.streams.get_highest_resolution().download()
            return 'Téléchargement de la playlist terminé.'
        except Exception as e:
            return f'Erreur : {str(e)}'
    elif 'youtube.com/watch' in url:
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            video.download()
            return f"Le téléchargement de la vidéo '{video.title}' terminé."
        except Exception as e:
            return f'Erreur : {str(e)}'
    else:
        return 'URL invalide.'

if __name__ == '__main__':
    app.run(debug=True)
