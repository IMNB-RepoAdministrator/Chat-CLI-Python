import os
import zipfile


def decompress(zip_path: str, extract_to_dir: str) -> str:
  """
    Extracts all contents of a zip file into a target directory using zipfile.

    Args:
        zip_path: Path to the .zip file to extract.
        extract_to_dir: Folder where the extracted files will be saved.

    Returns:
        The path to the directory containing the extracted files.
    """
  # Create the destination folder if it does not exist yet
  os.makedirs(extract_to_dir, exist_ok=True)

  # Open the existing zip file in read mode ('r') and extract everything
  with zipfile.ZipFile(zip_path, 'r') as zipf:
    zipf.extractall(extract_to_dir)

  return extract_to_dir
