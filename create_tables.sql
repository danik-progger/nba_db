CREATE SCHEMA IF NOT EXISTS basketball;

CREATE TABLE
    IF NOT EXISTS basketball.teams (
        team_code character varying(3) NOT NULL PRIMARY KEY,
        name character varying(50) NOT NULL,
        conference character NOT NULL CHECK (conference IN ('W', 'E'))
    );

CREATE TABLE
    IF NOT EXISTS basketball.stadiums (
        stadium_id serial NOT NULL PRIMARY KEY,
        city character varying(40) NOT NULL,
        capacity integer NOT NULL,
        team_code character varying(3),
            FOREIGN KEY (team_code) REFERENCES basketball.teams (team_code)
    );

CREATE TABLE
    IF NOT EXISTS basketball.schedule (
        game_id serial NOT NULL PRIMARY KEY,
        home_team_code character varying(3) NOT NULL,
            FOREIGN KEY (home_team_code) REFERENCES basketball.teams (team_code),
        guest_team_code character varying(3) NOT NULL,
            FOREIGN KEY (guest_team_code) REFERENCES basketball.teams (team_code),
        date date NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS basketball.game_results (
        game_id integer NOT NULL PRIMARY KEY,
            FOREIGN KEY (game_id) REFERENCES basketball.schedule (game_id),
        home_team_points integer NOT NULL,
        guest_team_points integer NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS basketball.play_off_series (
        season date NOT NULL,
        home_team_code character varying(3) NOT NULL,
            FOREIGN KEY (home_team_code) REFERENCES basketball.teams (team_code),
        guest_team_code character varying(3) NOT NULL,
            FOREIGN KEY (guest_team_code) REFERENCES basketball.teams (team_code),
        games_won_ht integer NOT NULL CHECK (games_won_ht <= 4),
        games_won_gt integer NOT NULL CHECK (
            games_won_gt <= 4
            AND games_won_ht + games_won_gt <= 7
        ),
        phase character varying(10) NOT NULL CHECK (phase IN ('1/8', '1/4', '1/2', 'final')),
        date_updated date NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS basketball.players (
        player_id serial NOT NULL PRIMARY KEY,
        name character varying(30) NOT NULL,
        weight float NOT NULL, -- kg
        height integer NOT NULL -- sm
    );

CREATE TABLE
    IF NOT EXISTS basketball.coaches (
        coach_id serial NOT NULL PRIMARY KEY,
        name character varying(30) NOT NULL,
        experience integer NOT NULL -- years
    );

CREATE TABLE
    IF NOT EXISTS basketball.players_contracts (
        player_id integer NOT NULL,
            FOREIGN KEY (player_id) REFERENCES basketball.players (player_id),
        team_code character varying(3) NOT NULL,
            FOREIGN KEY (team_code) REFERENCES basketball.teams (team_code),
        cost integer NOT NULL, -- dollars
        valid_from date NOT NULL,
        valid_to date NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS basketball.coaches_contracts (
        coach_id integer NOT NULL,
            FOREIGN KEY (coach_id) REFERENCES basketball.coaches (coach_id),
        team_code character varying(3) NOT NULL,
            FOREIGN KEY (team_code) REFERENCES basketball.teams (team_code),
        cost integer NOT NULL, -- dollars
        valid_from date NOT NULL,
        valid_to date NOT NULL
    );
