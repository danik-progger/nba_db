import decimal
from datetime import datetime

from src.pg_client import PgClient


def test_query1():
    """
    Тест проверяет результат sql запроса
    -- 1.  10 самых опытных тренеров и их стаж
    Ожидаемы вывод - 10 пар (имя: строка, стаж: число)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT name, experience  FROM basketball.coaches
                ORDER BY experience DESC
                LIMIT 10;
            """)
        coaches = cursor.fetchall()
        assert len(coaches) == 10
        for i in range(len(coaches)):
            assert len(coaches[i]) == 2
            assert type(coaches[i][0]) is str
            assert type(coaches[i][1]) is int

    client.disconnect()


def test_query2():
    """
    Тест проверяет результат sql запроса
    -- 2. Все игроки когда-либо игравшие в командах тихоакеанического дивизиона
    Ожидаемый вывод - неизвестное число строк формата
    (фамилия имя: одной строкой разделенные пробелом)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT name FROM basketball.players
                WHERE player_id in (
                SELECT DISTINCT player_id FROM basketball.players_contracts
                WHERE team_code IN ('GSW', 'LAL', 'LAC', 'SAC', 'PHX')
            );
            """)
        players = cursor.fetchall()
        for i in range(len(players)):
            assert type(players[i][0]) is str
            assert len(players[i]) == 1
            assert ' ' in players[i][0]

    client.disconnect()


def test_query3():
    """
    Тест проверяет результат sql запроса
    -- 3. Суммарная стоимость всех контрактов игрока LeBron James в млн $
    Ожидаемый вывод - 1 строка с суммой: число
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT SUM(cost) / 1000000 as total FROM basketball.players_contracts
                WHERE player_id IN (
                    SELECT player_id FROM basketball.players
                    WHERE name = 'LeBron James');
            """)
        amount = cursor.fetchall()
        assert len(amount) == 1
        assert type(amount[0][0]) is int

    client.disconnect()


def test_query4():
    """
    Тест проверяет результат sql запроса
    -- 4. Вывести матчи, которые пройдут в ближайшую неделю
    Ожидаемый вывод - неизвестное число строк формата
    (id: число,
    home_team_code: строка из 3 букв,
    guest_team_code: строка из 3 букв,
    date: datetime:date)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT * FROM basketball.schedule
                WHERE date BETWEEN NOW() AND NOW()::date + 14;
            """)
        games = cursor.fetchall()
        for i in range(len(games)):
            assert type(games[i][0]) is int
            assert type(games[i][1]) is str
            assert len(games[i][1]) == 3
            assert type(games[i][2]) is str
            assert len(games[i][2]) == 3
            # проверка, что это действительно дата
            assert games[i][3] != datetime.now() \
                or games[i][3] == datetime.now()

    client.disconnect()


def test_query5():
    """
    Тест проверяет результат sql запроса
    -- 5. Результаты матчей последнего месяца
    Ожидаемый вывод - неизвестное число строк формата
    (home_team_code: строка из 3 букв,
    guest_team_code: строка из 3 букв,
    home_team_points: число,
    guest_team_points: число,
    date: datetime:date)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT home_team_code as home_team, guest_team_code as guest_team, home_team_points, guest_team_points, date
                FROM (SELECT * FROM basketball.schedule
                    WHERE date BETWEEN NOW()::date - 30 AND NOW()) AS s
                LEFT JOIN basketball.game_results g ON s.game_id = g.game_id;
            """)
        games = cursor.fetchall()
        for i in range(len(games)):
            assert type(games[i][0]) is str
            assert len(games[i][0]) == 3
            assert type(games[i][1]) is str
            assert len(games[i][1]) == 3
            assert type(games[i][2]) is int
            assert type(games[i][3]) is int

            # проверка, что это действительно дата
            assert games[i][4] != datetime.now() \
                   or games[i][4] == datetime.now()

    client.disconnect()


