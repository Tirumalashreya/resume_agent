# utils/input_handlers.py
import os
import re
import PyPDF2
import pdfplumber
from pathlib import Path

# PDF processing imports
try:
    import fitz  # PyMuPDF for better PDF handling
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False
    print("PyMuPDF not available. Install with: pip install PyMuPDF")

class ResumeInputHandler:
    """
    Handles different types of resume and job description input (PDF, text file, direct paste).
    Provides methods to extract text from various sources and prompt the user for input.
    """

    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extracts text from a PDF file using multiple libraries for robustness.
        It tries PyMuPDF first (if available), then pdfplumber, and finally PyPDF2.
        """
        text = ""
        print(f"Attempting to extract text from PDF: {pdf_path}")

        # Try PyMuPDF (fitz) if available for potentially better extraction
        if PYMUPDF_AVAILABLE:
            try:
                doc = fitz.open(pdf_path)
                for page in doc:
                    text += page.get_text() # Extract text from each page
                doc.close() # Close the document after extraction
                if text.strip(): # If text was successfully extracted, return it
                    print("✓ Text extracted using PyMuPDF.")
                    return text
            except Exception as e:
                print(f"PyMuPDF extraction failed: {e}. Trying next method...")

        # Try pdfplumber as a fallback
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n" # Append page text with a newline
            if text.strip():
                print("✓ Text extracted using pdfplumber.")
                return text
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}. Trying next method...")

        # Try PyPDF2 as a final fallback
        try:
            with open(pdf_path, 'rb') as file: # Open PDF in binary read mode
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() + "\n" # Extract text from each page
            if text.strip():
                print("✓ Text extracted using PyPDF2.")
                return text
        except Exception as e:
            print(f"PyPDF2 extraction failed: {e}.")

        print("❌ Could not extract text from PDF using any method.")
        return text # Return empty string if no text could be extracted

    @staticmethod
    def get_resume_input() -> str:
        """
        Prompts the user for their resume input method (PDF, text file, or direct paste)
        and returns the extracted resume text.
        """
        print("\n=== RESUME INPUT OPTIONS ===")
        print("1. Upload PDF file")
        print("2. Upload text file")
        print("3. Paste resume text directly")

        while True:
            try:
                choice = input("\nSelect option (1-3): ").strip()

                if choice == "1":
                    return ResumeInputHandler._handle_pdf_input()
                elif choice == "2":
                    return ResumeInputHandler._handle_text_file_input()
                elif choice == "3":
                    return ResumeInputHandler._handle_direct_text_input()
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0) # Exit the program gracefully on user interruption
            except Exception as e:
                print(f"Error getting resume input: {e}")
                continue # Allow the user to try again

    @staticmethod
    def _handle_pdf_input() -> str:
        """Handles input when the user chooses to upload a PDF resume."""
        while True:
            try:
                pdf_path = input("Enter the path to your PDF resume: ").strip().strip('"\'')
                if not os.path.exists(pdf_path):
                    print("File not found. Please check the path and try again.")
                    continue
                if not pdf_path.lower().endswith('.pdf'):
                    print("Please provide a PDF file (.pdf extension).")
                    continue
                
                text = ResumeInputHandler.extract_text_from_pdf(pdf_path)
                if text.strip():
                    print("✓ PDF processed successfully!")
                    return text
                else:
                    print("Could not extract text from PDF. Please try a different file or method.")
                    continue
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error processing PDF: {e}")
                continue

    @staticmethod
    def _handle_text_file_input() -> str:
        """Handles input when the user chooses to upload a text file."""
        while True:
            try:
                file_path = input("Enter the path to your text file: ").strip().strip('"\'')
                if not os.path.exists(file_path):
                    print("File not found. Please check the path and try again.")
                    continue
                with open(file_path, 'r', encoding='utf-8') as file: # Open file in read mode with UTF-8 encoding
                    text = file.read()
                if text.strip():
                    print("✓ Text file processed successfully!")
                    return text
                else:
                    print("File appears to be empty. Please try a different file.")
                    continue
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error reading file: {e}")
                continue

    @staticmethod
    def _handle_direct_text_input() -> str:
        """Handles input when the user chooses to paste text directly."""
        print("\nPaste your resume text below. Type 'END' on a new line when finished:")
        lines = []
        try:
            while True:
                line = input() # Read line by line from user input
                if line.strip().upper() == 'END': # Check for 'END' marker
                    break
                lines.append(line)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            exit(0)

        text = '\n'.join(lines) # Join all lines to form the complete text
        if text.strip():
            print("✓ Text input received successfully!")
            return text
        else:
            print("No text received. Please try again.")
            # Recursively call to prompt again if no text was entered
            return ResumeInputHandler._handle_direct_text_input()

    @staticmethod
    def get_job_description_input() -> str:
        """
        Prompts the user for their job description input method (text file or direct paste)
        and returns the extracted job description text.
        """
        print("\n=== JOB DESCRIPTION INPUT ===")
        print("1. Upload text file")
        print("2. Paste job description directly")

        while True:
            try:
                choice = input("\nSelect option (1-2): ").strip()

                if choice == "1":
                    return ResumeInputHandler._handle_text_file_input() # Reuse text file handler
                elif choice == "2":
                    print("\nPaste the job description below. Type 'END' on a new line when finished:")
                    lines = []
                    try:
                        while True:
                            line = input()
                            if line.strip().upper() == 'END':
                                break
                            lines.append(line)
                    except KeyboardInterrupt:
                        print("\n\nOperation cancelled by user.")
                        exit(0)

                    text = '\n'.join(lines)
                    if text.strip():
                        print("✓ Job description received successfully!")
                        return text
                    else:
                        print("No text received. Please try again.")
                        continue # Prompt again for job description
                else:
                    print("Invalid choice. Please select 1 or 2.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                exit(0)
            except Exception as e:
                print(f"Error getting job description input: {e}")
                continue
