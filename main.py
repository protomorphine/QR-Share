from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build

from PIL import Image, ImageTk
import qrcode, os

from tkinter import *
from tkinter.filedialog import askopenfilename

# создание окна программы
window = Tk()
window.geometry('377x461')
window.resizable(False, False)
window.title('QR Share v1')
window.configure(background='white')

# область действия OAuth 2.0 для Google Drive API
SCOPES = ['https://www.googleapis.com/auth/drive']

SERVICE_ACCOUNT_FILE = 'alpine-biplane-288221-1bd20ac6dad0.json'

# ID папки на google диске, в которую загружаются файлы
FOLDER_ID = '1AL2Kyo_5ktP0UCpgJ_6ShUgdlWQHs3Z8'

# QR-код с ссылкой на Github
START_IMG = ImageTk.PhotoImage(qrcode.make('https://github.com/protomorphine/QR-Share'))

# авторизация через сервисный аккаунт
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('drive', 'v3', credentials=credentials)

def generate_qr():
    filename = askopenfilename()
    window.title('Создаю QR-код...')
    file_metadata = {
        'name': os.path.basename(filename),
        'parents': [FOLDER_ID]
    }
    media = MediaFileUpload(filename, resumable=True)

    r = service.files().create(body=file_metadata,
                            media_body=media,
                            fields='webContentLink').execute()

    window.geometry('455x544')

    qr_img = ImageTk.PhotoImage(qrcode.make(r['webContentLink']))
    qr_label.configure(image=qr_img)
    qr_label.image = qr_img

    fin_string = f'QR-код для файла {os.path.basename(filename)}'
    filename_label.configure(text=fin_string)
    filename_label.text = fin_string

    window.title('QR-код сгенерирован!')

qr_label = Label(window,
    image = START_IMG
)

button = Button( window,
    text="Выбрать файл",
    padx=10,
    pady=10,
    font=15,
    command = generate_qr
)
filename_label = Label(window,
    background = 'white'
)

qr_label.grid(column=0, row=0)
filename_label.grid(column=0, row=1)
button.grid(column=0, row=2)
window.mainloop()
