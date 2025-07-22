import json
import sys
import csv
import io
import zipfile
from extractor import extract_values, TARGET_PATTERNS, _normalize

def load_file(path: str):
    """Load JSON or CSV data from a path. ZIP archives are also supported."""
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as zf:
            csv_files = [n for n in zf.namelist() if n.lower().endswith('.csv')]
            if not csv_files:
                raise ValueError("No CSV files in archive")
            text = zf.read(csv_files[0]).decode('utf-8-sig')
        return parse_text(text)
    with open(path, 'rb') as f:
        content = f.read()
    text = content.decode('utf-8-sig')
    return parse_text(text)

def parse_text(text: str):
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            data = [data]
        return data
    except json.JSONDecodeError:
        pass
    sample = text[:1024]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    rows = []
    for row in reader:
        clean = {_normalize(k): v for k, v in row.items()}
        rows.append(clean)
    return rows

def main(path):
    data = load_file(path)
    result = extract_values(data)
    for name in TARGET_PATTERNS.values():

        print(f"{name}: {result.get(name)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_values.py <data.json>")
        sys.exit(1)
    main(sys.argv[1])
