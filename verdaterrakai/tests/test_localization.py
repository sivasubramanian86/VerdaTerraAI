import pytest
from verdaterrakai.config.localization import get_locale_prompt, DEFAULT_LOCALE, LOCALE_PROMPTS

def test_valid_locale():
    prompt = get_locale_prompt("hi-IN")
    assert "हिंदी" in prompt

def test_unsupported_locale_fallback():
    prompt = get_locale_prompt("fr-FR")
    assert prompt == LOCALE_PROMPTS[DEFAULT_LOCALE]
