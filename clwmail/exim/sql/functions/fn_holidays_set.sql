/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_holidays_set.sql
	Function description:  . manage leave for a user
							 - if the current time is within a holidaystart-holidayend interval
							   then set users holiday on, set message, set end date in user table
							 - delete inserted holiday from holidays table
							 - delete holidays from holiday table that are old
							 for users table:
							 - if current time > holidayend then set status to 1
							 Returns <1 failure, 1 success on delete
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION fn_holidays_set() RETURNS integer
    AS $$
DECLARE

    usercheck       VARCHAR := '';
    function_name   VARCHAR := 'fn_holidays_set';

BEGIN

    /*********************************************************************
     Turn off old holidays in user table
    *********************************************************************/
    UPDATE
        users
    SET
        status = 1,
        holidaymsg = NULL,
        holidayend = NULL
    WHERE
        holidayend IS NOT NULL
        AND
        holidayend < current_timestamp
		AND 
		b_isadmin is FALSE;

    /*********************************************************************
     Register new holidays in user table
    *********************************************************************/
   UPDATE
        users
    SET
        status = 2,
        holidaymsg = hol_message,
        holidayend = hol_holidayend
    FROM
        (
        SELECT
            DISTINCT ON (userid, domain)
            userid       as hol_userid,
            domain       as hol_domain,
            holidaystart as hol_holidaystart,
            holidayend   as hol_holidayend,
            message      as hol_message
        FROM
            holidays
        WHERE
            current_timestamp >= holidaystart
            AND
            current_timestamp < holidayend
        ORDER BY
            userid,
            domain
            /* holidaystart -- this means first starter updates user */
        ) x
    WHERE
        userid = lower(hol_userid)
        AND
        domain = lower(hol_domain)
		AND 
		b_isadmin is FALSE;

    /*********************************************************************
 	Delete old holiday records in holidays table
    *********************************************************************/

    DELETE FROM
        holidays
    USING
        (
        SELECT
            DISTINCT ON (userid, domain)
            id as hol_id
        FROM
            holidays
        WHERE
            current_timestamp >= holidaystart
            AND
            current_timestamp < holidayend
        ORDER BY
            userid,
            domain,
            holidaystart -- this means first starter updates user
        ) x
    WHERE
        id = hol_id;

    RETURN 1;

END;$$
    LANGUAGE plpgsql;

