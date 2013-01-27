CREATE OR REPLACE FUNCTION fn_holiday_manage(integer, character varying, character varying, timestamp without time zone, timestamp without time zone, character varying, integer) RETURNS integer
    AS $_$
DECLARE

    mode               ALIAS for $1;
    in_userid          ALIAS for $2;
    in_domain          ALIAS for $3;
    in_tstart          ALIAS for $4;
    in_tend            ALIAS for $5;
    in_msg             ALIAS for $6;
    in_id              ALIAS for $7;

    usercheck          VARCHAR := '';

    function_name   VARCHAR := 'fn_holiday_manage';

BEGIN

-- Data verification

    IF in_userid IS NULL THEN
        RAISE EXCEPTION 'holiday_manage_a : No userid provided';
        RETURN 0;
    END IF;

    IF in_domain IS NULL THEN
        RAISE EXCEPTION 'holiday_manage_b : No domain provided';
        RETURN 0;
    END IF;

    SELECT INTO usercheck
        userid
    FROM
        users
    WHERE
        userid = lower(in_userid)
        AND
        domain = lower(in_domain)
		AND
		b_isadmin is false;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'holiday_manage_c : user not found';
        RETURN 0;
    END IF;

    -- make person on leave
    IF mode = 1 THEN

        UPDATE
            users
        SET
            status = 2
        WHERE
            userid = lower(in_userid)
            AND
            domain = lower(in_domain);

        IF NOT FOUND THEN
            RAISE EXCEPTION 'holiday_manage_d : user not found';
            RETURN 0;
        END IF;

    -- unset leave status (default action)
    ELSE

        UPDATE
            users
        SET
            status = 1
        WHERE
            userid = lower(in_userid)
            AND
            domain = lower(in_domain);

        IF NOT FOUND THEN
            RAISE EXCEPTION 'holiday_manage_e : unsetting leave status failed';
            RETURN 0;
        END IF;

    END IF;

    RETURN 1;

END;$_$
    LANGUAGE plpgsql;

