# Flickr Album Downloader

A Python automation tool that downloads image albums from Flickr based on a list of URLs in an Excel file.

## Overview

This script automates the process of:
1. Reading album URLs from an Excel spreadsheet
2. Navigating to each Flickr album
3. Downloading all images in the album as a zip file
4. Renaming the downloaded zip with the part number for easy identification

## Features

- Automated Flickr album batch downloading
- Excel spreadsheet integration for managing download targets
- Custom file naming based on part numbers
- Configurable Chrome WebDriver options
- Error handling with detailed logging
- Download tracking and confirmation

## Requirements

- Python 3.6+
- Chrome web browser
- Following Python packages:
  - pandas
  - selenium
  - openpyxl (for Excel file handling)

## Installation

1. Clone this repository or download the script
2. Install required packages:

```bash
pip install pandas selenium openpyxl
```

3. Download the appropriate [ChromeDriver](https://sites.google.com/chromium.org/driver/) for your Chrome version
4. Ensure ChromeDriver is in your system PATH or in the same directory as the script

## Input File Format

The script expects an Excel file named `ORACLE Lighting Digital Assets.xlsx` with a sheet named `Sheet1` containing the following columns:
- `Part Number`: A unique identifier for each product
- `Image Folder`: The URL to the Flickr album

## Usage

1. Prepare your Excel file with part numbers and Flickr album URLs
2. Run the script:

```bash
python flickr_downloader.py
```

3. The script will:
   - Create a `flickr_downloads` directory if it doesn't exist
   - Process each row in the Excel file
   - Download and rename zip files with the format `{part_number}_{original_filename}.zip`

## Configuration Options

You can modify the following settings in the script:

- **Headless Mode**: Uncomment the line `chrome_options.add_argument("--headless")` to run Chrome in headless mode
- **Download Directory**: Change `base_output_dir` in the `main()` function
- **Wait Times**: Adjust the various `time.sleep()` and `WebDriverWait` durations
- **Excel File Details**: Change the file name or sheet name in the `main()` function

## Troubleshooting

- **Downloads not completing**: Increase the `max_wait_time` variable
- **Element not found errors**: The Flickr UI may have changed; update the XPath or CSS selectors
- **Rate limiting**: Increase the delay between downloads by adjusting the `time.sleep(5)` value

## How It Works

1. **Setup**: Configures Chrome WebDriver with download preferences
2. **Data Loading**: Reads part numbers and URLs from the Excel file
3. **For each URL**:
   - Navigates to the album
   - Clicks the "Download" button
   - Selects "Create zip file"
   - Waits for zip creation and downloads it
   - Renames the file with the part number prefix
4. **Cleanup**: Closes the browser when all downloads are complete

