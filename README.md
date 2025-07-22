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
