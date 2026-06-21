# VerdaTerraAI Synthetic Data Generator

This tool generates reproducible, statistical-driven synthetic data representing Indian cities, establishments (Hotels, Toilets, Garbage Points), and multi-sensory timeseries (Ammonia/H2S gas readings + CV tags).

## Generation
Run the generator to output CSV files:
```bash
cd tools/synthetic_data
python generate.py
```
This will populate the `output/` directory with 5 CSV files.

## Loading into AlloyDB
Since we are bypassing heavy ORMs for hackathon speed, use PostgreSQL's native `\copy` command to bulk load the data into AlloyDB.

1. Connect to your AlloyDB instance via `psql`.
2. Run the following commands (assuming your schema is already migrated):

```sql
\copy locations FROM 'output/locations.csv' DELIMITER ',' CSV HEADER;
\copy wards FROM 'output/wards.csv' DELIMITER ',' CSV HEADER;
\copy establishments FROM 'output/establishments.csv' DELIMITER ',' CSV HEADER;
\copy sensor_events FROM 'output/sensor_events.csv' DELIMITER ',' CSV HEADER;
\copy incidents FROM 'output/incidents.csv' DELIMITER ',' CSV HEADER;
```

*(Note: If you are using Cloud Run / Cloud SQL Auth proxy, you can pipe the local CSV files directly into the proxy stream using the identical `\copy` syntax.)*
