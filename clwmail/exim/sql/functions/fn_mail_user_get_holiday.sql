/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_get_holiday.sql
	Function description:  . get a holiday user
	Date started:          . 25 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_user_get_holiday (varchar, varchar) RETURNS varchar
AS '
DECLARE
	
	in_userid		ALIAS for $1;
	in_domain       ALIAS for $2;

	usercheck       VARCHAR := '''';    

	this_status     INTEGER := 2;
	
BEGIN
	
	SELECT INTO 
		usercheck 
		*
	FROM
		fn_mail_user_get (in_userid, in_domain, this_status); 

	RETURN usercheck;

END;'
    LANGUAGE plpgsql;

