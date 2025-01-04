
# Google Drive Bulk Downloader

A Python script that automates the process of downloading files and folders from Google Drive. Built using the PyDrive library, this tool allows you to efficiently manage bulk downloads while maintaining folder structures, skipping existing files, and exporting Google Docs/Sheets as PDFs.

---

## Features

- **Bulk Folder Download**: Download entire Google Drive folders, including subfolders.
- **Preserves Folder Structure**: Replicates the Google Drive folder hierarchy on your local machine.
- **File Skipping**: Automatically skips downloading files that already exist locally.
- **Google Docs/Sheets Export**: Converts Google Docs/Sheets to PDFs or other formats during download.
- **Persistent Authentication**: Reuses credentials to avoid repeated logins.
- **Logging**: Saves detailed logs of each run to a timestamped log file.

---

## Requirements

Before using the script, ensure you have the following installed:

- Python 3.6 or later
- Required Python libraries:
  - `pydrive`
  - `pathlib`

Install the dependencies using pip:

```bash
pip install pydrive pathlib
```

---

## Setup

### Step 1: Enable Google Drive API
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project and enable the **Google Drive API**.
3. Navigate to **APIs & Services > Credentials** and create an OAuth 2.0 client ID.
4. Download the `credentials.json` file and place it in the root directory of the script.

### Step 2: Configure the Script
1. Clone the repository and navigate to the folder:
   ```bash
   git clone https://github.com/your-username/google-drive-bulk-downloader.git
   cd google-drive-bulk-downloader
   ```
2. Customize the following paths in the script:
   - **`LINKS_FILE_PATH`**: Path to the text file containing Google Drive folder links.
   - **`OUTPUT_DIRECTORY_PATH`**: Path where downloaded files will be saved.

---

## Usage

### Step 1: Prepare the Links File
Create a text file (e.g., `download_links.txt`) with one Google Drive folder link per line. Example:

```
https://drive.google.com/drive/folders/1ABC123DEF456GHI789JKL?usp=sharing
https://drive.google.com/drive/folders/2XYZ987UVW654RST321OPQ?usp=sharing
```

### Step 2: Run the Script
Run the script using Python:

```bash
python google_drive_bulk_downloader.py
```

### Output
- Files are downloaded into the directory specified in `OUTPUT_DIRECTORY_PATH`.
- Logs are saved to a file named `log_<timestamp>.txt` in the script's root folder.

---

## Folder Structure Example

**Google Drive Structure:**
```
Main Folder
└── Subfolder
    ├── File1.pdf
    └── File2.png
```

**Local Output:**
```
Downloaded_Files
└── Main Folder
    └── Subfolder
        ├── File1.pdf
        └── File2.png
```

---

## Limitations

- Requires public access to Google Drive links or proper authentication for private folders.
- Does not support downloading Google Forms or other unsupported file types.

---

## Contributing

Contributions are welcome! Feel free to open issues, submit pull requests, or suggest enhancements.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [PyDrive Documentation](https://pythonhosted.org/PyDrive/)
- [Google Drive API](https://developers.google.com/drive)
```
