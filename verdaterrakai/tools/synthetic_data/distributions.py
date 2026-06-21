import random

CITIES = {
    "loc_bengaluru": {"name": "Bengaluru", "lat": 12.9716, "lon": 77.5946},
    "loc_delhi": {"name": "Delhi", "lat": 28.7041, "lon": 77.1025},
    "loc_mumbai": {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777}
}

WARD_ZONES = ["Transit Hub", "Commercial", "Residential"]

ZONE_WEIGHTS = {
    "Transit Hub": {
        "types": {"Public Toilet": 0.4, "Garbage Point": 0.5, "Restaurant": 0.05, "Hotel": 0.05},
        "anomaly_rate": 0.6,
        "ammonia_range": (40.0, 95.0),
        "vision_tags": ["overflowing_bin", "dirty_toilet", "flies", "puddles"]
    },
    "Commercial": {
        "types": {"Restaurant": 0.6, "Hotel": 0.2, "Public Toilet": 0.1, "Garbage Point": 0.1},
        "anomaly_rate": 0.3,
        "ammonia_range": (10.0, 40.0),
        "vision_tags": ["litter", "uncovered_bins"]
    },
    "Residential": {
        "types": {"Garbage Point": 0.8, "Public Toilet": 0.1, "Restaurant": 0.1, "Hotel": 0.0},
        "anomaly_rate": 0.1,
        "ammonia_range": (0.0, 15.0),
        "vision_tags": ["clean", "sorted_waste"]
    }
}

def get_weighted_choice(weights_dict):
    choices = list(weights_dict.keys())
    weights = list(weights_dict.values())
    return random.choices(choices, weights=weights, k=1)[0]
