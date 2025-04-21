def substitute_symbols(text: str) -> str:
    replacements = {
        '~': '¬',
        '&': '∧',
        '|': '∨',
        '$': '→',
        '%': '↔',
        '^': '⊥',
    }

    # Don't modify comments
    if ";" in text:
        formula, comment = text.split(";", 1)
        for short, full in replacements.items():
            formula = formula.replace(short, full)
        return f"{formula};{comment}"
    else:
        for short, full in replacements.items():
            text = text.replace(short, full)
        return text