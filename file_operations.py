import os
import shutil
import subprocess
import logging

from google_sheets import update_google_sheet

INPUT_DIR = os.environ.get('INPUT_DIR', '/app/input')
OUTPUT_DIR = os.environ.get('OUTPUT_DIR', '/app/output')
LOG_DIR = os.environ.get('LOG_DIR', '/app/logs')
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov']

logging.basicConfig(filename=os.path.join(LOG_DIR, 'file_operations.log'), level=logging.INFO)

def is_valid_video(file_path):
    # Add validation logic as needed
    return True

def create_folder_structure(base_path):
    categories = ["adult", "non_adult", "errors"]
    for category in categories:
        os.makedirs(os.path.join(base_path, category), exist_ok=True)

def copy_and_rename_file(src, dst):
    shutil.copy2(src, dst)
    base, ext = os.path.splitext(dst)
    os.rename(dst, base + "_validated" + ext)

def main():
    create_folder_structure(OUTPUT_DIR)
    for root, dirs, files in os.walk(INPUT_DIR):
        for file in files:
            if any(file.lower().endswith(ext) for ext in VIDEO_EXTENSIONS):
                file_path = os.path.join(root, file)
                if is_valid_video(file_path):
                    output_path = os.path.join(OUTPUT_DIR, "non_adult", file)
                    try:
                        subprocess.run(['python', '/app/scripts/analyze_video.py', file_path, OUTPUT_DIR])
                        copy_and_rename_file(file_path, output_path)
                        update_google_sheet(file_path, output_path)
                        logging.info(f"Processed and copied: {file_path}")
                    except Exception as e:
                        error_path = os.path.join(OUTPUT_DIR, "errors", file)
                        shutil.copy2(file_path, error_path)
                        logging.error(f"Error processing {file_path}: {str(e)}")
                else:
                    error_path = os.path.join(OUTPUT_DIR, "errors", file)
                    shutil.copy2(file_path, error_path)
                    logging.warning(f"Invalid video file: {file_path}")

if __name__ == "__main__":
    main()
