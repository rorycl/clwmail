/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/


CREATE OR REPLACE FUNCTION 
	fn_mail_get_alias_list () RETURNS  SETOF alias_type 
AS '
DECLARE
	resulter        alias_type%rowtype;
	function_name	VARCHAR := ''fn_mail_get_aliases_list'';
BEGIN

	FOR resulter IN
		SELECT 
			*
		FROM
			aliases	
		ORDER BY
			alias	
	LOOP
		RETURN NEXT resulter;
	END LOOP;


END;'
    LANGUAGE plpgsql;

