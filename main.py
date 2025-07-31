from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import json
import csv
import io
import os
import zipfile

from extractor import extract_values, _normalize

app = FastAPI()

async def load_data(upload_file: UploadFile):
    content = await upload_file.read()

    def parse_text(text: str):
        """Parse a JSON or CSV text block into records."""
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
        rows = []
        for row in reader:
            clean = {_normalize(k): v for k, v in row.items()}
            rows.append(clean)
        return rows

    # Handle ZIP archives containing CSVs (use the first CSV file found)
    if zipfile.is_zipfile(io.BytesIO(content)):
        with zipfile.ZipFile(io.BytesIO(content)) as zf:
            csv_files = [n for n in zf.namelist() if n.lower().endswith('.csv')]
            if not csv_files:
                raise HTTPException(status_code=400, detail="No CSV files in archive")
            text = zf.read(csv_files[0]).decode('utf-8-sig')
        return parse_text(text)

    # Regular text file
    try:
        text = content.decode('utf-8-sig')
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded")

    return parse_text(text)

@app.post("/extract")
async def extract(files: List[UploadFile] = File(...)):
    """Extract values from one or more uploaded files."""
    results = []
    for upload_file in files:
        data = await load_data(upload_file)
        values = extract_values(data)
        results.append({"filename": upload_file.filename, **values})
    return results

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
