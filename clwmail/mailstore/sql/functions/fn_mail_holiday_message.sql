CREATE OR REPLACE FUNCTION fn_mail_holiday_message(character varying, character varying)
RETURNS character varying
    AS $_$
DECLARE

    in_userid       ALIAS for $1;
    in_domain       ALIAS for $2;

    holmsg          VARCHAR := '';

BEGIN

    SELECT INTO holmsg
        holidaymsg
    FROM
        users
    WHERE
        userid = lower(in_userid)
        AND
        domain = lower(in_domain)
        AND
        status = 2;

    RETURN holmsg;

END;$_$
    LANGUAGE plpgsql;

