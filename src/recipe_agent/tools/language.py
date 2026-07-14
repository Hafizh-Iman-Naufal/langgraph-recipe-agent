"""Language detection and handling utilities."""
import re


def detect_language(text: str) -> str:
    """Detect if text is English or Indonesian."""
    # Common Indonesian words
    indonesian_indicators = [
        "saya", "aku", "mau", "ingin", "yang", "bisa", "dari",
        "dan", "dengan", "untuk", "pada", "adalah", "ini", "itu", "tidak",
        "bukan", "akan", "sudah", "belum", "juga", "atau", "tapi", "tetapi",
        "karena", "sehingga", "makanan", "minuman", "resep", "masak",
        "bahannya", "ditemukan", "terdekat", "mudah", "cepat"
    ]
    
    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)
    
    # Filter out very short words (1-2 chars) to avoid false positives
    words = [w for w in words if len(w) > 2]
    
    indonesian_count = sum(1 for word in words if word in indonesian_indicators)
    
    # If more than 15% of words are Indonesian indicators, classify as Indonesian
    # Minimum 2 matches required to avoid single-word false positives
    if len(words) > 2 and indonesian_count >= 2 and (indonesian_count / len(words)) > 0.15:
        return "id"
    
    return "en"


def get_language_name(lang_code: str) -> str:
    """Get language name from code."""
    return {
        "en": "English",
        "id": "Indonesian"
    }.get(lang_code, "English")
