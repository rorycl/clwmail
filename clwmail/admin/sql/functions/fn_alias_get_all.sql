/*
	------------------------
	CLWMail                . 
	SQL FUNCTION FOR 
	POSTGRES >8.0.x
	------------------------
	Function name:         . fn_mail_everyone.sql
	Function description:  . gets specific alias 
	Date started:          . 12 April 2006
	------------------------
	Rory Campbell-Lange	   . Campbell-Lange Workshop Limited
	------------------------

*/


CREATE OR REPLACE FUNCTION 
	fn_alias_get_all (varchar, varchar) RETURNS alias_type 
AS '
DECLARE
	in_alias		ALIAS for $1;
	in_domain       ALIAS for $2;
	resulter        alias_type%rowtype;
BEGIN

    SELECT INTO 
		resulter
		* 
	FROM
		aliases	
	WHERE
		domain = lower(in_domain)
		AND
		alias = lower(in_alias);

	RETURN  resulter;


END;'
    LANGUAGE plpgsql;

