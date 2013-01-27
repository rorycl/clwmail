CREATE OR REPLACE FUNCTION fn_holidays_show(character varying, character varying) RETURNS
SETOF user_holidays AS $_$
DECLARE
    in_userid       ALIAS for $1;
    in_domain       ALIAS for $2;
    resulter        user_holidays%rowtype;
BEGIN

    FOR resulter IN
        SELECT
           id           as holid,
           holidaystart as holstart,
           holidayend   as holend,
           message      as holmsg
        FROM
           holidays
        WHERE
            userid = lower(in_userid)
            AND
            domain = lower(in_domain)
    LOOP
        RETURN NEXT resulter;
    END LOOP;

    RETURN;

END;$_$
    LANGUAGE plpgsql;

