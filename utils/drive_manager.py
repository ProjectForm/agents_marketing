import os
import json
import logging
from pathlib import Path
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

logger = logging.getLogger("finlancer-agency")

class DriveManager:
    def __init__(self):
        self.service = None
        self.creds = None
        self._initialize_service()

    def _initialize_service(self):
        try:
            service_account_info = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
            if service_account_info:
                if service_account_info.startswith("{"):
                    info = json.loads(service_account_info)
                    self.creds = service_account.Credentials.from_service_account_info(info)
                else:
                    self.creds = service_account.Credentials.from_service_account_file(service_account_info)
                
                self.service = build('drive', 'v3', credentials=self.creds)
                logger.info("Google Drive service initialized successfully.")
            else:
                logger.warning("GOOGLE_SERVICE_ACCOUNT_JSON not found. Drive operations will be mocked.")
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive service: {e}")
            self.service = None

    def get_or_create_folder(self, name: str, parent_id: str = None) -> str:
        if not self.service:
            logger.info(f"[MOCK] Folder '{name}' created (parent: {parent_id})")
            return f"mock_folder_id_{name}"

        try:
            query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
            if parent_id:
                query += f" and '{parent_id}' in parents"
            
            results = self.service.files().list(q=query, fields="files(id, name)").execute()
            items = results.get('files', [])

            if items:
                return items[0]['id']
            
            file_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            if parent_id:
                file_metadata['parents'] = [parent_id]
            
            folder = self.service.files().create(body=file_metadata, fields='id').execute()
            return folder.get('id')
        except Exception as e:
            logger.error(f"Error getting/creating folder '{name}': {e}")
            raise

    def upload_file(self, local_path: Path, folder_id: str, mime_type: str) -> str:
        if not self.service:
            logger.info(f"[MOCK] File '{local_path.name}' uploaded to {folder_id}")
            return f"https://drive.google.com/mock/{local_path.name}"

        try:
            file_metadata = {
                'name': local_path.name,
                'parents': [folder_id]
            }
            media = MediaFileUpload(str(local_path), mimetype=mime_type, resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
            
            self.service.permissions().create(
                fileId=file.get('id'),
                body={'type': 'anyone', 'role': 'reader'}
            ).execute()
            
            file = self.service.files().get(fileId=file.get('id'), fields='webViewLink').execute()
            return file.get('webViewLink')
        except Exception as e:
            logger.error(f"Error uploading file '{local_path.name}': {e}")
            raise

    def upload_png(self, local_path: Path, folder_id: str) -> str:
        return self.upload_file(local_path, folder_id, "image/png")
    
    def upload_mp4(self, local_path: Path, folder_id: str) -> str:
        return self.upload_file(local_path, folder_id, "video/mp4")
    
    def upload_md(self, content: str, filename: str, folder_id: str) -> str:
        temp_md_path = Path(f"/tmp/{filename}")
        temp_md_path.write_text(content, encoding="utf-8")
        link = self.upload_file(temp_md_path, folder_id, "text/markdown")
        temp_md_path.unlink()
        return link
    
    def create_and_upload_daily_package(self, run_id: str, 
                                         text_outputs: dict, image_outputs: dict, 
                                         video_files: list, final_review: str, 
                                         output_parser, **kwargs) -> dict:
        uploaded_links = {}
        
        root_id = os.getenv("GOOGLE_DRIVE_ROOT_FOLDER_ID")
        finlancer_marketing_folder_id = self.get_or_create_folder("Finlancer Marketing", root_id)

        # Extrair data do run_id (formato YYYY-MM-DD_HHMMSS)
        date_str = run_id.split('_')[0]
        year = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y")
        year_folder_id = self.get_or_create_folder(year, finlancer_marketing_folder_id)

        month = datetime.strptime(date_str, "%Y-%m-%d").strftime("%B")
        month_folder_id = self.get_or_create_folder(month, year_folder_id)

        day_folder_id = self.get_or_create_folder(run_id, month_folder_id)
        
        if self.service:
            folder_info = self.service.files().get(fileId=day_folder_id, fields='webViewLink').execute()
            uploaded_links["day_folder_link"] = folder_info.get('webViewLink', 'N/A')
        else:
            uploaded_links["day_folder_link"] = f"https://drive.google.com/mock/{run_id}"

        # 01_feed
        feed_folder_id = self.get_or_create_folder("01_feed", day_folder_id)
        if image_outputs.get("feed_image_path"):
            uploaded_links["feed_image"] = self.upload_png(Path(image_outputs["feed_image_path"]), feed_folder_id)
        if text_outputs.get("instagram_legenda"):
            uploaded_links["feed_legenda"] = self.upload_md(text_outputs["instagram_legenda"], "legenda_feed.md", feed_folder_id)

        # 02_carrossel
        carousel_folder_id = self.get_or_create_folder("02_carrossel", day_folder_id)
        if image_outputs.get("carousel_images_paths"):
            for i, img_path in enumerate(image_outputs["carousel_images_paths"]):
                uploaded_links[f"carousel_slide_{i+1:02d}"] = self.upload_png(Path(img_path), carousel_folder_id)
        if text_outputs.get("instagram_carrossel_textos"):
            uploaded_links["carousel_legenda"] = self.upload_md(text_outputs["instagram_carrossel_textos"], "legenda_carrossel.md", carousel_folder_id)

        # 03_ugc_video
        ugc_folder_id = self.get_or_create_folder("03_ugc_video", day_folder_id)
        if video_files:
            for i, v_path in enumerate(video_files):
                uploaded_links[f"ugc_clip_{i+1}"] = self.upload_mp4(Path(v_path), ugc_folder_id)
        if image_outputs.get("ugc_persona_thumbnail_path"):
            uploaded_links["ugc_persona_thumbnail"] = self.upload_png(Path(image_outputs["ugc_persona_thumbnail_path"]), ugc_folder_id)
        if text_outputs.get("ugc_legenda"):
            uploaded_links["ugc_legenda"] = self.upload_md(text_outputs["ugc_legenda"], "legenda_ugc.md", ugc_folder_id)

        # INDEX.md
        index_content = output_parser.generate_index_content(
            run_id=run_id,
            text_outputs=text_outputs,
            image_outputs=image_outputs,
            final_review=final_review,
            uploaded_drive_links=uploaded_links
        )
        uploaded_links["index_file"] = self.upload_md(index_content, "INDEX.md", day_folder_id)

        logger.info(f"✅ Pacote do dia pronto: {uploaded_links.get('day_folder_link', 'N/A')}")
        return uploaded_links
