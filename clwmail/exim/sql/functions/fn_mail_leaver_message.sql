/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_leaver_message.sql
	Function description:  . get a user's leaver message
	Date started:          . 25 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_leaver_message (varchar, varchar) RETURNS varchar

AS '
DECLARE
	
	in_userid		ALIAS for $1;
	in_domain       ALIAS for $2;

	lvrmsg          VARCHAR := '''';    

BEGIN

	SELECT INTO lvrmsg
		leavemsg
	FROM
		users
	WHERE
		userid = lower(in_userid)
		AND
		domain = lower(in_domain)
		AND
		status = 3
		AND
		b_isadmin IS FALSE;

	RETURN lvrmsg;

END;'
    LANGUAGE plpgsql;

