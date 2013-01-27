/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_get_user_list.sql
	Function description:  . gets all available users 
							 that are not admins
	Date started:          . 12 December 2007
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/

CREATE OR REPLACE FUNCTION 
	fn_mail_get_user_list () RETURNS SETOF user_details
AS '
DECLARE
	resulter 	    user_details%rowtype;	
	function_name	VARCHAR := ''fn_mail_get_user_lists'';
	
BEGIN

	FOR resulter IN
		SELECT 
			*
		FROM
			users
		WHERE
			b_isadmin IS FALSE
		ORDER BY
			fullname
	LOOP
		RETURN NEXT resulter;
	END LOOP;

END;'
    LANGUAGE plpgsql;
