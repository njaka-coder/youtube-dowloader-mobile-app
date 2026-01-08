import os
from kivy.utils import platform

def get_download_path():
    """Retourne le dossier de téléchargement approprié selon l'OS."""
    if platform == 'android':
        from android.storage import primary_external_storage_path
        # Sur Android, on vise le dossier Download public
        dir_path = os.path.join(primary_external_storage_path(), 'Download')
    else:
        # Sur PC (Windows/Mac/Linux)
        dir_path = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        
    return dir_path

def request_android_permissions():
    """Demande les permissions nécessaires au démarrage sur Android."""
    if platform == 'android':
        from android.permissions import request_permissions, Permission
        request_permissions([
            Permission.INTERNET, 
            Permission.WRITE_EXTERNAL_STORAGE, 
            Permission.READ_EXTERNAL_STORAGE
        ])