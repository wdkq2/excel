# Excel Extraction API

This project provides a small FastAPI service that extracts four values from a JSON or CSV file exported from Excel:

- Voc
- Jsc
- FillFactor
- Efficiency

## Running locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Send a POST request to `/extract` with a file (multipart/form-data) to receive the parsed values.

CSV files exported from Excel may contain a UTF-8 BOM or extra whitespace in the
header names. The service normalizes these headers automatically so both JSON
and CSV uploads work out of the box.

## Deploying to Render
Create a Web Service and set the Build Command and Start Command as follows:

```
pip install -r requirements.txt
```

Start command is provided in the `Procfile` and should appear automatically as:

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```
=