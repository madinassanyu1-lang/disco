def classify_error(exc: Exception) -> str:
    # Basic heuristics to classify errors; expand as needed
    msg = str(exc).lower()
    if "timeout" in msg or "timed out" in msg or "network" in msg:
        return "Transient"
    if "captcha" in msg or "bot" in msg or "recaptcha" in msg:
        return "Hard stop"
    if "validation" in msg or "invalid" in msg:
        return "Validation failure"
    # Default to UI inconsistency for unknown DOM related exceptions
    return "UI inconsistency"


def is_recoverable(classification: str) -> bool:
    return classification in ("Transient", "UI inconsistency")
