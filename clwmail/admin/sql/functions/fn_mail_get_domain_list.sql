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
	fn_mail_get_domain_list () RETURNS SETOF domain_type 
AS '
DECLARE
	resulter 	    domain_type%rowtype;	
	function_name	VARCHAR := ''fn_mail_get_domain_list'';
	
BEGIN

	FOR resulter IN
		SELECT 
			*
		FROM
			domains	
		ORDER BY
			domain
	LOOP
		RETURN NEXT resulter;
	END LOOP;

END;'
    LANGUAGE plpgsql;
