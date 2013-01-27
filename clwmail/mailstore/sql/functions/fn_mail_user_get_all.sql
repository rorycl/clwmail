CREATE OR REPLACE FUNCTION fn_mail_user_get_all(character varying, character varying)
RETURNS user_details
    AS $_$
DECLARE

    in_userid       ALIAS for $1;
    in_domain       ALIAS for $2;
    resulter        user_details%rowtype;

BEGIN

    SELECT INTO
        resulter
        *
    FROM
       users
    WHERE
        userid = lower(in_userid)
        AND
        domain = lower(in_domain)
		AND 
		b_isadmin is FALSE;

    RETURN resulter;

END;$_$
    LANGUAGE plpgsql;

