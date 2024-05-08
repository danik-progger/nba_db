CREATE FUNCTION  resign_coaches_contract()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE basketball.coaches_contracts
    SET valid_to = NEW.valid_from
    WHERE coach_id = NEW.coach_id AND is_contract_valid(valid_from, valid_to);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION  resign_players_contract()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE basketball.players_contracts
    SET valid_to = NEW.valid_from
    WHERE player_id = NEW.player_id AND is_contract_valid(valid_from, valid_to);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION  update_series_score()
RETURNS TRIGGER AS $$
DECLARE
     c INTEGER;
BEGIN
    UPDATE basketball.play_off_series
    SET date_updated = NOW()
    WHERE season = NEW.season AND home_team_code = NEW.home_team_code AND guest_team_code = NEW.guest_team_code;

    SELECT
        COUNT(*)
      INTO c
      FROM
        basketball.play_off_series
      WHERE
          season = NEW.season AND home_team_code = NEW.home_team_code AND guest_team_code = NEW.guest_team_code AND
        (NEW.games_won_ht - games_won_ht != 1
    OR
         NEW.games_won_gt - games_won_gt != 1);


    IF c > 0 THEN
        RAISE EXCEPTION 'Score must by updated by 1 win';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER resign_coaches_contract
    BEFORE INSERT ON basketball.coaches_contracts
    FOR EACH ROW
    EXECUTE FUNCTION resign_coaches_contract();

CREATE TRIGGER resign_contract
    BEFORE INSERT ON basketball.players_contracts
    FOR EACH ROW
    EXECUTE FUNCTION resign_contract();

CREATE TRIGGER update_series_score
    BEFORE UPDATE ON basketball.play_off_series
    FOR EACH ROW
    EXECUTE FUNCTION update_series_score();