/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_get.sql
	Function description:  . get user details
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_user_get (varchar, varchar, integer) RETURNS varchar
AS '
DECLARE
	
	in_userid		ALIAS for $1;
	in_domain       ALIAS for $2;
	in_status       ALIAS for $3; -- 1 active 2 on hols 3 leaver 9 inactive

	usercheck       VARCHAR := '''';    

	this_status     INTEGER := 0;
	
BEGIN

	IF in_status = 1 or in_status IS NULL THEN
		this_status := 1;
	ELSIF in_status IN (2,3,9) THEN
		this_status := in_status;
	ELSE
		RAISE EXCEPTION ''user_get_a : status invalid'';
	END IF;

	SELECT INTO usercheck
		userid
	FROM
		users
	WHERE
		userid = lower(in_userid)
		AND
		domain = lower(in_domain)
		AND
		status = this_status
		AND 
		b_isadmin is FALSE;

	RETURN usercheck;

END;'
    LANGUAGE plpgsql;

