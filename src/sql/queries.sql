SELECT * FROM regions;
SELECT * FROM species;
SELECT * FROM climate;
SELECT * FROM observations;


-- MISSION 1
-- Your query here;

SELECT * FROM observations LIMIT 10;

-- MISSION 2
-- Your query here;
SELECT DISTINCT region_id FROM observations;


-- MISSION 3
-- Your query here;
SELECT COUNT(DISTINCT species_id) AS total_species FROM observations;

-- MISSION 4
-- Your query here;
SELECT COUNT(*) AS total_observations_region_2 FROM observations WHERE region_id = 2;

-- MISSION 5
-- Your query here;
SELECT COUNT(*) AS total_observation_on_1998_08_08 FROM observations WHERE observation_date = '1998-08-08';

-- MISSION 6
-- Your query here;
SELECT region_id, COUNT(*) AS total_observations
FROM observations
GROUP BY region_id
ORDER BY total_observations DESC
LIMIT 1;

-- MISSION 7
-- Your query here;
SELECT species_id, COUNT(*) AS total_observations
FROM observations
GROUP BY species_id
ORDER BY total_observations DESC
LIMIT 5;

-- MISSION 8
-- Your query here;
SELECT species_id, COUNT(*) AS total_observations
FROM observations
GROUP BY species_id
HAVING COUNT(*) < 5
ORDER BY total_observations ASC, species_id ASC;

-- MISSION 9
-- Your query here;
SELECT observer, COUNT(*) AS total_observations
FROM observations
GROUP BY observer
ORDER BY total_observations DESC;

-- MISSION 10
-- Your query here;
SELECT o.id, r.name AS region_name, o.observer, o.observation_date
FROM observations o
JOIN regions r ON o.region_id = r.id;

-- MISSION 11
-- Your query here;
SELECT o.id, s.scientific_name, o.observer, o.observation_date
FROM observations o
JOIN species s ON o.species_id = s.id;

-- MISSION 12
-- Your query here;
SELECT region_name, scientific_name, total_observations
FROM (
    SELECT
        r.name AS region_name,
        s.scientific_name,
        COUNT(*) AS total_observations,
        ROW_NUMBER() OVER (
            PARTITION BY r.id
            ORDER BY COUNT(*) DESC
        ) AS rn
    FROM observations o
    JOIN regions r ON o.region_id = r.id
    JOIN species s ON o.species_id = s.id
    GROUP BY r.id, r.name, s.id, s.scientific_name
) ranked
WHERE rn = 1
ORDER BY region_name;