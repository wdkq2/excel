TARGET_KEYS = {
    "Voc(V) :": "Voc",
    "Jsc(mA/cm^2) :": "Jsc",
    "Fill Factor(%) :": "FillFactor",
    "Efficiency(%) :": "Efficiency",
}

def _normalize(text: str) -> str:
    """Normalize header names read from CSV/JSON."""
    return text.strip().lstrip("\ufeff")


def _get_value(record: dict, field: str):
    for k, v in record.items():
        if _normalize(k) == field:
            return v
    return None


def extract_values(data):
    """Return the four desired values from parsed JSON/CSV records."""
    result = {}
    for record in data:
        key = _get_value(record, "NO")
        if isinstance(key, str) and key in TARGET_KEYS:
            name = TARGET_KEYS[key]
            value = _get_value(record, "Voltage(V)")


            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    continue
            result[name] = value
    return result
