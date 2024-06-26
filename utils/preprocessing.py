"""
Filename: preprocessing.py
Author: Ashish Sharma
Date created: 2024-04-28
License: MIT License
Description: This file contains utility functions related to preprocessing of data.
"""

import re
from PyPDF2 import PdfReader
from utils.logs import logger

def extract_text_from_pdf(file_path):
  """
  Extracts text from a PDF file and returns the combined text.

  Args:
      file_path (str): The path to the PDF file.

  Returns:
      str: The extracted text from the PDF file.
  """

  logger.info("Extracting text from pdf...")
  try:
    with open(file_path, 'rb') as pdf_file:
      reader = PdfReader(pdf_file)
      totalPages = len(reader.pages)
      extracted_text = ""

      for i in range(1, totalPages):
        extracted_text += reader.pages[i].extract_text()

      return extracted_text
  except FileNotFoundError:
      logger.error(f"Error: File not found at {file_path}")
      return ""

def clean_up_text(content: str) -> str:
    """
    Remove unwanted characters and patterns in text input.

    :param content: Text input.
    
    :return: Cleaned version of original text input.
    """
    try:
        logger.info("Data cleaning...")

        # Fix hyphenated words broken by newline
        content = re.sub(r'(\w+)-\n(\w+)', r'\1\2', content)

        # Remove specific unwanted patterns and characters
        unwanted_patterns = [
            "\\n", "  —", "——————————", "—————————", "—————",
            r'\\u[\dA-Fa-f]{4}', r'\uf075', r'\uf0b7',
            r'\.{2,}'
        ]
        for pattern in unwanted_patterns:
            content = re.sub(pattern, "", content)

        # Fix improperly spaced hyphenated words and normalize whitespace
        content = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', content)
        content = re.sub(r'\s+', ' ', content)

        content = content.lower()

        return content
    except Exception as e:
        logger.error(f"An error occurred during data cleaning: {e}")
        return None