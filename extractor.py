import re

TARGET_PATTERNS = {
    r"voc": "Voc",
    r"jsc": "Jsc",
    r"fill\s*factor": "FillFactor",
    r"efficiency": "Efficiency",
}

def _normalize(text: str) -> str:
    """Normalize header names read from CSV/JSON."""
    return text.strip().lstrip("\ufeff").lower()


def _get_value(record: dict, field: str):
    field = _normalize(field)
    for k, v in record.items():
        if _normalize(k) == field:
            return v
    return None


def extract_values(data):
    """Return the four desired values from parsed JSON/CSV records."""
    result = {}
    for record in data:
        label = str(_get_value(record, "NO") or "").lower()
        for pattern, name in TARGET_PATTERNS.items():
            if re.search(pattern, label):
                val = None
                for k, v in record.items():
                    if "volt" in _normalize(k):
                        val = v
                        break
                if val is None:
                    continue
                try:
                    result[name] = float(val)
                except (TypeError, ValueError):
                    pass
    return result
