import os
import re

# Mapping short to full month names
MONTH_MAP = {
  'jan': 'january', 'feb': 'february', 'mar': 'march', 'apr': 'april',
  'may': 'may', 'jun': 'june', 'jul': 'july', 'aug': 'august',
  'sep': 'september', 'oct': 'october', 'nov': 'november', 'dec': 'december'
}

# Mapping month pairs to release order
EDITION_PREFIX = {
  'january-february': 1,
  'march-april': 2,
  'may-june': 3,
  'july-august': 4,
  'september-october': 5,
  'november-december': 6
}

def capitalize_first(s):
  return s[0].upper() + s[1:] if s else s

def normalize_filename(filename, year):
  name = filename[:-4]  # strip .pdf
  parts = name.lower().split('-')

  if len(parts) < 2:
    return None, f"[SKIP] Unexpected format: {filename}"

  m1 = MONTH_MAP.get(parts[0], parts[0])
  m2 = MONTH_MAP.get(parts[1], parts[1])
  key = f"{m1}-{m2}"

  prefix = EDITION_PREFIX.get(key)
  if not prefix:
    return None, f"[SKIP] Unknown edition: {key}"

  newname = f"{prefix}-{capitalize_first(m1)}-{capitalize_first(m2)}-{year}.pdf"
  if newname == filename:
    return None, "[SKIP] Already normalized"

  return newname, f"[RENAME] {filename} → {newname}"

def main(root="."):
  for dirpath, _, filenames in os.walk(root):
    year = os.path.basename(dirpath)
    if not year.isdigit():
      continue

    for filename in filenames:
      if not filename.lower().endswith('.pdf'):
        continue
      old_path = os.path.join(dirpath, filename)
      print(f"[SCAN] Checking: {old_path}")
      newname, log = normalize_filename(filename, year)
      print(f"  └── {log}")
      if newname:
        new_path = os.path.join(dirpath, newname)
        os.rename(old_path, new_path)

if __name__ == "__main__":
  main()
