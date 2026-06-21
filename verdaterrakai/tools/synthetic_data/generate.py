import csv
import random
import uuid
from datetime import datetime, timedelta
from distributions import CITIES, WARD_ZONES, ZONE_WEIGHTS, get_weighted_choice

# Set static seed for reproducibility
random.seed(42)

NUM_WARDS_PER_CITY = 10
NUM_ESTABLISHMENTS_TOTAL = 1000
NUM_EVENTS_PER_ESTABLISHMENT = 5

OUTPUT_DIR = "output"

def generate_locations():
    locations = []
    wards = []
    
    for city_id, city_data in CITIES.items():
        locations.append({"location_id": city_id, "name": city_data["name"], "type": "city", "lat": city_data["lat"], "lon": city_data["lon"]})
        
        for w in range(NUM_WARDS_PER_CITY):
            ward_id = f"{city_id}_ward_{w}"
            zone_type = random.choice(WARD_ZONES)
            # Jitter lat/lon for ward center
            w_lat = city_data["lat"] + random.uniform(-0.1, 0.1)
            w_lon = city_data["lon"] + random.uniform(-0.1, 0.1)
            
            wards.append({
                "ward_id": ward_id,
                "city_id": city_id,
                "name": f"Ward {w} ({zone_type})",
                "zone_type": zone_type,
                "lat": w_lat,
                "lon": w_lon
            })
            
    return locations, wards

def generate_establishments(wards):
    establishments = []
    
    for _ in range(NUM_ESTABLISHMENTS_TOTAL):
        ward = random.choice(wards)
        zone = ward["zone_type"]
        
        est_type = get_weighted_choice(ZONE_WEIGHTS[zone]["types"])
        est_id = str(uuid.uuid4())
        
        # Jitter lat/lon inside ward
        e_lat = ward["lat"] + random.uniform(-0.01, 0.01)
        e_lon = ward["lon"] + random.uniform(-0.01, 0.01)
        
        establishments.append({
            "establishment_id": est_id,
            "ward_id": ward["ward_id"],
            "name": f"{est_type} {str(est_id)[:6]}",
            "type": est_type,
            "lat": e_lat,
            "lon": e_lon,
            "zone_type": zone
        })
        
    return establishments

def generate_events_and_incidents(establishments):
    events = []
    incidents = []
    
    base_time = datetime.utcnow() - timedelta(days=30)
    
    for est in establishments:
        zone = est["zone_type"]
        config = ZONE_WEIGHTS[zone]
        
        for i in range(NUM_EVENTS_PER_ESTABLISHMENT):
            event_time = base_time + timedelta(days=random.uniform(0, 30))
            
            is_anomaly = random.random() < config["anomaly_rate"]
            
            if is_anomaly:
                ammonia = random.uniform(config["ammonia_range"][0], config["ammonia_range"][1])
                tags = random.sample(config["vision_tags"], k=min(2, len(config["vision_tags"])))
            else:
                # Clean reading
                ammonia = random.uniform(0.0, 15.0)
                tags = ["clean"]
                
            events.append({
                "event_id": str(uuid.uuid4()),
                "establishment_id": est["establishment_id"],
                "timestamp": event_time.isoformat(),
                "ammonia_ppm": round(ammonia, 2),
                "vision_tags": "|".join(tags)
            })
            
            # If highly critical, log an incident
            if ammonia > 50.0:
                incidents.append({
                    "incident_id": str(uuid.uuid4()),
                    "establishment_id": est["establishment_id"],
                    "created_at": event_time.isoformat(),
                    "status": random.choice(["open", "open", "escalated", "resolved"]),
                    "description": f"Critical hygiene alert: Ammonia {round(ammonia, 2)} ppm. Tags: {','.join(tags)}"
                })
                
    return events, incidents

def write_csv(filename, data, fieldnames):
    path = f"{OUTPUT_DIR}/{filename}"
    with open(path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # Filter out keys not in fieldnames (like zone_type if we don't want it in db)
            filtered = {k: row[k] for k in fieldnames if k in row}
            writer.writerow(filtered)
    print(f"Wrote {len(data)} records to {path}")

def main():
    print("Generating Synthetic Data...")
    locs, wards = generate_locations()
    ests = generate_establishments(wards)
    events, incidents = generate_events_and_incidents(ests)
    
    write_csv("locations.csv", locs, ["location_id", "name", "type", "lat", "lon"])
    write_csv("wards.csv", wards, ["ward_id", "city_id", "name", "zone_type", "lat", "lon"])
    write_csv("establishments.csv", ests, ["establishment_id", "ward_id", "name", "type", "lat", "lon"])
    write_csv("sensor_events.csv", events, ["event_id", "establishment_id", "timestamp", "ammonia_ppm", "vision_tags"])
    write_csv("incidents.csv", incidents, ["incident_id", "establishment_id", "created_at", "status", "description"])
    
    print("Generation Complete.")

if __name__ == "__main__":
    main()
