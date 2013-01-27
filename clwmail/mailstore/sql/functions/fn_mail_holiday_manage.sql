CREATE OR REPLACE FUNCTION fn_mail_holiday_manage(integer, character varying, character varying, 
												  timestamp without time zone, timestamp without time zone, 
												  character varying, integer, boolean) RETURNS integer
    AS $_$
DECLARE

    mode               ALIAS for $1;
    in_userid          ALIAS for $2;
    in_domain          ALIAS for $3;
    in_tstart          ALIAS for $4;
    in_tend            ALIAS for $5;
    in_msg             ALIAS for $6;
    in_id              ALIAS for $7;
    in_default         ALIAS for $8;

    usercheck          VARCHAR := '';

    new_hol_id          INTEGER;
    overlap_count       INTEGER;

    function_name   VARCHAR := 'fn_mail_holiday_manage';

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
  -- make holiday message
    IF mode = 1 THEN


		IF in_tstart > in_tend THEN
            RAISE EXCEPTION 'The start date must precede the end date';
		END IF;
			
        -- check the dates do not overlap with any existing holidays messages
        SELECT INTO overlap_count
            count(id)
        FROM
            holidays
        WHERE
            userid = lower(in_userid)
            AND
            domain = lower(in_domain)
            AND
            (in_tstart, in_tend)
            OVERLAPS
            (holidaystart, holidayend);


        IF overlap_count > 0 THEN
            RAISE EXCEPTION 'holiday messages cannot overlap';
            RETURN 0;
        END IF;

        new_hol_id := nextval('holidays_id_seq');

        INSERT INTO
            holidays
            (id, userid, domain, holidaystart, holidayend, message)
            VALUES
            (new_hol_id, lower(in_userid), lower(in_domain), in_tstart, in_tend, in_msg);

		IF in_default IS TRUE THEN 
			UPDATE 
				users
			SET 
				default_message = in_msg
			WHERE
				userid = lower(in_userid)
				AND
				domain = lower(in_domain);
		END IF;

    -- edit holiday message
    ELSIF mode =2 THEN

		IF in_tstart > in_tend THEN
            RAISE EXCEPTION 'The start date must precede the end date';
		END IF;

        -- check the dates do not overlap with any existing holidays messages
        SELECT INTO overlap_count
            count(id)
        FROM
            holidays
        WHERE
            userid = lower(in_userid)
            AND
            id != in_id
            AND
            domain = lower(in_domain)
            AND
            (in_tstart, in_tend)
            OVERLAPS
            (holidaystart, holidayend);

        IF overlap_count > 0 THEN
            RAISE EXCEPTION 'holiday messages cannot overlap';
            RETURN 0;
        END IF;

        UPDATE
            holidays
        SET
            holidaystart = in_tstart,
            holidayend = in_tend,
            message = in_msg
        WHERE
            id = in_id
            AND
            userid = lower(in_userid)
            AND
            domain = lower(in_domain);

		IF in_default IS TRUE THEN 
			UPDATE 
				users
			SET 
				default_message = in_msg
			WHERE
				userid = lower(in_userid)
				AND
				domain = lower(in_domain);
		END IF;

    -- delete holiday message
    ELSIF mode = 3 THEN

        DELETE FROM
            holidays
        WHERE
            id = in_id
            AND
            userid = lower(in_userid)
            AND
            domain = lower(in_domain);
    END IF;
    RETURN 1;

END;$_$
    LANGUAGE plpgsql;

