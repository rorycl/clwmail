/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_get_domain_list.sql
	Function description:  . gets all available domains 
	Date started:          . 12 December 2007
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_pass_exists (VARCHAR) RETURNS BOOLEAN 
AS '
DECLARE
	function_name	VARCHAR := ''fn_mail_pass_check.sql'';
	t_password ALIAS FOR $1;
	pass_exists VARCHAR;
	
BEGIN
	SELECT INTO 
		pass_exists
		userid
		FROM 
			users
		WHERE
			password = t_password;

	IF FOUND THEN
		RETURN TRUE;
	ELSE
		RETURN FALSE;
	END IF;
END;'
    LANGUAGE plpgsql;
