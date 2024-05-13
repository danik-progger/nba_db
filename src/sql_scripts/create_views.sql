CREATE VIEW basketball.schedule_full_info AS
    (SELECT get_team_full_name(home_team_code) AS home_team,
           get_team_full_name(guest_team_code) AS guest_team,
           date, city FROM basketball.schedule AS s
    LEFT JOIN
        (SELECT city, stadium.team_code, name
         FROM basketball.stadiums AS stadium
         LEFT JOIN basketball.teams AS teams
             ON teams.team_code = stadium.team_code) AS team_stadium
    ON team_stadium.team_code = s.home_team_code
    ORDER BY date);

SELECT * FROM basketball.schedule_full_info;


CREATE VIEW basketball.tickets_full_info AS
SELECT first_name, last_name, secure(phone) AS phone, place, get_team_full_name(home_team_code) as home_team, get_team_full_name(guest_team_code) as guest_team FROM
((SELECT * FROM basketball.tickets
LEFT JOIN basketball.fans f on f.fan_id = tickets.fan_id) ticket
LEFT JOIN basketball.schedule games on games.game_id = ticket.game_id);

SELECT * FROM basketball.tickets_full_info;


CREATE VIEW basketball.all_league_workers AS
SELECT * FROM
(SELECT name, team_code, 'player' as role, valid_from, valid_to FROM basketball.players
    LEFT JOIN
    basketball.players_contracts pc on players.player_id = pc.player_id
    WHERE is_contract_valid(valid_from, valid_to)

UNION

SELECT name, team_code, 'coach' as role, valid_from, valid_to FROM basketball.coaches
    LEFT JOIN
    basketball.coaches_contracts cc on coaches.coach_id = cc.coach_id
    WHERE  is_contract_valid(valid_from, valid_to)) as all_contracts;

SELECT * FROM basketball.all_league_workers;
