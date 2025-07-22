import json
import sys
from extractor import extract_values, TARGET_KEYS

def main(path):
    with open(path) as f:
        data = json.load(f)
    result = extract_values(data)
    for name in TARGET_KEYS.values():
        print(f"{name}: {result.get(name)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_values.py <data.json>")
        sys.exit(1)
    main(sys.argv[1])
