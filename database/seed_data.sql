-- database/seed_data.sql

INSERT INTO locations (id, parent_id, level, name, country_code, locale) VALUES
('loc_india', NULL, 'country', 'India', 'IN', 'en-IN'),
('loc_karnataka', 'loc_india', 'state', 'Karnataka', 'IN', 'kn-IN'),
('loc_bengaluru', 'loc_karnataka', 'city', 'Bengaluru', 'IN', 'en-IN'),
('loc_delhi', 'loc_india', 'state', 'Delhi', 'IN', 'hi-IN');

INSERT INTO facilities (id, location_id, name, type) VALUES
('fac_001', 'loc_bengaluru', 'Taj West End Kitchen', 'hotel'),
('fac_002', 'loc_bengaluru', 'Majestic Bus Stand Toilet', 'public_toilet'),
('fac_003', 'loc_delhi', 'Connaught Place Garbage Point', 'garbage_point');

INSERT INTO sensors (id, facility_id, location_id, type, hardware_version, status) VALUES
('sen_001', 'fac_002', 'loc_bengaluru', 'e-nose', 'v1.2', 'active'),
('sen_002', 'fac_003', 'loc_delhi', 'bin-fill', 'v2.0', 'active');

INSERT INTO compliance_policies (id, location_id, category, title, content, standards_version) VALUES
('doc_001', 'loc_india', 'public_toilet', 'Swachh Bharat Public Toilet Norms', 'Public toilets must be cleaned twice daily. Ammonia levels > 50 ppm require immediate closure.', 'SWM_2016'),
('doc_002', 'loc_karnataka', 'solid_waste', 'BBMP SWM Rules', 'Kitchens > 50kg waste must segregate at source.', 'BBMP_2020'),
('doc_003', 'loc_india', 'kitchen_hygiene', 'FSSAI Hygiene Norms', 'Commercial kitchens must cover all waste bins.', 'FSSAI_v2');
