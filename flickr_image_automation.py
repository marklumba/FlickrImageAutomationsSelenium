import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def setup_driver(download_dir):
    """Set up and return a Chrome WebDriver with configured download directory."""
    chrome_options = Options()
    # Uncomment the line below if you want to run headless
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    
    # Set download directory
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def download_album(driver, album_url, part_number, download_dir):
    """Navigate to album and download all images as a zip file."""
    print(f"\nAccessing album for Part Number: {part_number}")
    print(f"Album URL: {album_url}")
    
    try:
        # Navigate to the album page
        driver.get(album_url)
        
        # Wait for page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".photo-list-photo-view, .view"))
        )
        
        # Wait a moment to ensure everything is loaded
        time.sleep(5)
        
        # Click the Download button
        download_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//a[span[text()='Download']]"))
        )
        download_button.click()

        # Wait for and click the "Create zip file" button
        create_zip_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Create zip file']]"))
        )
        create_zip_button.click()

        # Wait for and click the "Download zip file" button
        try:
            WebDriverWait(driver, 200).until(
                EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Download zip file')]"))
            )
            download_zip_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Download zip file')]")
            download_zip_button.click()
            print("Successfully clicked the Download zip file button.")
        except TimeoutException:
            print("Timed out waiting for the Download zip file button to appear.")
            return False
        except Exception as e:
            print(f"An error occurred while clicking download button: {str(e)}")
            return False

        # Track files before and after download to identify the new zip file
        initial_files = set(f for f in os.listdir(download_dir) if f.endswith('.zip'))
        max_wait_time = 200  # seconds
        start_time = time.time()
        downloaded = False

        print("Waiting for download to complete...")
        while time.time() - start_time < max_wait_time and not downloaded:
            time.sleep(1)  # Check every second
            current_files = set(f for f in os.listdir(download_dir) if f.endswith('.zip'))
            new_files = current_files - initial_files

            if new_files:
                downloaded = True
                new_file = new_files.pop()  # Take the first new file (should be the latest)
                new_filename = f"{part_number}_{new_file}"
                old_path = os.path.join(download_dir, new_file)
                new_path = os.path.join(download_dir, new_filename)
                
                # Ensure the new filename doesn't already exist
                counter = 1
                while os.path.exists(new_path):
                    base_name, ext = os.path.splitext(new_file)
                    new_filename = f"{part_number}_{base_name}_{counter}{ext}"
                    new_path = os.path.join(download_dir, new_filename)
                    counter += 1
                
                os.rename(old_path, new_path)
                print(f"Download complete! Saved as: {new_filename}")
                break
            elif time.time() - start_time >= max_wait_time:
                print(f"Warning: Could not confirm download completion for {part_number}")

        return downloaded

    except TimeoutException as e:
        print(f"Timeout error for {part_number}: {e}")
        return False
    except NoSuchElementException as e:
        print(f"Element not found for {part_number}: {e}")
        return False
    except Exception as e:
        print(f"Error downloading album for {part_number}: {e}")
        return False

def main():
    # Define the base output directory (for downloads)
    base_output_dir = os.path.abspath("flickr_downloads")
    os.makedirs(base_output_dir, exist_ok=True)
    
    # Read the Excel file from the specific sheet
    try:
        df = pd.read_excel("ORACLE Lighting Digital Assets.xlsx", sheet_name="Sheet1") 
        print("Successfully read Excel file from 'Sheet1' sheet.")
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        print("Please make sure your Excel file exists and has the correct sheet name.")
        print("Exiting program.")
        exit()
    
    # Setup the WebDriver with the download directory
    driver = setup_driver(base_output_dir)
    
    try:
        # Process each row in the DataFrame
        for index, row in df.iterrows():
            part_number = row["Part Number"]
            album_url = row["Image Folder"]
            
            # Download the album
            success = download_album(driver, album_url, part_number, base_output_dir)
            
            if success:
                print(f"Successfully downloaded album for {part_number}")
            else:
                print(f"Failed to download album for {part_number}")
            
            # Add a delay between downloads to avoid rate limiting
            time.sleep(5)
    
    finally:
        # Clean up the WebDriver
        driver.quit()
        
    print("\nDownload process completed!")

if __name__ == "__main__":
    main()


