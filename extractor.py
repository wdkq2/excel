TARGET_KEYS = {
    "Voc(V) :": "Voc",
    "Jsc(mA/cm^2) :": "Jsc",
    "Fill Factor(%) :": "FillFactor",
    "Efficiency(%) :": "Efficiency"
}


def extract_values(data):
    result = {}
    for record in data:
        key = record.get("NO")
        if isinstance(key, str) and key in TARGET_KEYS:
            name = TARGET_KEYS[key]
            value = record.get("Voltage(V)")
            # convert numeric string to float if necessary
            if isinstance(value, str):
                try:
                    value = float(value)
                except ValueError:
                    continue
            result[name] = value
    return result
