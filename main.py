from fastapi import FastAPI, File, UploadFile, HTTPException
import json
import csv
import io

from extractor import extract_values, _normalize

app = FastAPI()

async def load_data(upload_file: UploadFile):
    content = await upload_file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")
    # try JSON
    try:
        data = json.loads(text)
        if isinstance(data, dict):
            data = [data]
        return data
    except json.JSONDecodeError:
        pass
    # fallback to CSV
    reader = csv.DictReader(io.StringIO(text))
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
