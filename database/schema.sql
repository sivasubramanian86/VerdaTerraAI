-- database/schema.sql
-- AlloyDB / PostgreSQL Mock Schema for VerdaTerraAI

CREATE TABLE IF NOT EXISTS locations (
    id TEXT PRIMARY KEY,
    parent_id TEXT,
    level TEXT NOT NULL,
    name TEXT NOT NULL,
    country_code TEXT,
    locale TEXT,
    geom TEXT, -- Mocking GEOGRAPHY
    FOREIGN KEY (parent_id) REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS facilities (
    id TEXT PRIMARY KEY,
    location_id TEXT NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    geom TEXT,
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS sensors (
    id TEXT PRIMARY KEY,
    facility_id TEXT,
    location_id TEXT,
    type TEXT NOT NULL,
    hardware_version TEXT,
    status TEXT NOT NULL,
    FOREIGN KEY (facility_id) REFERENCES facilities(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS sensor_readings (
    id TEXT PRIMARY KEY,
    sensor_id TEXT NOT NULL,
    reading_type TEXT NOT NULL,
    value REAL NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);

CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    facility_id TEXT,
    location_id TEXT,
    category TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT DEFAULT 'open',
    description TEXT,
    evidence_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (facility_id) REFERENCES facilities(id),
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE TABLE IF NOT EXISTS compliance_policies (
    id TEXT PRIMARY KEY,
    location_id TEXT NOT NULL,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    standards_version TEXT,
    -- embedding vector(768) -- pgvector mock
    FOREIGN KEY (location_id) REFERENCES locations(id)
);
