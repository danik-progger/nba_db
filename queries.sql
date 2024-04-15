-- 1.  10 самых опытных тренеров и их стаж
SELECT name, experience  FROM basketball.coaches
ORDER BY experience DESC
LIMIT 10;

-- 2. Все игроки когда-либо игравшие в командах тихоакеанического дивизиона
SELECT  name FROM basketball.players
WHERE player_id in (
    SELECT DISTINCT player_id FROM basketball.players_contracts
    WHERE team_code IN ('GSW', 'LAL', 'LAC', 'SAC', 'PHX')
);

-- 3. Суммарная стоимость всех контрактов игрока LeBron James в млн $
SELECT SUM(cost) / 1000000 as total FROM basketball.players_contracts
WHERE player_id IN (
    SELECT player_id FROM basketball.players
    WHERE name = 'LeBron James');

-- 4. Вывести матчи, которые пройдут в ближайшую неделю
SELECT * FROM basketball.schedule WHERE date BETWEEN NOW() AND NOW()::date + 14;

-- 5. Результаты матчей последнего месяца
SELECT home_team_code as home_team, guest_team_code as guest_team, home_team_points, guest_team_points, date
FROM (SELECT * FROM basketball.schedule
    WHERE date BETWEEN NOW()::date - 30 AND NOW()) AS s
LEFT JOIN basketball.game_results g ON s.game_id = g.game_id;

-- 6. Имя и год окончания контракта действующего тренера окманды MEM
SELECT valid_to, name FROM (
    SELECT coach_id, valid_to FROM (
        SELECT coach_id, valid_to FROM basketball.coaches_contracts
        WHERE team_code = 'MEM' AND NOW() BETWEEN valid_from AND valid_to
    ) as mem_coach) as mem_coach
LEFT JOIN basketball.coaches coaches ON mem_coach.coach_id = coaches.coach_id;

-- 7. Колличество игр в сезоне для каждой команды
SELECT team_code,
       SUM(home_games + guest_games) AS total_games
FROM (
    SELECT home_team_code AS team_code,
           COUNT(game_id) AS home_games,
           0 AS guest_games
    FROM basketball.schedule
    GROUP BY home_team_code

    UNION ALL

    SELECT guest_team_code AS team_code,
           0 AS home_games,
           COUNT(game_id) AS guest_games
    FROM basketball.schedule
    GROUP BY guest_team_code
) AS games_count
GROUP BY team_code
ORDER BY team_code;

-- 8. Текущие затраты на контракты каждой команды
SELECT team_code,
       SUM(cost) AS total_cost
FROM (
    SELECT team_code, cost
    FROM basketball.coaches_contracts
    WHERE NOW() BETWEEN valid_from AND valid_to

    UNION ALL

    SELECT team_code, cost
    FROM basketball.players_contracts
    WHERE NOW() BETWEEN valid_from AND valid_to
) AS combined_contracts
GROUP BY team_code;

-- 9. Игроки принимающие участие в ближайшем матче
SELECT name FROM (
SELECT player_id FROM basketball.players_contracts
WHERE team_code IN(
    (
        SELECT home_team_code FROM basketball.schedule
        WHERE date > NOW()
        ORDER BY date
        LIMIT 1
    )

    UNION ALL

    (
        SELECT guest_team_code FROM basketball.schedule
        WHERE date > NOW()
        ORDER BY date
        LIMIT 1
    )
)) AS c
LEFT JOIN basketball.players p ON c.player_id = p.player_id;

-- 10. Расписание игр на стадионе Лос Анжелеса
SELECT date, home_team_code, guest_team_code FROM (
    SELECT date, home_team_code, guest_team_code FROM basketball.schedule
    WHERE guest_team_code IN (
        SELECT team_code FROM basketball.stadiums
        WHERE city = 'Los Angeles')

    UNION ALL

    SELECT date, home_team_code, guest_team_code FROM basketball.schedule
    WHERE home_team_code IN (
        SELECT team_code FROM basketball.stadiums
        WHERE city = 'Los Angeles')
) as date_for_stadium_in_la
ORDER BY date;

-- 11. Команды отсортированные по колличесту выигранных матчей
SELECT name, wins FROM (SELECT t.team_code,
       SUM((r.home_team_points > r.guest_team_points)::int) +
       SUM((r.guest_team_points > r.home_team_points)::int) AS wins
FROM basketball.teams t
LEFT JOIN (
    SELECT s.home_team_code AS team_code,
           home_team_points,
           guest_team_points
    FROM basketball.game_results r
    JOIN basketball.schedule s ON r.game_id = s.game_id

    UNION ALL

    SELECT s.guest_team_code AS team_code,
           guest_team_points,
           home_team_points
    FROM basketball.game_results r
    JOIN basketball.schedule s ON r.game_id = s.game_id
) AS r ON t.team_code = r.team_code
GROUP BY t.team_code) AS team_codes
LEFT JOIN (SELECT team_code, name FROM basketball.teams) AS teams
        ON team_codes.team_code = teams.team_code
ORDER BY wins DESC;

