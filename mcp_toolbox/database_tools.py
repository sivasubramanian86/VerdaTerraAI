import sqlite3
import json
import os
import uuid

# Connection handling supports ALLOYDB_URI conceptually, but defaults to SQLite for local dev
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "verdaterra.db")

def _get_conn():
    # In production, this would use asyncpg or psycopg2 connected to ALLOYDB_URI
    return sqlite3.connect(DB_PATH)

def query_compliance_norms(jurisdiction_id: str, query_text: str, limit: int = 3) -> list:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT title, content FROM compliance_policies WHERE location_id IN (?, 'loc_india') LIMIT ?", (jurisdiction_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [{"title": r[0], "content": r[1], "similarity_score": 0.9} for r in rows]

def read_incidents(location_id: str, days_back: int) -> list:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, severity, status FROM incidents WHERE location_id = ? ORDER BY created_at DESC", (location_id,))
    rows = cursor.fetchall()
    conn.close()
    return [{"incident_id": r[0], "category": r[1], "severity": r[2], "status": r[3]} for r in rows]

def update_incident_status(incident_id: str, new_status: str) -> dict:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("UPDATE incidents SET status = ? WHERE id = ?", (new_status, incident_id))
    conn.commit()
    conn.close()
    return {"status": "success", "incident_id": incident_id, "new_status": new_status}

def fetch_aggregated_metrics(location_id: str) -> dict:
    conn = _get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE location_id = ? AND status = 'open'", (location_id,))
    unresolved = cursor.fetchone()[0]
    conn.close()
    return {
        "location_id": location_id,
        "hygiene_score": max(0, 100 - (unresolved * 5)),
        "open_incidents": unresolved
    }

def search_nearby_hotspots(lat: float, lng: float, radius_km: float, category: str) -> list:
    # Mocks PostGIS ST_DWithin
    return [{"location_name": "Bengaluru Central", "active_critical_incidents": 2}]

def upsert_sensor_reading(sensor_id: str, reading_type: str, value: float) -> dict:
    conn = _get_conn()
    cursor = conn.cursor()
    reading_id = f"rdg_{uuid.uuid4().hex[:8]}"
    cursor.execute("""
        INSERT INTO sensor_readings (id, sensor_id, reading_type, value)
        VALUES (?, ?, ?, ?)
    """, (reading_id, sensor_id, reading_type, value))
    conn.commit()
    conn.close()
    return {"status": "success", "trigger_alert": value > 50}
