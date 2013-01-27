/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_get_leaver.sql
	Function description:  . get a leaver user
	Date started:          . 25 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_user_get_leaver (varchar, varchar) RETURNS varchar
AS '
DECLARE
	
	in_userid		ALIAS for $1;
	in_domain       ALIAS for $2;

	usercheck       VARCHAR := '''';    

	this_status     INTEGER := 3;
	
BEGIN
	
	SELECT INTO 
		usercheck 
		*
	FROM
		fn_mail_user_get (in_userid, in_domain, this_status); 

	RETURN usercheck;

END;'
    LANGUAGE plpgsql;

