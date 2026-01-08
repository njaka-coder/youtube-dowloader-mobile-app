# import yt_dlp

# def download_video(url):
#     if not url:
#         raise ValueError("URL must not be empty")
#     else:
#         ydl_opts = {
#             'outtmpl': 'downloads/%(title)s.%(ext)s',
#              'merge_output_format': 'mp4',
#              'yesplaylist': False 
#         }

#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])

# def download_audio(url):
#     ydl_opts = {
#         'format': 'bestaudio',
#         'outtmpl': 'downloads/%(title)s.%(ext)s',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#         }]
#     }
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

# # Example usage:
# download_audio('https://www.youtube.com/watch?v=QiHMkiPGlv4&list=RDQiHMkiPGlv4&start_radio=13')
import yt_dlp
import os

class VideoDownloader:
    def __init__(self):
        self.download_path = ""

    def download(self, url, path, is_audio, is_playlist, status_callback):
        """
        Télécharge le média.
        :param status_callback: Une fonction qui accepte un string (pour les logs)
        """
        self.download_path = path
        
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'noplaylist': not is_playlist,
            'progress_hooks': [lambda d: self._hook(d, status_callback)],
            'quiet': True,
            'no_warnings': True,
            # Astuce pour éviter FFmpeg sur Android (on garde le format natif)
            'format': 'bestaudio/best' if is_audio else 'best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info.get('title', 'Inconnu')
                status_callback(f"Début : {title}")
                
                ydl.download([url])
                
            status_callback("✅ Téléchargement terminé !")
        except Exception as e:
            status_callback(f"❌ Erreur : {str(e)}")

    def _hook(self, d, callback):
        """Gère les retours de yt-dlp"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').strip()
            # Nettoyage des caractères de couleur console
            percent = percent.replace('\x1b[0;94m', '').replace('\x1b[0m', '')
            callback(f"En cours : {percent}")
        elif d['status'] == 'finished':
            callback("Finalisation du fichier...")