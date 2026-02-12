import re

def extract_features(text: str):

    length = len(text)
    special_chars = len(re.findall(r"[^\w\s]", text))
    digits = sum(c.isdigit() for c in text)
    uppercase = sum(c.isupper() for c in text)

    sql_keywords = len(re.findall(
        r"(select|union|insert|delete|drop|where|and|or)",
        text.lower()
    ))

    xss_keywords = len(re.findall(
        r"(script|onerror|onload|javascript)",
        text.lower()
    ))

    angle_brackets = text.count("<") + text.count(">")
    equals_count = text.count("=")

    return [
        length,
        special_chars,
        digits,
        uppercase,
        sql_keywords,
        xss_keywords,
        angle_brackets,
        equals_count
    ]
