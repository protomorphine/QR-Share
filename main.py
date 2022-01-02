from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
from PIL import Image
import qrcode, os, sys

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = '' # путь к json-файлу с сервисным ключом 

# ID папки на google диске, в которую загружаются файлы
FOLDER_ID = '1AL2Kyo_5ktP0UCpgJ_6ShUgdlWQHs3Z8'

# авторизация через сервисный аккаунт
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

file_metadata = {
    'name': os.path.basename(sys.argv[1]),
    'parents': [FOLDER_ID]
}
media = MediaFileUpload(sys.argv[1], resumable=True)

r = service.files().create(body=file_metadata,
                           media_body=media,
                           fields='webContentLink').execute()

qr_img = qrcode.make(r['webContentLink'])

qr_img.show()
