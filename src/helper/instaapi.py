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
            # Login with saved session if available
            if os.path.exists(f"{self.username}_session.json"):
                self.client.load_settings(f"{self.username}_session.json")
                self.client.login(self.username, self.password)
            else:
                # Normal login process
                self.client.login(self.username, self.password)
                self.client.dump_settings(f"{self.username}_session.json")
        except LoginRequired as e:
            print("Login required, attempting manual login...")
            self.handle_two_factor_auth()
        except Exception as e:
            print(f"Unexpected error during login: {e}")

    def handle_two_factor_auth(self):
        try:
            # Trigger login to receive the 2FA code prompt
            self.client.login(self.username, self.password)
        except Exception as e:
            # Check if 2FA is required
            if 'Two-factor authentication required' in str(e):
                verification_code = input("Enter the 2FA verification code sent to your device: ")
                try:
                    self.client.two_factor_login(verification_code)
                    print("2FA login successful.")
                    self.client.dump_settings(f"{self.username}_session.json")
                except Exception as e:
                    print(f"2FA login failed: {e}")
            else:
                print(f"Unexpected login error: {e}")

    def upload_photo(self, photo_path: str, caption: str) -> dict:
        """
        Uploads a photo to Instagram.
        :param photo_path: The full path to the image file.
        :param caption: The photo description.
        :return: Information about the uploaded post.
        """
        if not os.path.exists(photo_path):
            raise FileNotFoundError(f"The image at '{photo_path}' was not found.")

        result = self.client.photo_upload(photo_path, caption)

        # Convert the result to a dictionary for JSON response
        return {
            "status": "success",
            "media_id": result.dict().get("id"),
            "media_url": result.dict().get("media_url"),
            "caption": caption,
        }

    def upload_video(self, video_path: str, thumbnail_path: str, caption: str) -> dict:
        """
        Uploads a video to Instagram.
        :param video_path: The full path to the video file.
        :param thumbnail_path: The full path to the thumbnail image.
        :param caption: The video caption.
        :return: A dictionary with upload details.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"The video at '{video_path}' was not found.")
        if not os.path.exists(thumbnail_path):
            raise FileNotFoundError(f"The thumbnail at '{thumbnail_path}' was not found.")

        result = self.client.video_upload(video_path, caption, thumbnail_path)

        # Convert result to a dictionary for JSON response
        return {
            "status": "success",
            "media_id": result.dict().get("id"),
            "media_url": result.dict().get("media_url"),
            "caption": caption,
        }

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
