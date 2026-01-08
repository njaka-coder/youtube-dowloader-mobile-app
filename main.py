import threading
from kivy.app import App
from kivy.lang import Builder
from kivy.clock import mainthread
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.uix.button import Button

# Importation de nos modules locaux
import utils
import downloader

# KV_DESIGN = '''
# BoxLayout:
#     orientation: 'vertical'
#     padding: 30
#     spacing: 20
#     canvas.before:
#         Color:
#             rgba: 0.1, 0.1, 0.1, 1
#         Rectangle:
#             pos: self.pos
#             size: self.size

#     Label:
#         text: "YouTube Downloader"
#         font_size: '26sp'
#         bold: True
#         size_hint_y: None
#         height: 60
#         color: 0.9, 0.2, 0.2, 1

#     TextInput:
#         id: url_input
#         hint_text: "Coller l'URL ici..."
#         size_hint_y: None
#         height: 50
#         multiline: False
#         background_color: 0.2, 0.2, 0.2, 1
#         foreground_color: 1, 1, 1, 1

#     BoxLayout:
#         orientation: 'horizontal'
#         size_hint_y: None
#         height: 50
#         Label:
#             text: "Télécharger une Playlist ?"
#         CheckBox:
#             id: playlist_check
#             size_hint_x: 0.2

#     BoxLayout:
#         spacing: 20
#         size_hint_y: None
#         height: 60
#         Button:
#             text: "VIDÉO"
#             background_normal: ''
#             background_color: 0.2, 0.6, 0.8, 1
#             on_release: app.start_thread("video")
#         Button:
#             text: "AUDIO"
#             background_normal: ''
#             background_color: 0.3, 0.7, 0.3, 1
#             on_release: app.start_thread("audio")


#     Label:
#         id: status_label
#         text: "En attente..."
#         text_size: self.width, None
#         halign: 'center'
#         valign: 'middle'
#         color: 0.8, 0.8, 0.8, 1
# '''
class SmoothButton(Button):
    back_color = ListProperty([1, 1, 1, 1])
    radius = ListProperty([15])

KV_DESIGN = '''
# 1. Define a reusable Custom Button with rounded corners
#  Custom property for radius
<SmoothButton>:
    background_color: (0, 0, 0, 0)   #  Make default background transparent
    background_normal: ''           #  Remove default grey texture
    canvas.before:
        Color:
            rgba: self.back_color
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: self.radius

BoxLayout:
    orientation: 'vertical'
    padding: 30
    spacing: 20
    canvas.before:
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "YouTube Downloader"
        font_size: '26sp'
        bold: True
        size_hint_y: None
        height: dp(80) 
        color: (0.9, 0.2, 0.2, 1)

    TextInput:
        id: url_input
        hint_text: "Coller l'URL ici..."
        size_hint_y: None
        height: dp(50)
        multiline: False
        background_color: (0.2, 0.2, 0.2, 1)
        foreground_color: (1, 1, 1, 1)
        # Optional: You can also round the TextInput using similar canvas logic

    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: None
        height: dp(50)
        Label:
            text: "Télécharger une Playlist ?"
        CheckBox:
            id: playlist_check
            size_hint_x: 0.2

    BoxLayout:
        spacing: 20
        size_hint_y: None
        height: dp(60)
        
        # 2. Use the new SmoothButton instead of Button
        SmoothButton:
            text: "VIDÉO"
            back_color: (0.2, 0.6, 0.8, 1)
            on_release: app.start_thread("video")
            
        SmoothButton:
            text: "AUDIO"
            back_color: (0.3, 0.7, 0.3, 1)
            on_release: app.start_thread("audio")
            

    Label:
        id: status_label
        text: "En attente..."
        text_size: self.width, None
        halign: 'center'
        valign: 'middle'
        color: 0.8, 0.8, 0.8, 1
'''

class MainApp(App):
    def build(self):
        # Demander les permissions au lancement (Android seulement)
        utils.request_android_permissions()
        return Builder.load_string(KV_DESIGN)

    def start_thread(self, format_type):
        url = self.root.ids.url_input.text
        if not url:
            self.update_ui("Erreur : URL manquante")
            return

        is_playlist = self.root.ids.playlist_check.active
        
        # Lancer le travail lourd dans un thread
        threading.Thread(
            target=self.run_process, 
            args=(url, format_type, is_playlist)
        ).start()

    def run_process(self, url, format_type, is_playlist):
        # 1. Récupérer le bon dossier
        path = utils.get_download_path()
        self.update_ui(f"Dossier cible : {path}")

        # 2. Configurer le downloader
        dl = downloader.VideoDownloader()
        is_audio = (format_type == "audio")
        
        # 3. Lancer le téléchargement avec callback vers l'UI
        dl.download(url, path, is_audio, is_playlist, self.update_ui)

    @mainthread
    def update_ui(self, message):
        """Met à jour l'UI depuis le thread secondaire"""
        self.root.ids.status_label.text = message

if __name__ == '__main__':
    MainApp().run()