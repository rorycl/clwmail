/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_everyone.sql
	Function description:  . get everyone who is active
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/


CREATE OR REPLACE FUNCTION 
	fn_mail_everyone (varchar) RETURNS setof users_active
AS '
DECLARE
	in_domain       ALIAS for $1;
	resulter        users_active%rowtype;
BEGIN

    FOR resulter IN
        SELECT 
            userid 
        FROM
            users
		WHERE
			domain = lower(in_domain)
			AND
			status IN (1,2)
			AND
			b_isadmin IS FALSE
		ORDER BY
			userid
    LOOP
        RETURN NEXT resulter;
    END LOOP;

    RETURN;

END;'
    LANGUAGE plpgsql;

