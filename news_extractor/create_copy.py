import pickle
import os
from datetime import datetime
import shutil

def copy_pkl_with_timestamp(file_path):
    # Check if the file exists and has the .pkl extension
    if not os.path.isfile(file_path) or not file_path.endswith('.pkl'):
        raise ValueError("The provided file does not exist or is not a .pkl file.")

    # Get current date and time in the format yyyy_mm_dd_hhmm
    timestamp = datetime.now().strftime('%Y_%m_%d_%H%M')

    # Extract directory, filename, and extension
    file_dir, file_name = os.path.split(file_path)
    
    # Generate the new file name with the timestamp prefix
    new_file_name = f"{timestamp}_{file_name}"
    new_file_path = os.path.join(file_dir, new_file_name)

    # Copy the original .pkl file to the new file
    shutil.copy(file_path, new_file_path)

    print(f"File copied successfully to: {new_file_path}")

# Example usage
original_file_path = r'C:\Users\Thales Henrique\Documents\news_extractor\data\articles_database.pkl'
copy_pkl_with_timestamp(original_file_path)
