import pytest
from verdaterrakai.agents.civic_campaign_agent import generate_campaign_node

def test_campaign_generation_hindi_business():
    result = generate_campaign_node(
        issue_description="Open trash bins",
        audience="business_operator",
        locale="hi-IN"
    )
    assert result["status"] == "success"
    
    campaign = result["campaign"]
    assert "महत्वपूर्ण स्वच्छता चेतावनी" in campaign["explanation"]
    assert len(campaign["checklist"]) == 2
    assert "कूड़ेदान को तुरंत ढकें" in campaign["checklist"][0]
    assert len(campaign["storyboard_script"]) == 2

def test_campaign_generation_fallback_citizen():
    result = generate_campaign_node(
        issue_description="Littering",
        audience="citizen",
        locale="fr-FR"  # Should fallback to en-IN
    )
    campaign = result["campaign"]
    assert "[en-IN]" in campaign["explanation"]
    assert "Help keep your city clean" in campaign["explanation"]
