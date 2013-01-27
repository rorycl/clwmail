CREATE OR REPLACE FUNCTION fn_mail_user_get_active_smtp(character varying) RETURNS SETOF users LANGUAGE plpgsql AS $_$
DECLARE
        in_email       ALIAS for $1;
        usercheck      users%ROWTYPE;

BEGIN

        SELECT INTO usercheck
                *
        FROM
            users
        WHERE
            userid || '@' || domain  = lower(in_email)
            AND
            status IN (1,2)
            AND
            b_isadmin IS FALSE
        ORDER BY
            userid;

        IF NOT FOUND THEN
                RAISE EXCEPTION 'user not found';
                RETURN;
        END IF;

        RETURN NEXT usercheck;
END;$_$;
