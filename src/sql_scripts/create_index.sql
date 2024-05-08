CREATE INDEX game_dates
ON basketball.schedule (date);

CREATE INDEX valid_tickets
ON basketball.tickets (fan_id, game_id);