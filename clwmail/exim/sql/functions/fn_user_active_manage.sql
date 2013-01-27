/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_user_active_manage.sql
	Function description:  . make a user active
	Date started:          . dater
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_user_active_manage (varchar, varchar) RETURNS integer
AS '
DECLARE
	
	in_userid		   ALIAS for $1;
	in_domain          ALIAS for $2;

	function_name	VARCHAR := ''fn_user_active_manage'';
	
BEGIN

-- Data verification

	IF in_userid IS NULL THEN
		RAISE EXCEPTION ''usr_active_manage_a : No userid provided'';
		RETURN 0;
	END IF;

	IF in_domain IS NULL THEN
		RAISE EXCEPTION ''usr_active_manage_b : No domain provided'';
		RETURN 0;
	END IF;

	UPDATE 
		users
	SET
		status = 1
	WHERE
		userid = lower(in_userid)
		AND
		domain = lower(in_domain)
		AND
		b_isadmin IS FALSE;

	IF NOT FOUND THEN
		RAISE EXCEPTION ''usr_active_manage_c : setting active status failed'';
		RETURN 0;
	END IF;
		
	RETURN 1;

END;'
    LANGUAGE plpgsql;

