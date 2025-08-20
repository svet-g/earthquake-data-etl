ALTER TABLE de_2506_a."earthquakes-svet-g"
    DROP CONSTRAINT IF EXISTS pk_id,
    DROP CONSTRAINT IF EXISTS check_latitude,
    DROP CONSTRAINT IF EXISTS check_longitude,
    DROP CONSTRAINT IF EXISTS check_sig,
    ADD CONSTRAINT pk_id PRIMARY KEY (id),
    ADD CONSTRAINT check_latitude CHECK (latitude BETWEEN -90 AND 90),
    ADD CONSTRAINT check_longitude CHECK (longitude BETWEEN -180 AND 180),
    ADD CONSTRAINT check_sig CHECK (sig >= 0);