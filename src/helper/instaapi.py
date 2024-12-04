from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os


class InstagramService:
    def __init__(self, username: str, password: str):
        self.client = Client()
        self.username = username
        self.password = password
        self.login()

    def login(self):
        try:
            # Login mit gespeicherten Sitzungsdaten (falls vorhanden)
            if os.path.exists(f"{self.username}_session.json"):
                self.client.load_settings(f"{self.username}_session.json")
                self.client.login(self.username, self.password)
            else:
                # Normaler Login
                self.client.login(self.username, self.password)
                self.client.dump_settings(f"{self.username}_session.json")
        except LoginRequired:
            print("Login erforderlich, versuche erneut...")
            self.client.login(self.username, self.password)
            self.client.dump_settings(f"{self.username}_session.json")

    def upload_photo(self, photo_path: str, caption: str) -> dict:
        """
        Lädt ein Foto auf Instagram hoch.
        :param photo_path: Der vollständige Pfad zur Bilddatei.
        :param caption: Die Bildbeschreibung.
        :return: Informationen über den hochgeladenen Beitrag.
        """
        if not os.path.exists(photo_path):
            raise FileNotFoundError(f"Das Bild unter '{photo_path}' wurde nicht gefunden.")

        return self.client.photo_upload(photo_path, caption)

    def upload_video(self, video_path: str, thumbnail_path: str, caption: str) -> dict:
        """
        Lädt ein Video auf Instagram hoch.
        :param video_path: Der vollständige Pfad zur Videodatei.
        :param thumbnail_path: Der vollständige Pfad zum Vorschaubild (Thumbnail).
        :param caption: Die Videobeschreibung.
        :return: Informationen über den hochgeladenen Beitrag.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Das Video unter '{video_path}' wurde nicht gefunden.")
        if not os.path.exists(thumbnail_path):
            raise FileNotFoundError(f"Das Thumbnail unter '{thumbnail_path}' wurde nicht gefunden.")

        return self.client.video_upload(video_path, caption, thumbnail_path)

    def upload_reel(self, video_path: str, caption: str) -> dict:
        """
        Lädt ein Reel auf Instagram hoch.
        :param video_path: Der vollständige Pfad zur Videodatei.
        :param caption: Die Beschreibung des Reels.
        :return: Informationen über den hochgeladenen Beitrag.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Das Video unter '{video_path}' wurde nicht gefunden.")

        return self.client.clip_upload(video_path, caption)
