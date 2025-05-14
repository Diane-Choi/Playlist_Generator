import re

def sanitize_file_name(file_name):
  file_name = re.sub(r'[\/:*?"<>|]', '_', file_name)
  file_name = re.sub(r'\s+', '_', file_name)
  file_name = re.sub(r'_+', '_', file_name)
  file_name = file_name.strip()
  return file_name
  