CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `day_to_day_diff` AS
    SELECT 
        `tpd1`.`trip_date` AS `day1`,
        `tpd2`.`trip_date` AS `day2`,
        (`tpd2`.`trip_count` - `tpd1`.`trip_count`) AS `diff`
    FROM
        (`trips_per_day` `tpd1`
        JOIN `trips_per_day` `tpd2` ON (((TO_DAYS(`tpd2`.`trip_date`) - TO_DAYS(`tpd1`.`trip_date`)) = 1)))