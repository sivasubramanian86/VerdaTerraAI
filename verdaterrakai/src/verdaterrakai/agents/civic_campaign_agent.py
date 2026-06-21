from typing import Dict, Any, List
from pydantic import BaseModel
from verdaterrakai.config.localization import get_locale_prompt

class StoryboardPanel(BaseModel):
    visual: str
    voiceover: str

class CampaignContent(BaseModel):
    explanation: str
    checklist: List[str]
    storyboard_script: List[StoryboardPanel]

def generate_campaign_node(issue_description: str, audience: str, locale: str) -> Dict[str, Any]:
    """
    Mock LLM generator for Civic Campaigns.
    In production, this would inject the system prompt into a Gemini LLM call
    with `response_format=CampaignContent`.
    """
    from verdaterrakai.config.localization import SUPPORTED_LOCALES, DEFAULT_LOCALE
    system_prompt = get_locale_prompt(locale)
    if locale not in SUPPORTED_LOCALES:
        locale = DEFAULT_LOCALE
    
    # Mock generation logic based on audience and locale
    explanation = f"[{locale}] Issue: {issue_description}. Audience: {audience}. "
    checklist = []
    panels = []
    
    if locale == "hi-IN":
        if audience == "business_operator":
            explanation += "यह आपके व्यवसाय के लिए एक महत्वपूर्ण स्वच्छता चेतावनी है।"
            checklist = ["[ ] कूड़ेदान को तुरंत ढकें", "[ ] कर्मचारियों को प्रशिक्षित करें"]
        else:
            explanation += "कृपया अपने शहर को स्वच्छ रखने में मदद करें।"
            checklist = ["[ ] नागरिक ऐप पर रिपोर्ट करें"]
            
        panels = [
            StoryboardPanel(visual="गंदा क्षेत्र", voiceover="आज की लापरवाही..."),
            StoryboardPanel(visual="स्वच्छ व्यवसाय", voiceover="कल का स्वास्थ्य।")
        ]
        
    else:  # Fallback/en-IN
        if audience == "business_operator":
            explanation += "Critical hygiene alert for your business."
            checklist = ["[ ] Cover bins immediately", "[ ] Train staff"]
        else:
            explanation += "Help keep your city clean."
            checklist = ["[ ] Report on citizen app"]
            
        panels = [
            StoryboardPanel(visual="Dirty area", voiceover="Today's neglect..."),
            StoryboardPanel(visual="Clean business", voiceover="Tomorrow's health.")
        ]
        
    campaign = CampaignContent(
        explanation=explanation,
        checklist=checklist,
        storyboard_script=panels
    )
    
    return {
        "status": "success",
        "system_prompt": system_prompt,
        "campaign": campaign.model_dump()
    }
