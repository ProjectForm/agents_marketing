import os
import logging
import json
from pathlib import Path
from datetime import datetime

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger(__name__)

class DriveManager:
    def __init__(self):
        self.creds = self._authenticate()
        self.service = build('drive', 'v3', credentials=self.creds)
        self.root_folder_id = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
        if not self.root_folder_id:
            logger.error("GOOGLE_DRIVE_ROOT_FOLDER_ID não configurado no .env")
            raise ValueError("GOOGLE_DRIVE_ROOT_FOLDER_ID is not set")

    def _authenticate(self):
        service_account_info = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
        if not service_account_info:
            logger.error("GOOGLE_SERVICE_ACCOUNT_JSON não configurado no .env")
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON is not set")
        
        if service_account_info.startswith('{'):
            info = json.loads(service_account_info)
        else:
            with open(service_account_info, 'r') as f:
                info = json.load(f)

        creds = service_account.Credentials.from_service_account_info(
            info,
            scopes=['https://www.googleapis.com/auth/drive']
        )
        return creds

    def get_or_create_folder(self, name: str, parent_id: str = None) -> str:
        parent_id = parent_id or self.root_folder_id
        query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and '{parent_id}' in parents and trashed = false"
        results = self.service.files().list(q=query, fields="files(id)").execute()
        items = results.get('files', [])

        if items:
            return items[0]['id']
        else:
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_id]
            }
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            logger.info(f"Pasta '{name}' criada com ID: {folder.get('id')}")
            return folder.get('id')

    def upload_file(self, local_path: str, drive_folder_id: str, mime_type: str) -> str:
        file_path = Path(local_path)
        file_metadata = {
            'name': file_path.name,
            'parents': [drive_folder_id]
        }
        media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
        uploaded_file = self.service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
        logger.info(f"Arquivo '{file_path.name}' enviado. Link: {uploaded_file.get('webViewLink')}")
        return uploaded_file.get('webViewLink')

    def upload_text_as_md(self, content: str, filename: str, drive_folder_id: str) -> str:
        temp_md_path = Path(f"/tmp/{filename}")
        with open(temp_md_path, "w", encoding="utf-8") as f:
            f.write(content)
        link = self.upload_file(str(temp_md_path), drive_folder_id, 'text/markdown')
        temp_md_path.unlink()
        return link

    def create_daily_structure(self, date_str: str) -> dict:
        year = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y")
        month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B")
        day_folder_name = date_str

        year_folder_id = self.get_or_create_folder(year, self.root_folder_id)
        month_folder_id = self.get_or_create_folder(month, year_folder_id)
        day_folder_id = self.get_or_create_folder(day_folder_name, month_folder_id)

        instagram_folder_id = self.get_or_create_folder("instagram", day_folder_id)
        facebook_folder_id = self.get_or_create_folder("facebook", day_folder_id)
        tiktok_folder_id = self.get_or_create_folder("tiktok", day_folder_id)

        # Get day folder link
        day_folder = self.service.files().get(fileId=day_folder_id, fields='webViewLink').execute()

        return {
            "day_folder_id": day_folder_id,
            "day_folder_link": day_folder.get('webViewLink'),
            "instagram_folder_id": instagram_folder_id,
            "facebook_folder_id": facebook_folder_id,
            "tiktok_folder_id": tiktok_folder_id,
        }

    def upload_daily_package(self, date_str: str, outputs: dict) -> dict:
        folder_ids = self.create_daily_structure(date_str)
        uploaded_links = {"day_folder_link": folder_ids["day_folder_link"]}

        if "instagram" in outputs:
            insta_folder = folder_ids["instagram_folder_id"]
            if "legendas" in outputs["instagram"]:
                uploaded_links["instagram_legendas"] = self.upload_text_as_md(
                    outputs["instagram"]["legendas"], "legendas.md", insta_folder
                )
            if "roteiros" in outputs["instagram"]:
                uploaded_links["instagram_roteiros"] = self.upload_text_as_md(
                    outputs["instagram"]["roteiros"], "roteiros.md", insta_folder
                )
            if "images" in outputs["instagram"]:
                for img_name, img_path in outputs["instagram"]["images"].items():
                    if img_path:
                        uploaded_links[f"instagram_image_{img_name}"] = self.upload_file(
                            img_path, insta_folder, 'image/png'
                        )
        
        if "facebook" in outputs and "post" in outputs["facebook"]:
            fb_folder = folder_ids["facebook_folder_id"]
            uploaded_links["facebook_post"] = self.upload_text_as_md(
                outputs["facebook"]["post"], "post_storytelling.md", fb_folder
            )

        if "tiktok" in outputs and "roteiro_ugc" in outputs["tiktok"]:
            tiktok_folder = folder_ids["tiktok_folder_id"]
            uploaded_links["tiktok_roteiro_ugc"] = self.upload_text_as_md(
                outputs["tiktok"]["roteiro_ugc"], "roteiro_ugc.md", tiktok_folder
            )

        if "index" in outputs:
            uploaded_links["index_md"] = self.upload_text_as_md(
                outputs["index"], "INDEX.md", folder_ids["day_folder_id"]
            )

        return uploaded_links
