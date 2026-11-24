import os
import zipfile


def compress(source_path: str, output_zip_path: str) -> str:
  """
    Compresses a file or directory into a zip archive using zipfile.

    Args:
        source_path: Path to the file or folder to compress.
        output_zip_path: Destination path for the resulting .zip file.

    Returns:
        The path to the created zip file.
    """
  # Open a new zip file in write mode ('w') using DEFLATE compression
  with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Check if the source is a directory
    if os.path.isdir(source_path):
      # Walk through all folders and files inside the directory
      for root, _, files in os.walk(source_path):
        for file in files:
          full_path = os.path.join(root, file)
          # Calculate relative path so the zip doesn't include full system drive paths
          relative_path = os.path.relpath(full_path, source_path)
          zipf.write(full_path, arcname=relative_path)
    else:
      # If it is a single file, add it directly using just its filename
      zipf.write(source_path, arcname=os.path.basename(source_path))

  return output_zip_path
