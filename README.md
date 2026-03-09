# google-drive-bulk-downloader

Downloads Google Drive folders in bulk using PyDrive. Mirrors the remote folder structure locally, skips files that already exist, and exports Google Docs/Sheets as PDFs.

## Requirements

- Python 3.6+
- `pydrive`

```bash
pip install pydrive
```

You also need a Google Cloud project with the Drive API enabled and an OAuth 2.0 `credentials.json` file in the script directory. See [Google's OAuth setup guide](https://developers.google.com/drive/api/quickstart/python) for steps.

## Configuration

Edit the script and set:

```python
LINKS_FILE_PATH = 'download_links.txt'    # path to your links file
OUTPUT_DIRECTORY_PATH = 'downloaded'      # where files get saved
```

## Usage

1. Create a text file with one Google Drive folder URL per line:

```
https://drive.google.com/drive/folders/FOLDER_ID_1
https://drive.google.com/drive/folders/FOLDER_ID_2
```

2. Run the script:

```bash
python google_drive_bulk_downloader.py
```

On first run, it will open a browser window for OAuth authentication. Credentials are cached locally for subsequent runs.

## Output

- Files are saved to `OUTPUT_DIRECTORY_PATH`, mirroring the Drive folder hierarchy.
- Each run writes a timestamped log file to the script directory.

## Limitations

- Folders must be accessible to the authenticated account (public links or shared with your account).
- Google Forms and a few other Drive types are not supported for export.
