import logging

logger = logging.getLogger(__name__)

SUPPORTED_LOCALES = ["en-IN", "hi-IN", "ta-IN", "es-ES"]
DEFAULT_LOCALE = "en-IN"

LOCALE_PROMPTS = {
    "en-IN": "You are a civic environmental assistant. Provide instructions in Indian English.",
    "hi-IN": "आप एक नागरिक पर्यावरण सहायक हैं। कृपया हिंदी (Devanagari) में उत्तर दें।",
    "ta-IN": "நீங்கள் ஒரு குடிமக்கள் சுற்றுச்சூழல் உதவியாளர். தயவுசெய்து தமிழில் பதிலளிக்கவும்.",
    "es-ES": "Eres un asistente ambiental cívico. Por favor responde en español."
}

def get_locale_prompt(locale: str) -> str:
    """
    Retrieves the system prompt for a given locale, gracefully falling back to DEFAULT_LOCALE.
    """
    if locale not in SUPPORTED_LOCALES:
        logger.warning(f"Unsupported locale '{locale}' requested. Falling back to '{DEFAULT_LOCALE}'.")
        locale = DEFAULT_LOCALE
        
    return LOCALE_PROMPTS.get(locale, LOCALE_PROMPTS[DEFAULT_LOCALE])
