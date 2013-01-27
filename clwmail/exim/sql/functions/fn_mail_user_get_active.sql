/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_get_active.sql
	Function description:  . get an active user
	Date started:          . 25 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_user_get_active (varchar, varchar) RETURNS varchar
AS '

DECLARE

    in_userid       ALIAS for $1;
    in_domain       ALIAS for $2;
    resulter        users_active%rowtype;

	usercheck       VARCHAR := '''';    

BEGIN

	SELECT INTO usercheck
            userid
        FROM
            users
        WHERE
			userid  = lower(in_userid)
			AND
            domain = lower(in_domain)
            AND
            status IN (1,2)
            AND
            b_isadmin IS FALSE
        ORDER BY
            userid;

	RETURN usercheck;
END;'
    LANGUAGE plpgsql;