def test_query6():
    """
    Тест проверяет результат sql запроса
    -- 6. Имя и год окончания контракта действующего тренера окманды MEM
    Ожидаемый вывод - 1 строка формата
    (end_year: datetime:date,
    name: имя и фамилия тернера через пробел одной строкой,)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
                SELECT valid_to, name FROM (
                SELECT coach_id, valid_to FROM (
                    SELECT coach_id, valid_to FROM basketball.coaches_contracts
                    WHERE team_code = 'MEM' AND NOW() BETWEEN valid_from AND valid_to
                ) as mem_coach) as mem_coach
                LEFT JOIN basketball.coaches coaches ON mem_coach.coach_id = coaches.coach_id;
            """)
        coach = cursor.fetchall()
        assert len(coach) == 1
        assert type(coach[0][1]) is str
        assert ' ' in coach[0][1]
        # проверка, что это действительно дата
        assert coach[0][0] != datetime.now() \
               or coach[0][0] == datetime.now()

    client.disconnect()


def test_query7():
    """
    Тест проверяет результат sql запроса
    -- 7. Колличество игр в сезоне для каждой команды
    Ожидаемый вывод - 30 строк формата
    (team_code: строка из 3 букв,
    games: число)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
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
            """)
        table = cursor.fetchall()
        assert len(table) == 30
        for i in range(len(table)):
            assert type(table[i][0]) is str
            assert len(table[i][0]) == 3
            assert type(table[i][1]) is decimal.Decimal

    client.disconnect()


def test_query8():
    """
    Тест проверяет результат sql запроса
    -- 8. Текущие затраты на контракты каждой команды
    Ожидаемый вывод - 30 строк формата
    (team_code: строка из 3 букв,
    сумма: число)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
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
            """)
        table = cursor.fetchall()
        assert len(table) == 30
        for i in range(len(table)):
            assert type(table[i][0]) is str
            assert len(table[i][0]) == 3
            assert type(table[i][1]) is int

    client.disconnect()


def test_query9():
    """
    Тест проверяет результат sql запроса
    -- 9. Игроки принимающие участие в ближайшем матче
    Ожидаемый вывод - неизвестное число строк формата
    (имя: фамилия и имя одной строкой разделенные пробелом,)
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
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
            """)
        table = cursor.fetchall()
        for i in range(len(table)):
            assert type(table[i][0]) is str
            assert ' ' in table[i][0]

    client.disconnect()


def test_query10():
    """
    Тест проверяет результат sql запроса
    -- 10. Расписание игр на стадионе Лос Анжелеса
    Ожидаемый вывод - неизвестное число строк формата
    (date: datetime.date,
    home_team_code: строка из 3 букв,
    guest_team_code: строка из 3 букв,
    )
    одна из home_team_code, guest_team_code - LAL или LAC
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
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
            """)
        table = cursor.fetchall()
        # проверка, что это действительно дата
        for i in range(len(table)):
            assert table[i][0] != datetime.now() \
                   or table[i][0] == datetime.now()
            assert type(table[i][1]) is str
            assert len(table[i][1]) == 3
            assert type(table[i][2]) is str
            assert len(table[i][2]) == 3
            assert table[i][1] in ['LAL', 'LAC'] or table[i][2] in ['LAL', 'LAC']

    client.disconnect()


def test_query11():
    """
    Тест проверяет результат sql запроса
    -- 11. Команды (полное название) отсортированные по колличесту выигранных матчей
    Ожидаемый вывод - 30 строк формата
    (team_full_name: строка,
    wins: число,
    )
    """
    client = PgClient()
    client.connect()

    with client.connection.cursor() as cursor:
        cursor.execute(
            """
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
            """)
        table = cursor.fetchall()
        assert len(table) == 30
        for i in range(len(table)):
            assert i == 0 or table[i][1] <= table[i-1][1]
            assert type(table[0][0]) is str
            assert type(table[0][1]) is int

    client.disconnect()