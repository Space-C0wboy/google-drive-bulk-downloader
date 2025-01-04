from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pathlib import Path
import logging
from datetime import datetime
from tqdm import tqdm

# Configure logging to file and console
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_file = f"log_{timestamp}.txt"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Log to file
        logging.StreamHandler()        # Log to console
    ]
)

# Paths to be customized by the user
LINKS_FILE_PATH = r'./download_links.txt'  # Path to the file containing Google Drive folder links
OUTPUT_DIRECTORY_PATH = r'./Downloaded_Files'  # Output directory for downloaded files

# Global progress bar
progress_bar = None


def authenticate_drive():
    """
    Authenticate with Google Drive using PyDrive. Reuses saved credentials if available.
    
    Returns:
        GoogleDrive: Authenticated GoogleDrive object.
    """
    try:
        gauth = GoogleAuth()

        # Try to load saved credentials
        if Path("credentials.json").exists():
            gauth.LoadCredentialsFile("credentials.json")
            if gauth.credentials is None or gauth.access_token_expired:
                gauth.Refresh()  # Refresh expired credentials
            else:
                gauth.Authorize()
        else:
            # Authenticate and save credentials for the first time
            gauth.LocalWebserverAuth()
            gauth.SaveCredentialsFile("credentials.json")

        logging.info("Authentication successful.")
        return GoogleDrive(gauth)
    except Exception as e:
        logging.error(f"Failed to authenticate: {e}")
        raise


def count_files(folder_id, drive):
    """
    Recursively counts all files in a Google Drive folder and its subfolders.
    
    Args:
        folder_id (str): ID of the Google Drive folder.
        drive (GoogleDrive): Authenticated GoogleDrive object.
    
    Returns:
        int: Total number of files in the folder and its subfolders.
    """
    try:
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    except Exception as e:
        logging.error(f"Failed to fetch file list for folder ID {folder_id}: {e}")
        return 0

    count = 0
    for file in file_list:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            count += count_files(file['id'], drive)
        else:
            count += 1
    return count


def download_google_drive_folder(folder_id, output_directory, drive):
    """
    Downloads all files from a specified Google Drive folder, avoiding redundant folder structures
    and skipping files that already exist. Updates the global progress bar.
    
    Args:
        folder_id (str): ID of the Google Drive folder.
        output_directory (str): Path to save downloaded files.
        drive (GoogleDrive): Authenticated GoogleDrive object.
    """
    try:
        folder_metadata = drive.CreateFile({'id': folder_id})
        folder_name = folder_metadata['title']
        logging.info(f"Processing folder: {folder_name}")
    except Exception as e:
        logging.error(f"Failed to fetch folder metadata for folder ID {folder_id}: {e}")
        return

    # Avoid redundant folder names by using only the output directory if it matches the current folder
    folder_output_path = Path(output_directory)
    if folder_name not in str(folder_output_path):
        folder_output_path /= folder_name
        folder_output_path.mkdir(parents=True, exist_ok=True)

    try:
        file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    except Exception as e:
        logging.error(f"Failed to fetch file list for folder ID {folder_id}: {e}")
        return

    for file in file_list:
        try:
            if file['mimeType'] == 'application/vnd.google-apps.folder':
                download_google_drive_folder(file['id'], folder_output_path, drive)
            else:
                # Determine the target file path
                file_path = folder_output_path / file['title']

                # Skip if the file already exists
                if file_path.exists():
                    logging.info(f"Skipped: {file['title']} (already exists)")
                    progress_bar.update(1)  # Update progress bar even if skipping
                    continue

                # Download the file
                if 'downloadUrl' in file:
                    file.GetContentFile(str(file_path))
                    logging.info(f"Downloaded: {file['title']} to {file_path}")
                elif 'exportLinks' in file:
                    export_link = file['exportLinks'].get('application/pdf')
                    if export_link:
                        response = drive.auth.service._http.request(export_link)
                        with open(file_path.with_suffix('.pdf'), 'wb') as f:
                            f.write(response[1])
                        logging.info(f"Exported: {file['title']} as PDF")
                    else:
                        logging.warning(f"No export link available for {file['title']}. Skipping.")
                else:
                    logging.warning(f"Skipped: {file['title']} (not downloadable or exportable)")

                progress_bar.update(1)
        except Exception as e:
            logging.error(f"Failed to process {file['title']}: {e}")


def google_drive_bulk_download(links_file_path, output_directory_path):
    """
    Bulk downloads all files from Google Drive folders listed in a file.
    Displays a progress bar during the download process.
    
    Args:
        links_file_path (str): Path to the file containing Google Drive folder links.
        output_directory_path (str): Path to save downloaded files.
    """
    drive = authenticate_drive()

    # Step 1: Extract folder IDs and count all files
    folder_ids = extract_folder_ids(links_file_path)
    if not folder_ids:
        logging.error("No valid folder IDs found. Exiting.")
        return

    logging.info("Counting all files in the provided folders. This may take some time, please be patient...")
    total_files = sum(count_files(folder_id, drive) for folder_id in folder_ids)
    logging.info(f"Total files to download: {total_files}")

    # Step 2: Initialize progress bar
    global progress_bar
    progress_bar = tqdm(total=total_files, desc="Downloading Files", unit="file")

    # Step 3: Download files
    for folder_id in folder_ids:
        download_google_drive_folder(folder_id, output_directory_path, drive)

    progress_bar.close()


def extract_folder_ids(links_file_path):
    """
    Extracts Google Drive folder IDs from a file containing folder links.
    
    Args:
        links_file_path (str): Path to the file containing Google Drive folder links.
    
    Returns:
        list: List of extracted folder IDs.
    """
    try:
        with open(links_file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        logging.error(f"Links file not found: {links_file_path}")
        return []

    folder_ids = []
    for line in lines:
        if "drive.google.com/drive/folders/" in line:
            try:
                folder_id = line.split('/folders/')[1].split('?')[0]
                folder_ids.append(folder_id)
            except IndexError:
                logging.warning(f"Invalid folder link format: {line.strip()}")
    return folder_ids


if __name__ == "__main__":
    google_drive_bulk_download(LINKS_FILE_PATH, OUTPUT_DIRECTORY_PATH)
    logging.info(f"Logs saved to: {log_file}")
