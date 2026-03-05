REQUIRED_FIELDS = {
    'Study_Time':         (float, int),
    'Number_of_Failures': (float, int),
    'Number_of_Absences': (float, int),
    'Final_Grade':        (float, int),
    'Grade_1':            (float, int),
    'Grade_2':            (float, int),
}

FIELD_RULES = {
    'Study_Time':         {'min': 0, 'max': 10},
    'Number_of_Failures': {'min': 0, 'max': 20},
    'Number_of_Absences': {'min': 0, 'max': 100},
    'Final_Grade':        {'min': 0, 'max': 20},
    'Grade_1':            {'min': 0, 'max': 20},
    'Grade_2':            {'min': 0, 'max': 20},
}

def validate_input(data):
    errors = []
    if not isinstance(data, dict):
        return {}, ['Request body must be a JSON object.']

    for field, allowed_types in REQUIRED_FIELDS.items():
        if field not in data:
            errors.append('Missing required field: ' + field)
            continue
        if not isinstance(data[field], allowed_types):
            errors.append('Field ' + field + ' must be a number.')

    if errors:
        return {}, errors

    for field, rules in FIELD_RULES.items():
        value = data[field]
        lo = rules['min']
        hi = rules['max']
        if not (lo <= value <= hi):
            errors.append('Field ' + field + ' must be between ' + str(lo) + ' and ' + str(hi))

    if errors:
        return {}, errors

    cleaned = {field: float(data[field]) for field in REQUIRED_FIELDS}
    return cleaned, []
