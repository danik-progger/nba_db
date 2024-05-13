### Проект по курсу базы данных
# NBA Managment


В этом проекте представленна база данных предназначенная для управляющих баскетбольной лигой

База данных хранит информацию и историю о взаимодействии игроков и команд, тренеров и команд, а также игр между командами

Форма нормализации базы данных: 2NF

---
## Краткий экскурс в NBA:
Играют 30 команд, по 15 в каждой конференции

В каждой команде несколько игроков и 1 тренер

Регулярный чемпионат - игры, расписание которых известно заранее. По их итогам определяется сетка и расписание на серии 1/8 плей-офф.
Серии играют до 4 побед, победитель проходит в следующую стадию

---

## Ключевые сущности:

<table>
    <thead>
        <tr>
            <th colspan=4>players</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>PK</td>
            <td>player_id</td>
            <td>serial</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>name</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>weight</td>
            <td>float</td>
            <td>кг</td>
        </tr>
        <tr>
            <td></td>
            <td>height</td>
            <td>int</td>
            <td>см</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=4>coaches</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>PK</td>
            <td>coach_id</td>
            <td>serial</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>name</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>experience</td>
            <td>int</td>
            <td>годы</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=4>fans</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>PK</td>
            <td>fan_id</td>
            <td>serial</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>first_name</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>last_name</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>phone</td>
            <td>char varying(50)</td>
            <td>'+' and 10 numbers </td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=4>teams</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>PK</td>
            <td>team_code</td>
            <td>char varying(3)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>name</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>conference</td>
            <td>char</td>
            <td>W - западная, E - восточная</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=4>stadiums</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>PK</td>
            <td>stadium_id</td>
            <td>serial</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>name</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>city</td>
            <td>char varying(50)</td>
            <td></td>
        </tr>
        <tr>
            <td>FK refs teams</td>
            <td>team_code</td>
            <td>char varying(3)</td>
            <td>Стадион принадлежит команде <br>1 к 1</td>
        </tr>
    </tbody>
</table>


## Таблицы связки:
### Контракты:
Таблицы хранят историю о контрактах между игроками и командами (тренерами и командами).

Каждый контракт подписывает 1 команда и 1 игрок(тренер). У игрока(тренера) за карьеру может быть 1 или более контрактов. У команды точно хотя бы 1 подписанный тренер и точно больше 1 подписанного игрока

Версионирование SCD-2, указываются даты начала действия и оканчания контракта. Новая запись вносится при подписании нового контракта
<table>
    <thead>
        <tr>
            <th colspan=4>players_contracts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FK refs players</td>
            <td>player_id</td>
            <td>int</td>
            <td>Игрок может подписать несколько контрактов <br> В контракте только 1 игрок</td>
        </tr>
        <tr>
            <td>FK refs teams</td>
            <td>team_code</td>
            <td>int</td>
            <td>Команда подписывает несколько контрактов <br> В контракте только 1 команда</td>
        </tr>
        <tr>
            <td></td>
            <td>cost</td>
            <td>int</td>
            <td>$</td>
        </tr>
        <tr>
            <td></td>
            <td>valid_from</td>
            <td>date</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>valid_to</td>
            <td>date</td>
            <td></td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=4>tickets</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FK refs fans</td>
            <td>fan_id</td>
            <td>int</td>
            <td>У одного фаната много билетов <br> В билете ровно 1 фанат</td>
        </tr>
        <tr>
            <td>FK refs schedule</td>
            <td>game_id</td>
            <td>int</td>
            <td>На игру продано 0 или более билетов <br> В билете ровно 1 игра</td>
        </tr>
        <tr>
            <td></td>
            <td>place</td>
            <td>char varying(50)</td>
            <td>сектор - буква из ['A', 'B', 'C', 'D', 'E', 'F', 'G'] + место - число</td>
        </tr>
    </tbody>
</table>

<table>
    <thead>
        <tr>
            <th colspan=4>coaches_contracts</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FK refs coaches</td>
            <td>coach_id</td>
            <td>int</td>
            <td>Тренер может подписать несколько контрактов <br> В контракте только 1 тренер</td>
        </tr>
        <tr>
            <td>FK refs teams</td>
            <td>team_code</td>
            <td>int</td>
            <td>Команда подписывает 1 или нескольких тренеров <br> В контракте только 1 команда</td>
        </tr>
        <tr>
            <td></td>
            <td>cost</td>
            <td>int</td>
            <td>$</td>
        </tr>
        <tr>
            <td></td>
            <td>valid_from</td>
            <td>date</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>valid_to</td>
            <td>date</td>
            <td></td>
        </tr>
    </tbody>
</table>

### Сериии плей-офф:
В каждой серии играются матчи до 4 побед одной из команд

В каждой серии участвует 2 команды. Каждая команда участвует в 0+ сериях

<table>
    <thead>
        <tr>
            <th colspan=4>playoff_series</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FK refs teams</td>
            <td>home_team_code</td>
            <td>int</td>
            <td>Команда участвует в 0+ играх. В игре ровно 1 домашняя команда</td>
        </tr>
        <tr>
            <td>FK refs teams</td>
            <td>guest_team_code</td>
            <td>int</td>
            <td>Команда участвует в 0+ играх. В игре ровно 1 гостевая команда</td>
        </tr>
        <tr>
            <td></td>
            <td>games_won_ht</td>
            <td>int</td>
            <td><=4</td>
        </tr>
        <tr>
            <td></td>
            <td>games_won_gt</td>
            <td>int</td>
            <td><=4<br> games_won_ht + games_won_gt <=7</td>
        </tr>
        <tr>
            <td></td>
            <td>guest_team_code</td>
            <td>char varying(10)</td>
            <td>IN ("1/8", "1/4",  "1/2", "final")</td>
        </tr>
    </tbody>
</table>

### Игры:

Расписание составляется 1 раз и не меняется
<table>
    <thead>
        <tr>
            <th colspan=4>schedule</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>PK</td>
            <td>game_id</td>
            <td>serial</td>
            <td></td>
        </tr>
        <tr>
            <td>FK refs teams</td>
            <td>home_team_code</td>
            <td>int</td>
            <td>Команда участвет в 1+ играх. В игре ровно 1 домашняя команда</td>
        </tr>
        <tr>
            <td>FK refs teams</td>
            <td>guest_team_code</td>
            <td>int</td>
            <td>Команда участвет в 1+ играх. В игре ровно 1 гостевая команда</td>
        </tr>
        <tr>
            <td></td>
            <td>date</td>
            <td>date</td>
            <td>дата, на которую поставена игра</td>
        </tr>
    </tbody>
</table>

Результаты игры заносятся в таблицу 1 раз по окончании игры и не изменяются
<table>
    <thead>
        <tr>
            <th colspan=4>games_results</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>FK refs schedule</td>
            <td>game_id</td>
            <td>int</td>
            <td>Каждый результат относится к ровно 1 игре. У игры 0 или 1 результат</td>
        </tr>
        <tr>
            <td></td>
            <td>home_team_points</td>
            <td>int</td>
            <td></td>
        </tr>
        <tr>
            <td></td>
            <td>guest_team_points</td>
            <td>int</td>
            <td></td>
        </tr>
    </tbody>
</table>
