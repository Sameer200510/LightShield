import re

SQL_PATTERNS = [
    r"(?i)\bselect\b",
    r"(?i)\bunion\b",
    r"(?i)\binsert\b",
    r"(?i)\bdelete\b",
    r"(?i)\bdrop\b",
    r"(?i)\bor\s+1=1\b",
]

XSS_PATTERNS = [
    r"(?i)<script.*?>.*?</script>",
    r"(?i)javascript:",
    r"(?i)onerror\s*=",
    r"(?i)onload\s*=",
]

CMD_PATTERNS = [
    r";\s*ls",
    r";\s*cat",
    r";\s*whoami",
    r"\|\|",
    r"&&",
]


def check_signature(payload: str) -> int:
    patterns = SQL_PATTERNS + XSS_PATTERNS + CMD_PATTERNS

    for pattern in patterns:
        if re.search(pattern, payload):
            return 1

    return 0