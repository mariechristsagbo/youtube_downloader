from flask import Flask, render_template, request, redirect, url_for
from pytube import Playlist, YouTube
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    pattern = r'list=([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    if match:
        try:
            playlist = Playlist(url)
            download_links = []
            for video in playlist.videos:
                download_links.append(video.streams.get_highest_resolution().url)
        
            print(download_links)
            return render_template('download.html', download_link=download_links)
        except Exception as e:
            return f'Erreur : {str(e)}'
    elif 'youtube.com/watch' in url:
        try:
            yt = YouTube(url)
            video = yt.streams.get_highest_resolution()
            print(video.url)
            return render_template('download.html', download_link=video.url)
        except Exception as e:
            return f'Erreur : {str(e)}'
    else:
        return 'URL invalide.'

if __name__ == '__main__':
    app.run(debug=True)