import re
import logging
from typing import Tuple, Dict, Any
import copy

logger = logging.getLogger(__name__)

def check_pii_leakage(text: str) -> Tuple[bool, str]:
    """
    Checks for potential Aadhaar, SSN, or phone number leakage.
    Returns (True, "violation reason") if violation found, else (False, "").
    """
    if not text:
        return False, ""
        
    # Basic mocked regex for Aadhaar (4-4-4) or standard phone numbers
    aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
    phone_pattern = r'\b\d{10}\b'
    
    if re.search(aadhaar_pattern, text):
        return True, "Potential Aadhaar number detected in payload."
    if re.search(phone_pattern, text):
        return True, "Potential Phone number detected in payload."
        
    return False, ""

def check_harmful_content(text: str) -> Tuple[bool, str]:
    """
    Checks for malicious prompt injections or harmful instructions.
    """
    if not text:
        return False, ""
        
    text_lower = text.lower()
    blocklist = ["ignore all previous instructions", "bypass rules", "you are now unrestricted"]
    
    for phrase in blocklist:
        if phrase in text_lower:
            return True, f"Malicious prompt injection detected: '{phrase}'."
            
    return False, ""


def redact_for_log(text: str) -> str:
    """
    A regex-driven mask that replaces 10-digit numbers and Aadhaar patterns with [REDACTED_PII].
    Safe to run before logger.info().
    """
    if not text:
        return ""
    
    aadhaar_pattern = r'\b\d{4}\s\d{4}\s\d{4}\b'
    phone_pattern = r'\b\d{10}\b'
    
    redacted = re.sub(aadhaar_pattern, '[REDACTED_PII]', text)
    redacted = re.sub(phone_pattern, '[REDACTED_PII]', redacted)
    
    return redacted


def sanitize_for_public(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strips out exact geographic coordinates and Inspector IDs from JSON objects
    before they are returned to public/citizen facing routes.
    """
    if not payload:
        return {}
        
    safe_payload = copy.deepcopy(payload)
    
    # Recursively remove sensitive keys (simplified for hackathon)
    keys_to_redact = ['lat', 'lon', 'inspector_id', 'exact_coordinates', 'internal_notes']
    
    def recursive_sanitize(obj):
        if isinstance(obj, dict):
            for k in list(obj.keys()):
                if k in keys_to_redact:
                    del obj[k]
                else:
                    recursive_sanitize(obj[k])
        elif isinstance(obj, list):
            for item in obj:
                recursive_sanitize(item)
                
    recursive_sanitize(safe_payload)
    return safe_payload
