/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_alias_resolve
	Function description:  . resolve an alias
	Date started:          . 25 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/


CREATE OR REPLACE FUNCTION 
	fn_mail_alias_resolve (varchar, varchar) RETURNS setof users_alias
AS '
DECLARE
	in_alias        ALIAS for $1;
	in_domain       ALIAS for $2;
	resulter        users_alias%rowtype;
BEGIN

    FOR resulter IN
        SELECT 
			DISTINCT
            u.userid || ''@'' || u.domain as username
        FROM
           alias_users au,
		   users u
		WHERE
			u.status IN (1,2)
			AND
			u.userid = au.userid
			AND
			u.domain = lower(in_domain)
			AND
			au.alias = lower(in_alias)
			AND 
			b_isadmin is FALSE

    LOOP
        RETURN NEXT resulter;
    END LOOP;

    RETURN;

END;'
    LANGUAGE plpgsql;

