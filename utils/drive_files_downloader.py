import io
import os
import re
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import PyPDF2
import configparser


# Get the absolute path of the script file
script_dir = os.path.dirname(os.path.abspath(__file__))

# Change the working directory to the parent folder
os.chdir(os.path.join(script_dir, '..'))

config = configparser.ConfigParser()
config.read('config.ini')

# Set up credentials and build Drive API client
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/bigquery',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
    ]
# replace with your service account file path
SERVICE_ACCOUNT_FILE = config['api_keys']['GOOGLE_API_JSON_PATH']
creds = None
try:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
except FileNotFoundError:
    print('The service account file was not found.')
if creds:
    drive_service = build('drive', 'v3', credentials=creds)

# Define a function to download a PDF file from Drive

# list files in google drive folder
def list_files_in_folder(folder_id):
    # Call the Drive API to list files in the folder
    query = f"'{folder_id}' in parents"
    results = drive_service.files().list(
        q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    # Print the name and ID of each file in the folder
    if not items:
        print('No files found in the folder.')
    else:
        print('Files in the folder:')
        for item in items:
            print(f'{item["name"]} ({item["id"]})')


def download_pdf(file_id, file_name):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = io.BytesIO()
        downloader.write(request.execute())
        downloader.seek(0)
        pdf_reader = PyPDF2.PdfFileReader(downloader)
        with open(file_name, 'wb') as f:
            f.write(downloader.read())
    except HttpError as error:
        print(f'An error occurred: {error}')
        downloader.close()
        return None
    downloader.close()
    return pdf_reader

# Define a function to parse the contents of a PDF file


def parse_pdf(file_reader):
    # Implement your parsing logic here
    # For example, extract text from the first page of the PDF
    page = file_reader.getPage(0)
    text = page.extractText()
    # Use regular expressions to extract specific information
    matches = re.findall(r'Total: \$(\d+\.\d{2})', text)
    if matches:
        total = float(matches[0])
        print(f'Total amount: ${total:.2f}')
    else:
        print('Total amount not found in PDF')
        
if __name__ == '__main__':
    google_drive_folder_id = '1znbd1nC5KGx8iIXqfXaumhYP3a2cQ8fj'
    articles = list_files_in_folder(google_drive_folder_id)
    for article in articles:
        continue
        # Download a sample PDF file from Drive and parse its contents
        file_id = 'your_file_id_here'  # replace with the ID of your PDF file in Drive
        file_name = 'sample.pdf'
        pdf_reader = download_pdf(file_id, file_name)
        if pdf_reader:
            parse_pdf(pdf_reader)

        # Optional: delete the downloaded file
        os.remove(file_name)
