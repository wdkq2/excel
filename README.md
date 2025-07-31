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

For quick testing you can also run the helper script:

```bash
python extract_values.py <path-to-file>
```

CSV files exported from Excel may contain a UTF-8 BOM, extra whitespace or use
different delimiters (comma, semicolon, tab). The API automatically normalizes
headers and detects the delimiter so both JSON and various CSV exports work out
of the box. If the summary numbers (e.g. `Voc(V) : 1.105`) appear as separate
records, the extractor searches the `NO` column using regular expressions so
these rows are still recognized.

If you upload a ZIP archive, the first `.csv` file inside the archive will be
parsed automatically before the values are extracted.

## Deploying to Render
Create a Web Service and set the Build Command and Start Command as follows:

```
pip install -r requirements.txt
```

Start command is provided in the `Procfile` and should appear automatically as:

```
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Troubleshooting on Render
On the free plan, services are automatically suspended after a period of
inactivity. Sending a request to the service URL (e.g. `/docs`) will wake it up
again, though it may take a few seconds to start. Make sure the Start Command in
Render is exactly `uvicorn main:app --host 0.0.0.0 --port $PORT`; otherwise the
server may exit immediately.
