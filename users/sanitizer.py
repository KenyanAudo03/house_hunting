# users/utils/sanitizer.py
import re


def clean_text(value, max_length=255):
    """
    Strip and validate simple text input.
    Allows only letters, spaces, hyphens, and apostrophes.
    Returns None if invalid.
    """
    value = (value or "").strip()
    if value and not re.match(r"^[a-zA-Z\s\-']+$", value):
        return None
    return value[:max_length]


def clean_username(value):
    """
    Validate username format.
    Allows letters, numbers, and @/./+/-/_ characters.
    Returns None if invalid.
    """
    value = (value or "").strip()
    if value and not re.match(r"^[a-zA-Z0-9_@.+-]+$", value):
        return None
    return value


def clean_phone(value):
    """
    Validate phone number format.
    Allows 10–15 digits, optionally starting with +.
    Returns None if invalid.
    """
    value = (value or "").strip()
    if value and not re.match(r"^[+]?[0-9]{10,15}$", value.replace(" ", "")):
        return None
    return value


def clean_email(value):
    """
    Basic email validation.
    Returns None if invalid.
    """
    value = (value or "").strip()
    if value and not re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        return None
    return value


def clean_bio(value, max_length=500):
    """
    Trim and restrict bio length.
    Always returns a safe string (may be empty).
    """
    return (value or "").strip()[:max_length]
