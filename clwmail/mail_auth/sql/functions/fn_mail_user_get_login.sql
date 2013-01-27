CREATE OR REPLACE FUNCTION fn_mail_user_get_login(character varying, character varying) RETURNS user_details
    AS $_$
DECLARE

        in_userid_domain        		ALIAS for $1;
        in_password                     ALIAS for $2;

        resulter                        user_details%rowtype;

BEGIN

        SELECT INTO
                resulter
                *
        FROM
                users
        WHERE
                userid || '@' || domain = lower(in_userid_domain)
                AND
                password = in_password;

        RETURN resulter;

END;$_$
    LANGUAGE plpgsql;

