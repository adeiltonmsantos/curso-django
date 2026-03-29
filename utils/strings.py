def is_positive(value):
    try:
        number = float(value) > 0
    except Exception:
        return False

    return number > 0
