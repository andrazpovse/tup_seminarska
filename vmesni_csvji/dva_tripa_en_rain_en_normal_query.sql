select t1.start_date, w.events, nested.start_date, nested.events
from trip t1 JOIN weather w ON w.date = date(t1.start_date) INNER JOIN (
	select t2.start_date, w1.events
	from trip t2 JOIN weather w1 ON w1.date = date(t2.start_date)) nested ON TO_DAYS(nested.start_date) = TO_DAYS(t1.start_date) + 1
    
WHERE nested.events = 'Rain' and w.events = '';