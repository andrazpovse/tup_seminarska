-- SELECT * FROM (
-- SELECT 
--     stn.long, stn.lat,
--     AVG(sts.bikes_available / stn.dock_count) AS avg_load
-- FROM
--     status sts
--         JOIN
--     station stn ON sts.station_id = stn.id
-- WHERE
--     HOUR(time) >= 9 AND HOUR(time) <= 14
--     AND (sts.bikes_available / stn.dock_count)
-- GROUP BY station_id
-- ) x WHERE avg_load > 0.5;
SELECT 
    stn.long, stn.lat,
    AVG(sts.bikes_available / stn.dock_count) AS avg_load
FROM
    status sts
        JOIN
    station stn ON sts.station_id = stn.id
WHERE
    HOUR(time) >= %(start)s AND HOUR(time) <= %(end)s
GROUP BY station_id