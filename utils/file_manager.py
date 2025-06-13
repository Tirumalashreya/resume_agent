# utils/file_manager.py
from datetime import datetime
import os

def save_output_to_file(content: str, filename: str = None) -> str:
    """
    Saves the provided content to a text file.
    If no filename is specified, a default filename with a timestamp is generated.
    Returns the name of the file saved, or None if an error occurs.
    """
    if not filename:
        # Generate a filename with a timestamp to ensure uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"optimized_resume_{timestamp}.txt" # Default filename

    try:
        # Open the file in write mode ('w') with UTF-8 encoding
        # This will create the file if it doesn't exist, or overwrite it if it does
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content) # Write the content to the file
        print(f"File saved successfully to: {filename}")
        return filename
    except Exception as e:
        print(f"Error saving file '{filename}': {e}")
        return None # Return None to indicate failure
