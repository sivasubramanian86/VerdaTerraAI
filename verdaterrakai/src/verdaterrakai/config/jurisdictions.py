import json
import os
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class Hierarchy(BaseModel):
    state: str
    district: str
    city: str

class JurisdictionConfig(BaseModel):
    name: str
    hierarchy: Hierarchy
    locales: List[str] = Field(default_factory=lambda: ["en-IN"])
    policy_packs: List[str] = Field(default_factory=lambda: ["national_swachh_bharat"])
    routing_overrides: Dict[str, str] = Field(default_factory=dict)

class JurisdictionRegistry:
    _registry: Dict[str, JurisdictionConfig] = {}
    _loaded: bool = False

    @classmethod
    def load(cls):
        if cls._loaded:
            return
        config_path = os.path.join(os.path.dirname(__file__), "jurisdictions.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for loc_id, cfg in data.items():
                    cls._registry[loc_id] = JurisdictionConfig(**cfg)
            cls._loaded = True
        except Exception as e:
            logger.error(f"Failed to load jurisdictions.json: {e}")

    @classmethod
    def get_jurisdiction(cls, location_id: str) -> Optional[JurisdictionConfig]:
        cls.load()
        return cls._registry.get(location_id)
