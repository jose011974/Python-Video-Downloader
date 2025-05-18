import os
import re

def rename_files():
  """Renames files in the current directory by removing the last 3 characters
  before the file extension.
  """
  for filename in os.listdir("."):
    # Use regex to match the filename pattern
    match = re.match(r"^(.*)-[0-9]{2}(\..*)$", filename)
    if match:
      new_filename = match.group(1) + match.group(2)
      os.rename(filename, new_filename)
      print(f"Renamed '{filename}' to '{new_filename}'")

if __name__ == "__main__":
  rename_files()
