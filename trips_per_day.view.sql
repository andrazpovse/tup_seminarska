CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `trips_per_day` AS
    SELECT 
        CAST(`trip`.`start_date` AS DATE) AS `trip_date`,
        COUNT(0) AS `trip_count`
    FROM
        `trip`
    GROUP BY `trip_date`