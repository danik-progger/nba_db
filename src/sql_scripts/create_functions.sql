CREATE FUNCTION get_team_full_name(in text, out f1 text)
AS $$
    SELECT name FROM basketball.teams
    WHERE team_code = $1
$$ LANGUAGE SQL;

CREATE FUNCTION secure(in text, out f1 text)
AS $$
    SELECT CONCAT(
                   SUBSTRING($1,0 , 4),
                   repeat('*', length($1) - 3),
                   SUBSTRING($1,length($1))
           ) AS secure_str;
$$ LANGUAGE SQL;

CREATE FUNCTION is_contract_valid(fr date, t date, out f1 bool)
AS $$
    SELECT NOW() BETWEEN $1 AND $2 AS ans;
$$ LANGUAGE SQL;

