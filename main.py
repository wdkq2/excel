from fastapi import FastAPI, File, UploadFile, HTTPException
import json
import csv
import io

from extractor import extract_values, _normalize

app = FastAPI()

async def load_data(upload_file: UploadFile):
    content = await upload_file.read()
    try:
        # "utf-8-sig" strips a BOM if present
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")

    # First attempt to parse JSON
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            data = [data]
        return data
    except json.JSONDecodeError:
        pass

    # Fallback to CSV with delimiter detection
    sample = text[:1024]
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    data = []
    for row in reader:
        clean = {_normalize(k): v for k, v in row.items()}
        data.append(clean)
    return data

@app.post("/extract")
async def extract(file: UploadFile = File(...)):
    data = await load_data(file)
    result = extract_values(data)
    return result
